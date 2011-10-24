from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from socialregistration.contrib.github.models import GithubProfile
from socialregistration.tests import TemplateTagTest, OAuth2Test
import json
import urllib

class TestTemplateTag(TemplateTagTest, TestCase):
    def get_tag(self):
        return 'github', 'github_button'


class TestGithub(OAuth2Test, TestCase):
    profile = GithubProfile
    
    def get_redirect_url(self):
        return reverse('socialregistration:github:redirect')
    
    def get_callback_url(self):
        return reverse('socialregistration:github:callback')

    def get_setup_callback_url(self):
        return reverse('socialregistration:github:setup')
    
    def get_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, urllib.urlencode({
            'access_token': '456'})
    
    def get_setup_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, json.dumps({'login': '123'})
    
    def create_profile(self, user):
        GithubProfile.objects.create(user=user, github='123')

class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('socialregistration.contrib.github.auth.GithubAuth' in settings.AUTHENTICATION_BACKENDS)
