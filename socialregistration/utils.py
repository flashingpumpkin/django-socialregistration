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
from xml.dom import minidom

from oauth import oauth
from openid.consumer import consumer as openid
from openid.store.interface import OpenIDStore as OIDStore
from openid.association import Association as OIDAssociation

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _

from django.conf import settings
from django.utils import simplejson

from django.contrib.sites.models import Site


from socialregistration.models import OpenIDStore as OpenIDStoreModel, OpenIDNonce

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
        
        stored_assoc = stored_assocs[0]
        
        assoc = OIDAssociation(
            stored_assoc.handle, base64.decodestring(stored_assoc.secret),
            stored_assoc.issued, stored_assoc.lifetime, stored_assoc.assoc_type
        )
        
        return assoc

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

class OAuthClient(oauth.OAuthClient):
    """
    Simple OAuth client to perform OAuth requests 
    ( primarily connect accounts - for other requests see class OAuth below )
    """
    
    def __init__(self, request, consumer_key, consumer_secret,
        request_token_url, access_token_url, authorization_url, callback_url, parameters=None):
    
        self.request = request
    
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
    
        self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

        self.parameters = parameters
        
        self.errors = []
        
        self.callback_url = callback_url
    
    def _get_response(self, oauth_request):
        try:
            return urllib2.urlopen(oauth_request.to_url()).read()
        except urllib2.HTTPError, e:
            raise Exception('%s on %s' % (e, oauth_request.to_url()))
        
    def get_request_token(self):
        """
        Get a request token
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            self.consumer, http_url=self.request_token_url,
            parameters=self.parameters
        )
        oauth_request.sign_request(self.signature_method, self.consumer, None)
        response = self._get_response(oauth_request)
        
        if response.startswith('{'):
            # Response is in json convert to string
            oauth_token = simplejson.loads(response)['oauth_token']
            oauth_token_secret = simplejson.loads(response)['oauth_token_secret']

            response = 'oauth_token=' + oauth_token + '&oauth_token_secret=' + oauth_token_secret
            
        return oauth.OAuthToken.from_string(response)
    
    def get_access_token(self):
        """
        Get an access token
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            self.consumer, http_url=self.access_token_url, token=self.token,
            parameters=self.parameters
        )
        oauth_request.sign_request(self.signature_method, self.consumer, self.token)
        response = self._get_response(oauth_request)

        if response.startswith('<?xml'):
            # Response is in xml convert to string
            xml = minidom.parseString(response)
            oauth_token = xml.getElementsByTagName('oauth_token')[0].childNodes[0].nodeValue
            oauth_token_secret = xml.getElementsByTagName('oauth_token_secret')[0].childNodes[0].nodeValue
  
            response = 'oauth_token=' + oauth_token + '&oauth_token_secret=' + oauth_token_secret
        
        return oauth.OAuthToken.from_string(response)
    
    def token_prefix(self):
        """
        Returns a prefix for the token to store in the session so we can hold
        more than one single oauth provider's access key in the session 
        """
        if getattr(self, '_prefix', None) is None:
            self._prefix = urllib2.urlparse.urlparse(self.request_token_url).netloc
        return self._prefix
    
    @property
    def token(self):
        """ Short wrapper around get_request_token to cache the token """
        if getattr(self, '_token', None) is None:
            self._token = self.get_request_token()
        return self._token
    
    def session_token(self):
        """ Short wrapper around the token we've stored in the session """
        return self.request.session.get(
            'oauth_%s_unauthed_token' % self.token_prefix(),
            None
        )
    
    def get_authorization_url(self):
        """
        Returns the url to redirect the user to
        """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            self.consumer,
            http_url=self.authorization_url,
            token=self.token,
        )
        if self.callback_url:
            oauth_request.parameters['oauth_callback'] = Site.objects.get_current().domain + reverse(self.callback_url)

        oauth_request.sign_request(self.signature_method, self.consumer, self.token)
        return oauth_request.to_url()
    
    def get_redirect(self):
        """
        Returns a HttpResponseRedirect object to redirect the user to the url
        where authorization of the current application is handled.
        """
        self.request.session['oauth_%s_unauthed_token' % self.token_prefix()] = self.token.to_string()
        return HttpResponseRedirect(self.get_authorization_url())
    
    def is_valid(self):
        """
        Check if everything is valid after the user got redirected back to our 
        site.
        """
        if not self.session_token():
            self.errors.append(_('No un-authorized token given.'))
            return False
        
        self._token = oauth.OAuthToken.from_string(self.session_token())

        if not self.token.key == self.request.GET.get('oauth_token', 'no-token-given'):
            self.errors.append(_('The given authorization tokens do not match.'))
            return False
        
        self._token = self.get_access_token()
        self.request.session['oauth_%s_access_token' % self.token_prefix()] = self.token.to_string()
        
        return True

class OAuth(object):
    """
    Base object to perform OAuth signed requests to a service provider
    """      
    def __init__(self, request, consumer_key, secret_key, request_token_url):
        self.request = request
        self.consumer = oauth.OAuthConsumer(consumer_key, secret_key)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        
        self.request_token_url = request_token_url
        
    def token_prefix(self):
        """ 
        Create a prefix for the token so we can hold multiple different oauth
        tokens in the session 
        """
        return urllib2.urlparse.urlparse(self.request_token_url).netloc

    @property
    def access_token(self):
        if getattr(self, '_access_token', None) is None:
            self._access_token = oauth.OAuthToken.from_string(
                self.request.session['oauth_%s_access_token' % self.token_prefix()]
            )
        return self._access_token

    def get_request(self, url, parameters=None):
        """ Build a request object """
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
            self.consumer, http_url=url, token=self.access_token,
            parameters=parameters
        )
        oauth_request.sign_request(
            self.signature_method, self.consumer, self.access_token
        )
        return oauth_request

    def get_response(self, oauth_request):
        """ Submit the request and fetch the response body 
        TODO: Add POST support"""
        try:
            return urllib2.urlopen(oauth_request.to_url()).read()
        except urllib2.HTTPError, e:
            raise Exception('%s on %s' % (e, oauth_request.to_url()))

    def query(self, url, parameters=None):
        return self.get_response(
            self.get_request(url, parameters)
        )
        
class OAuthTwitter(OAuth):
    """
    Verifying twitter credentials
    """
    url = 'https://twitter.com/account/verify_credentials.json'
    
    def get_user_info(self):
        user = simplejson.loads(self.query(self.url))
        return user
    
class OAuthFriendFeed(OAuth):
    """
    Verifying friendfeed credentials
    """
    url = 'http://friendfeed-api.com/v2/validate'
    
    def get_user_info(self):
        user = simplejson.loads(self.query(self.url))
        return user
