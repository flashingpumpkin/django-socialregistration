"""

Updated on 19.12.2009

@author: alen, pinda
Inspired by:
    http://github.com/leah/python-oauth/blob/master/oauth/example/client.py
    http://github.com/facebook/tornado/blob/master/tornado/auth.py
"""
import time
import base64
import urllib
import urllib2

# parse_qsl was moved from the cgi namespace to urlparse in Python2.6.
# this allows backwards compatibility
try:
    from urlparse import parse_qsl
except ImportError:
    from cgi import parse_qsl

from xml.dom import minidom

import oauth2 as oauth
from openid.consumer import consumer as openid
from openid.consumer.discover import DiscoveryFailure
from openid.store.interface import OpenIDStore as OIDStore
from openid.association import Association as OIDAssociation

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _

from django.conf import settings
from django.utils import simplejson

from django.contrib.sites.models import Site


from socialregistration.models import OpenIDStore as OpenIDStoreModel, OpenIDNonce
from urlparse import urlparse

USE_HTTPS = bool(getattr(settings, 'SOCIALREGISTRATION_USE_HTTPS', False))

def _https():
    if USE_HTTPS:
        return 's'
    else:
        return ''

class OpenIDStore(OIDStore):
    max_nonce_age = 6 * 60 * 60

    def storeAssociation(self, server_url, assoc=None):
        stored_assoc = OpenIDStoreModel.objects.create(
            server_url=server_url,
            handle=assoc.handle,
            secret=base64.encodestring(assoc.secret),
            issued=assoc.issued,
            lifetime=assoc.issued,
            assoc_type=assoc.assoc_type
        )


    def getAssociation(self, server_url, handle=None):
        stored_assocs = OpenIDStoreModel.objects.filter(
            server_url=server_url
        )
        if handle:
            stored_assocs = stored_assocs.filter(handle=handle)

        stored_assocs.order_by('-issued')

        if stored_assocs.count() == 0:
            return None

        return_val = None

        for stored_assoc in stored_assocs:
            assoc = OIDAssociation(
                stored_assoc.handle, base64.decodestring(stored_assoc.secret),
                stored_assoc.issued, stored_assoc.lifetime, stored_assoc.assoc_type
            )

            if assoc.getExpiresIn() == 0:
                stored_assoc.delete()
            else:
                if return_val is None:
                    return_val = assoc

        return return_val

    def removeAssociation(self, server_url, handle):
        stored_assocs = OpenIDStoreModel.objects.filter(
            server_url=server_url
        )
        if handle:
            stored_assocs = stored_assocs.filter(handle=handle)

        stored_assocs.delete()

    def useNonce(self, server_url, timestamp, salt):
        try:
            nonce = OpenIDNonce.objects.get(
                server_url=server_url,
                timestamp=timestamp,
                salt=salt
            )
        except OpenIDNonce.DoesNotExist:
            nonce = OpenIDNonce.objects.create(
                server_url=server_url,
                timestamp=timestamp,
                salt=salt
            )
            return True

        return False


class OpenID(object):
    def __init__(self, request, return_to, endpoint):
        """
        @param request: : django.http.HttpRequest object
        @param return_to: URL to redirect back to once the user authenticated
            the application on the OpenID provider
        @param endpoint: URL to the OpenID provider we're connecting to
        """
        self.request = request
        self.return_to = return_to
        self.endpoint = endpoint
        self.store = OpenIDStore()
        self.consumer = openid.Consumer(self.request.session, self.store)
        self.result = None
                    
    def get_redirect(self):
        auth_request = self.consumer.begin(self.endpoint)
        redirect_url = auth_request.redirectURL(
            'http%s://%s/' % (_https(), Site.objects.get_current().domain),
            self.return_to
        )
        return HttpResponseRedirect(redirect_url)

    def complete(self):
        self.result = self.consumer.complete(
            dict(self.request.GET.items()),
            'http%s://%s%s' % (_https(), Site.objects.get_current(),
                self.request.path)
        )

    def is_valid(self):
        if self.result is None:
            self.complete()

        return self.result.status == openid.SUCCESS


def get_token_prefix(url):
    """
    Returns a prefix for the token to store in the session so we can hold
    more than one single oauth provider's access key in the session.

    Example:

        The request token url ``http://twitter.com/oauth/request_token``
        returns ``twitter.com``

    """
    try:
        return urllib2.urlparse.urlparse(url).netloc
    except AttributeError:
        return urllib2.rulparse.urlparse(url)[1]


class OAuthError(Exception):
    pass

class OAuthClient(object):

    def __init__(self, request, consumer_key, consumer_secret, request_token_url,
        access_token_url, authorization_url, callback_url, parameters=None):

        self.request = request

        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.client = oauth.Client(self.consumer)

        self.signature_method = oauth.SignatureMethod_HMAC_SHA1()

        self.parameters = parameters

        self.callback_url = callback_url

        self.errors = []
        self.request_token = None
        self.access_token = None

    def _get_request_token(self):
        """
        Obtain a temporary request token to authorize an access token and to
        sign the request to obtain the access token
        """
        if self.request_token is None:
            if self.callback_url is not None:
                params = urllib.urlencode([
                    ('oauth_callback', 'http://%s%s' % (Site.objects.get_current(),
                        reverse(self.callback_url))),
                ])
                request_token_url = '%s?%s' % (self.request_token_url, params)
            else:
                request_token_url = self.request_token_url
            response, content = self.client.request(request_token_url, "GET")
            if response['status'] != '200':
                raise OAuthError(
                    _('Invalid response while obtaining request token from "%s".') % get_token_prefix(self.request_token_url))
            self.request_token = dict(parse_qsl(content))
            self.request.session['oauth_%s_request_token' % get_token_prefix(self.request_token_url)] = self.request_token
        return self.request_token

    def _get_access_token(self):
        """
        Obtain the access token to access private resources at the API endpoint.
        """
        if self.access_token is None:
            request_token = self._get_rt_from_session()
            token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
            if self.callback_url is not None:
                # If a callback_url is provided, the callback has to include a verifier.
                token.set_verifier(self.request.GET.get('oauth_verifier'))
            self.client = oauth.Client(self.consumer, token)
            response, content = self.client.request(self.access_token_url, "GET")
            if response['status'] != '200':
                raise OAuthError(
                    _('Invalid response while obtaining access token from "%s".') % get_token_prefix(self.request_token_url))
            self.access_token = dict(parse_qsl(content))

            self.request.session['oauth_%s_access_token' % get_token_prefix(self.request_token_url)] = self.access_token
        return self.access_token

    def _get_rt_from_session(self):
        """
        Returns the request token cached in the session by ``_get_request_token``
        """
        try:
            return self.request.session['oauth_%s_request_token' % get_token_prefix(self.request_token_url)]
        except KeyError:
            raise OAuthError(_('No request token saved for "%s".') % get_token_prefix(self.request_token_url))

    def _get_authorization_url(self):
        request_token = self._get_request_token()
        return '%s?oauth_token=%s' % (self.authorization_url,
            request_token['oauth_token'])

    def is_valid(self):
        try:
            self._get_rt_from_session()
            self._get_access_token()
        except OAuthError, e:
            self.errors.append(e.args[0])
            return False
        return True


    def get_redirect(self):
        """
        Returns a ``HttpResponseRedirect`` object to redirect the user to the
        URL the OAuth provider handles authorization.
        """
        return HttpResponseRedirect(self._get_authorization_url())

class OAuth(object):
    """
    Base class to perform oauth signed requests from access keys saved in a user's
    session.
    See the ``OAuthTwitter`` class below for an example.
    """

    def __init__(self, request, consumer_key, secret_key, request_token_url):
        self.request = request

        self.consumer_key = consumer_key
        self.secret_key = secret_key
        self.consumer = oauth.Consumer(consumer_key, secret_key)

        self.request_token_url = request_token_url

    def _get_at_from_session(self):
        """
        Get the saved access token for private resources from the session.
        """
        try:
            return self.request.session['oauth_%s_access_token' % get_token_prefix(self.request_token_url)]
        except KeyError:
            raise OAuthError(
                _('No access token saved for "%s".') % get_token_prefix(self.request_token_url))

    def query(self, url, method="GET", params=dict(), headers=dict()):
        """
        Request a API endpoint at ``url`` with ``params`` being either the
        POST or GET data.
        """
        access_token = self._get_at_from_session()

        token = oauth.Token(access_token['oauth_token'], access_token['oauth_token_secret'])

        client = oauth.Client(self.consumer, token)

        body = urllib.urlencode(params)

        response, content = client.request(url, method=method, headers=headers,
            body=body)

        if response['status'] != '200':
            raise OAuthError(
                _('No access to private resources at "%s".') % get_token_prefix(self.request_token_url))

        return content

class OAuthTwitter(OAuth):
    """
    Verifying twitter credentials
    """
    url = 'https://twitter.com/account/verify_credentials.json'

    def get_user_info(self):
        user = simplejson.loads(self.query(self.url))
        return user
