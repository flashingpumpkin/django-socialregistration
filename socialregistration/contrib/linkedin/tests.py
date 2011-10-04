from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from socialregistration.contrib.linkedin.models import LinkedInProfile
from socialregistration.tests import TemplateTagTest, OAuthTest
import json
import urllib


class TestTemplateTag(TemplateTagTest, TestCase):
    def get_tag(self):
        return 'linkedin', 'linkedin_button'

class TestLinkedIn(OAuthTest, TestCase):
    profile = LinkedInProfile
    
    def get_redirect_url(self):
        return reverse('socialregistration:linkedin:redirect')
    
    def get_callback_url(self):
        return reverse('socialregistration:linkedin:callback')

    def get_setup_callback_url(self):
        return reverse('socialregistration:linkedin:setup')
    
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
            'id': '123'})
    
    def create_profile(self, user):
        LinkedInProfile.objects.create(user=user, linkedin_id='123')


class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('socialregistration.contrib.linkedin.auth.LinkedInAuth' in settings.AUTHENTICATION_BACKENDS)
