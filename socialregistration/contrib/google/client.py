from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth2
from socialregistration.settings import SESSION_KEY
import json
import urllib

class Google(OAuth2):
    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', '')
    scope = getattr(settings, 'GOOGLE_REQUEST_PERMISSIONS', 'https://www.googleapis.com/auth/userinfo.profile')
    
    auth_url = 'https://accounts.google.com/o/oauth2/auth'
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    
    _user_info = None
    
    def __init__(self, access_token=None):
        super(Google, self).__init__(access_token)

    def get_callback_url(self, **kwargs):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('socialregistration:google:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('socialregistration:google:callback'))
    

    def get_redirect_url(self, state='', **kwargs):
        """
        Assemble the URL to where we'll be redirecting the user to to request
        permissions.
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.get_callback_url(**kwargs),
            'scope': self.scope or '',
            'state': state,
            'access_type': 'offline',
        }
        
        return '%s?%s' % (self.auth_url, urllib.urlencode(params))

    def parse_access_token(self, content):
        parsed = json.loads(content)

        if 'refresh_token' in parsed:
            self._refresh_token = 're:%s' % parsed.get('refresh_token')
            return {'access_token': 're:%s' % parsed.get('refresh_token')}

        return parsed
    
    def request_access_token(self, params):
        """ 
        Google requires correct content-type for POST requests
        """
        return self.client().request(self.access_token_url, method="POST", body=urllib.urlencode(params), headers={'Content-Type': 'application/x-www-form-urlencoded'})
    
    def get_access_token(self, grant_type='authorization_code', **params):
        """
        Google requires grant_type
        """
        return super(Google, self).get_access_token(grant_type=grant_type, **params)
    
    def new_access_token(self, **params):
        if self._access_token.startswith("re:"):
            token = super(Google, self).get_access_token(grant_type='refresh_token', refresh_token=self._access_token[3:])
        else:
            token = self._access_token

        return token

    def get_user_info(self):
        if self._user_info is None:
            nat = self.new_access_token()
            resp, content = self.request('https://www.googleapis.com/oauth2/v1/userinfo', params={'access_token': nat})
            self._user_info = json.loads(content)
        return self._user_info
    
    @staticmethod
    def get_session_key():
        return '%sgoogle' % SESSION_KEY
