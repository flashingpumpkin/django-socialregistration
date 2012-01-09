from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth
from socialregistration.settings import SESSION_KEY
import json
import urlparse

class Tumblr(OAuth):
    api_key = getattr(settings, 'TUMBLR_CONSUMER_KEY', '')
    secret_key = getattr(settings, 'TUMBLR_CONSUMER_SECRET_KEY', '')
    
    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'
    auth_url = 'http://www.tumblr.com/oauth/authorize'
    
    def get_callback_url(self):
        if self.is_https():
            return urlparse.urljoin(
                'https://%s' % Site.objects.get_current().domain,
                reverse('socialregistration:tumblr:callback'))
        return urlparse.urljoin(
            'http://%s' % Site.objects.get_current().domain,
            reverse('socialregistration:tumblr:callback'))

    def get_user_info(self):
        if self._user_info is None:
            self._user_info = json.loads(
                self.request('http://api.tumblr.com/v2/user/info'))['response']['user']
        return self._user_info
    
    @staticmethod
    def get_session_key():
        return '%stumblr' % SESSION_KEY


