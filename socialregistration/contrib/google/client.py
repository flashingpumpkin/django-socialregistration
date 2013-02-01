from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth2, OAuthError
from socialregistration.settings import SESSION_KEY
import json
import httplib2
import urllib

class Google(OAuth2):
    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', '')
    scope = getattr(settings, 'GOOGLE_REQUEST_PERMISSIONS', 'https://www.googleapis.com/auth/userinfo.profile')
    
    auth_url = 'https://accounts.google.com/o/oauth2/auth'
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    
    _user_info = None
    
    def get_callback_url(self, **kwargs):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('socialregistration:google:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('socialregistration:google:callback'))
    
    def parse_access_token(self, content):
        """ 
        Forsquare returns JSON instead of url encoded data.
        """
        return json.loads(content)
    
    def request_access_token(self, params):
        """ 
        Google requires correct content-type for POST requests
        """
        return self.client().request(self.access_token_url, method="POST", body=urllib.urlencode(params), headers={'Content-Type':'application/x-www-form-urlencoded'})
    
    def get_access_token(self, **params):
        """
        Google requires grant_type
        """
        return super(Google, self).get_access_token(grant_type='authorization_code', **params)
    
    def get_user_info(self):
        if self._user_info is None:
            resp, content = self.request('https://www.googleapis.com/oauth2/v1/userinfo', params={'access_token': self._access_token})
            self._user_info = json.loads(content)
        return self._user_info
    
    @staticmethod
    def get_session_key():
        return '%sgoogle' % SESSION_KEY
