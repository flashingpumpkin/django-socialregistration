from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth2
from socialregistration.settings import SESSION_KEY
import json


class Instagram(OAuth2):
    client_id = getattr(settings, 'INSTAGRAM_CLIENT_ID', '')
    secret = getattr(settings, 'INSTAGRAM_CLIENT_SECRET', '')
    scope = getattr(settings, 'INSTAGRAM_REQUEST_PERMISSIONS', 'basic')
    
    auth_url = 'https://api.instagram.com/oauth/authorize/'
    access_token_url = 'https://api.instagram.com/oauth/access_token/'
    
    _user_info = None
    
    def get_callback_url(self, **kwargs):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('socialregistration:instagram:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('socialregistration:instagram:callback'))

    def get_access_token(self, **params):
        """
        Instagram requires a `grant_type` parameter when requesting the access
        token. 
        """
        return super(Instagram, self).get_access_token(grant_type='authorization_code', **params)


    def parse_access_token(self, content):
        return json.loads(content)
        
    def get_user_info(self):
        return self.access_token_dict['user']['id']

    
    @staticmethod
    def get_session_key():
        return '%sinstagram' % SESSION_KEY
