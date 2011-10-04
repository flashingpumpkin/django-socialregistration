from django.utils.translation import ugettext_lazy as _
from socialregistration.clients import Client
import httplib2
import oauth2 as oauth
import urllib
import urlparse


class OAuthError(Exception):
    pass

class OAuth(Client):
    api_key = None
    secret_key = None
    
    auth_url = None
    request_token_url = None
    access_token_url = None
    
    _request_token = None
    _access_token = None
    _access_token_dict = None
    _user_info = None
    
    def __init__(self, access_token=None, access_token_secret=None):
        self.consumer = oauth.Consumer(self.api_key, self.secret_key)
        
        if access_token and access_token_secret:
            self._access_token = oauth.Token(access_token, access_token_secret)
        
    def client(self, verifier=None):
        if not self._request_token and not self._access_token:
            client = oauth.Client(self.consumer)
        if self._request_token and not self._access_token:
            if verifier is not None:
                self._request_token.set_verifier(verifier)
            client = oauth.Client(self.consumer, self._request_token)
        if self._access_token:
            client = oauth.Client(self.consumer, self._access_token)
        
        return client

    def _get_request_token(self):
        params = {
            'oauth_callback': self.get_callback_url()
        }
        
        response, content = self.client().request(self.request_token_url,
            "POST", body=urllib.urlencode(params))
        
        if not response['status'] == '200':
            raise OAuthError(_(
                "Invalid status code %s while obtaining request token from %s: %s") % (
                    response['status'], self.request_token_url, content))
        
        token = dict(urlparse.parse_qsl(content))
        
        return oauth.Token(token['oauth_token'], token['oauth_token_secret'])
    
    def _get_access_token(self, verifier=None):
        response, content = self.client(verifier).request(
            self.access_token_url, "POST")
        
        if not response['status'] == '200':
            raise OAuthError(_(
                "Invalid status code %s while obtaining access token from %s: %s") % 
                (response['status'], self.access_token_url, content))
        
        token = dict(urlparse.parse_qsl(content))
        
        
        return (oauth.Token(token['oauth_token'], token['oauth_token_secret']),
            token)
        
    def get_request_token(self):
        if self._request_token is None:
            self._request_token = self._get_request_token()
        return self._request_token
    
    def get_access_token(self, verifier=None):
        if self._access_token is None:
            self._access_token, self._access_token_dict = self._get_access_token(verifier)
        return self._access_token
    
    
    def get_redirect_url(self):
        params = {
            'oauth_token': self.get_request_token().key,
        }
        return '%s?%s' % (self.auth_url, urllib.urlencode(params))
    
    def complete(self, GET):
        token = self.get_access_token(verifier=GET.get('oauth_verifier', None))
        return token
    
    def get_user_info(self):
        return self._access_token_dict or {}
    
    def request(self, url, method="GET", params=None, headers=None):
        params = params or {}
        headers = headers or {}
        
        response, content = self.client().request(url, method, headers=headers,
            body=urllib.urlencode(params))
        
        if response['status'] != '200':
            raise OAuthError(_(
                "Invalid status code %s while requesting %s: %s") % (
                    response['status'], url, content))
        
        return content
    
    
class OAuth2(Client):
    client_id = None
    secret = None
    
    auth_url = None
    access_token_url = None
    scope = None
    
    _access_token = None
    _user_info = None
    
    def __init__(self, access_token=None):
        self._access_token = access_token
    
    def client(self):
        return httplib2.Http()
    
    def get_redirect_url(self, state=''):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.get_callback_url(),
            'scope': self.scope or '',
            'state': state,
        }
        
        return '%s?%s' % (self.auth_url, urllib.urlencode(params))
    
    def parse_access_token(self, content):
        return dict(urlparse.parse_qsl(content))

    def request_access_token(self, params):
        return self.request(self.access_token_url, method="POST", params=params)
    
    def _get_access_token(self, code, **params):
        params.update({
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.secret,
            'redirect_uri': self.get_callback_url(),
        })
        
        resp, content = self.request_access_token(params=params)
        
        content = self.parse_access_token(content)
        
        if 'error' in content:
            raise OAuthError(_(
                "Received error while obtaining access token from %s: %s") % (
                    self.access_token_url, content['error']))

        return content
    
    def get_access_token(self, code=None, **params):
        if self._access_token is None:
            if code is None:
                raise ValueError(_('Invalid code.'))
            self._access_token = self._get_access_token(code, **params)['access_token']
        return self._access_token
    
    def complete(self, GET):
        return self.get_access_token(code=GET.get('code'))        

    def get_signing_params(self):
        return dict(access_token=self._access_token)
        
    def request(self, url, method="GET", params=None, headers=None):
        params = params or {}
        headers = headers or {}
        
        params.update(self.get_signing_params())
        
        if method.upper() == "GET":
            url = '%s?%s' % (url, urllib.urlencode(params))
            return self.client().request(url, method=method, headers=headers)
        return self.client().request(url, method, body=urllib.urlencode(params),
            headers=headers)
        
    def get_user_info(self):
        raise NotImplementedError
    
    def get_callback_url(self):
        raise NotImplementedError
    
