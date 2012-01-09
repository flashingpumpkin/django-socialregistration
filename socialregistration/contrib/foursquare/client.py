from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth2
from socialregistration.settings import SESSION_KEY
import json


class Foursquare(OAuth2):
    client_id = getattr(settings, 'FOURSQUARE_CLIENT_ID', '')
    secret = getattr(settings, 'FOURSQUARE_CLIENT_SECRET', '')
    scope = getattr(settings, 'FOURSQUARE_REQUEST_PERMISSIONS', '')
    
    auth_url = 'https://foursquare.com/oauth2/authorize'
    access_token_url = 'https://foursquare.com/oauth2/access_token'
    
    _user_info = None
    
    def get_callback_url(self):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('socialregistration:foursquare:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('socialregistration:foursquare:callback'))
    
    def parse_access_token(self, content):
        """ 
        Forsquare returns JSON instead of url encoded data.
        """
        return json.loads(content)
    
    def request_access_token(self, params):
        """ 
        Foursquare does not accept POST requests to retrieve an access token,
        so we'll be doing a GET request instead.
        """
        return self.request(self.access_token_url, method="GET", params=params)
    
    def get_access_token(self, **params):
        """
        Foursquare requires a `grant_type` parameter when requesting the access
        token. 
        """
        return super(Foursquare, self).get_access_token(grant_type='authorization_code', **params)

    def get_signing_params(self):
        """
        Foursquare requires `oauth_token` parameter instead of `access_token` 
        """
        return dict(oauth_token=self._access_token)
    
    def get_user_info(self):
        if self._user_info is None:
            resp, content = self.request('https://api.foursquare.com/v2/users/self')
            self._user_info = json.loads(content)['response']['user']
        return self._user_info
    
    @staticmethod
    def get_session_key():
        return '%sfoursquare' % SESSION_KEY
