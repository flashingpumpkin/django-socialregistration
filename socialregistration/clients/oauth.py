from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from socialregistration.clients import Client
import httplib2
import oauth2 as oauth
import urllib
import urlparse


class OAuthError(Exception):
    """ 
    Exception thrown when we run into OAuth{1,2} errors. This error is 
    displayed to the end user in the default templates. 
    """
    pass

class OAuth(Client):
    """
    Base class for OAuth1 services such as Twitter, LinkedIn and Tumblr. 
    """
    
    # The API key provided by the service 
    api_key = None
    
    # The secret key provided by the service 
    secret_key = None
    
    # The authorization / authentication URL we'll be asking the user for
    # permissions at
    auth_url = None
    
    # The request token URL we'll be fetching the request token from
    request_token_url = None
    
    # The access token URL we'll be fetching the access token from
    access_token_url = None
    
    # Memoized request token
    _request_token = None
    
    # Memoized access token
    _access_token = None
    
    # Memoized dict of whole access token response
    _access_token_dict = None
    
    # Memoized user information 
    _user_info = None
    
    def __init__(self, access_token=None, access_token_secret=None):
        self.consumer = oauth.Consumer(self.api_key, self.secret_key)
        
        if access_token and access_token_secret:
            self._access_token = oauth.Token(access_token, access_token_secret)
        
    def client(self, verifier=None):
        """
        Return the correct client depending on which stage of the OAuth process
        we're in.
        """
        # We're just starting out and don't have neither request nor access
        # token. Return the standard client
        if not self._request_token and not self._access_token:
            client = oauth.Client(self.consumer)
        
        # We're one step in, we've got the request token and can add that to 
        # the client.
        if self._request_token and not self._access_token:
            if verifier is not None:
                self._request_token.set_verifier(verifier)
            client = oauth.Client(self.consumer, self._request_token)
            
        # Two steps in, we've got an access token and can now properly sign 
        # our client requests with it.
        if self._access_token:
            client = oauth.Client(self.consumer, self._access_token)
        
        return client

    def _get_request_token(self):
        """
        Fetch a request token from `self.request_token_url`.
        """
        
        params = {
            'oauth_callback': self.get_callback_url()
        }
        
        
        response, content = self.client().request(self.request_token_url,
            "POST", body=urllib.urlencode(params))
        
        content = smart_unicode(content)
        
        if not response['status'] == '200':
            raise OAuthError(_(
                u"Invalid status code %s while obtaining request token from %s: %s") % (
                    response['status'], self.request_token_url, content))
        
        token = dict(urlparse.parse_qsl(content))
        
        return oauth.Token(token['oauth_token'], token['oauth_token_secret'])
    
    def _get_access_token(self, verifier=None):
        """
        Fetch an access token from `self.access_token_url`.
        """
        
        response, content = self.client(verifier).request(
            self.access_token_url, "POST")
        
        content = smart_unicode(content)
        
        if not response['status'] == '200':
            raise OAuthError(_(
                u"Invalid status code %s while obtaining access token from %s: %s") % 
                (response['status'], self.access_token_url, content))
        
        token = dict(urlparse.parse_qsl(content))
        
        
        return (oauth.Token(token['oauth_token'], token['oauth_token_secret']),
            token)
        
    def get_request_token(self):
        """
        Return the request token for this API. If we've not fetched it yet,
        go out, request and memoize it.
        """
        
        if self._request_token is None:
            self._request_token = self._get_request_token()
        return self._request_token
    
    def get_access_token(self, verifier=None):
        """
        Return the access token for this API. If we've not fetched it yet,
        go out, request and memoize it.
        """
        
        if self._access_token is None:
            self._access_token, self._access_token_dict = self._get_access_token(verifier)
        return self._access_token
    
    
    def get_redirect_url(self):
        """
        Return the authorization/authentication URL signed with the request 
        token.
        """
        params = {
            'oauth_token': self.get_request_token().key,
        }
        return '%s?%s' % (self.auth_url, urllib.urlencode(params))
    
    def complete(self, GET):
        """
        When redirect back to our application, try to complete the flow by
        requesting an access token. If the access token request fails, it'll
        throw an `OAuthError`.
        
        Tries to complete the flow by validating against the `GET` paramters 
        received.
        """
        token = self.get_access_token(verifier=GET.get('oauth_verifier', None))
        return token
    
    def request(self, url, method="GET", params=None, headers=None):
        """
        Make signed requests against `url`.
        """
        params = params or {}
        headers = headers or {}
        
        response, content = self.client().request(url, method, headers=headers,
            body=urllib.urlencode(params))
        
        content = smart_unicode(content)
        
        if response['status'] != '200':
            raise OAuthError(_(
                u"Invalid status code %s while requesting %s: %s") % (
                    response['status'], url, content))
        
        return content
    
    
class OAuth2(Client):
    """
    Base class for OAuth2 services such as Facebook, Github and Foursquare.
    """
    
    # The client id provided by the service
    client_id = None
     
    # The secret id provided by the service 
    secret = None
    
    # The URL where we'll be requesting permissions from the user
    auth_url = None
    
    # The URL where we'll be obtaining an access token once permissions were
    # granted
    access_token_url = None
    
    # The permission's we'll be asking for
    scope = None
    
    # The access token we obtained
    _access_token = None
    
    # Memoized user info fetched once an access token was obtained
    _user_info = None
    
    def __init__(self, access_token=None):
        self._access_token = access_token
    
    def client(self):
        return httplib2.Http()
    
    def get_redirect_url(self, state=''):
        """
        Assemble the URL to where we'll be redirecting the user to to request
        permissions.
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.get_callback_url(),
            'scope': self.scope or '',
            'state': state,
        }
        
        return '%s?%s' % (self.auth_url, urllib.urlencode(params))
    
    def parse_access_token(self, content):
        """
        Parse the access token response. The default OAuth response should be
        a query string - but some services return JSON instead. 
        """
        return dict(urlparse.parse_qsl(content))

    def request_access_token(self, params):
        """
        Request the access token from `self.access_token_url`. The default 
        behaviour is to use a `POST` request, but some services use `GET` 
        requests. Individual clients can override this method to use the 
        correct HTTP method.
        """
        return self.request(self.access_token_url, method="POST", params=params)
    
    def _get_access_token(self, code, **params):
        """
        Fetch an access token with the provided `code`.
        """
        params.update({
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.secret,
            'redirect_uri': self.get_callback_url(),
        })
        
        resp, content = self.request_access_token(params=params)
        
        content = smart_unicode(content)
        
        content = self.parse_access_token(content)
        
        if 'error' in content:
            raise OAuthError(_(
                u"Received error while obtaining access token from %s: %s") % (
                    self.access_token_url, content['error']))

        return content
    
    def get_access_token(self, code=None, **params):
        """
        Return the memoized access token or go out and fetch one.
        """
        if self._access_token is None:
            if code is None:
                raise ValueError(_('Invalid code.'))
            
            access_token_dict = self._get_access_token(code, **params)
            try:
                self._access_token = access_token_dict['access_token']
            except KeyError, e:
                raise OAuthError("Credentials could not be validated, the provider returned no access token.")
                
        return self._access_token
    
    def complete(self, GET):
        """
        Complete the OAuth2 flow by fetching an access token with the provided
        code in the GET parameters.
        """
        if 'error' in GET:
            raise OAuthError(
                _("Received error while obtaining access token from %s: %s") % (
                    self.access_token_url, GET['error']))
        return self.get_access_token(code=GET.get('code'))        

    def get_signing_params(self):
        """
        Return the paramters for signing a request. Some APIs don't 
        obey the standard `access_token` parameter - they can override this 
        method and return their used parameters.
        """
        return dict(access_token=self._access_token)
        
    def request(self, url, method="GET", params=None, headers=None):
        """
        Make signed requests against `url`.
        """
        params = params or {}
        headers = headers or {}
        
        params.update(self.get_signing_params())
        
        if method.upper() == "GET":
            url = '%s?%s' % (url, urllib.urlencode(params))
            return self.client().request(url, method=method, headers=headers)
        return self.client().request(url, method, body=urllib.urlencode(params),
            headers=headers)
        

