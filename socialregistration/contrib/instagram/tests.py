from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from socialregistration.contrib.instagram.models import InstagramProfile
from socialregistration.tests import TemplateTagTest, OAuth2Test
import json


class TestTemplateTag(TemplateTagTest, TestCase):
    def get_tag(self):
        return 'instagram', 'instagram_button'


class TestInstagram(OAuth2Test, TestCase):
    profile = InstagramProfile
    
    def get_redirect_url(self):
        return reverse('socialregistration:instagram:redirect')
    
    def get_callback_url(self):
        return reverse('socialregistration:instagram:callback')

    def get_setup_callback_url(self):
        return reverse('socialregistration:instagram:setup')
    
    def get_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, json.dumps({
            "access_token": "fb2e77d.47a0479900504cb3ab4a1f626d174d2d",
            "user": {
                "id": "1574083",
                "username": "snoopdogg",
                "full_name": "Snoop Dogg",
            }
        })
    
    def get_setup_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, json.dumps({'user': {'id': '1574083'}})
    
    def create_profile(self, user):
        InstagramProfile.objects.create(user=user, instagram='1574083')

class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('socialregistration.contrib.instagram.auth.InstagramAuth' in settings.AUTHENTICATION_BACKENDS)
