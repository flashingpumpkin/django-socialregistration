from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from socialregistration.contrib.tumblr.models import TumblrProfile
from socialregistration.tests import TemplateTagTest, OAuthTest
import json
import urllib


class TestTemplateTag(TemplateTagTest, TestCase):
    def get_tag(self):
        return 'tumblr', 'tumblr_button'

class TestTumblr(OAuthTest, TestCase):
    profile = TumblrProfile
    
    def get_redirect_url(self):
        return reverse('socialregistration:tumblr:redirect')
    
    def get_callback_url(self):
        return reverse('socialregistration:tumblr:callback')

    def get_setup_callback_url(self):
        return reverse('socialregistration:tumblr:setup')
    
    def get_redirect_mock_response(self, *args, **kwargs):
        return {'status': '200'}, urllib.urlencode({
            'oauth_token': '123',
            'oauth_token_secret': '456'})
    
    def get_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, urllib.urlencode({
            'oauth_token': '456',
            'oauth_token_secret': '789'})
    
    def get_setup_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, json.dumps({ 
            'response': {
                'user': {
                    'name': '123'}}})

    def create_profile(self, user):
        TumblrProfile.objects.create(user=user, tumblr='123')

class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('socialregistration.contrib.tumblr.auth.TumblrAuth' in settings.AUTHENTICATION_BACKENDS)
