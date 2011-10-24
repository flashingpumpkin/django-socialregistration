from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from socialregistration.contrib.foursquare.models import FoursquareProfile
from socialregistration.tests import TemplateTagTest, OAuth2Test
import json


class TestTemplateTag(TemplateTagTest, TestCase):
    def get_tag(self):
        return 'foursquare', 'foursquare_button'

class TestFoursquare(OAuth2Test, TestCase):
    profile = FoursquareProfile

    def get_redirect_url(self):
        return reverse('socialregistration:foursquare:redirect')
    
    def get_callback_url(self):
        return reverse('socialregistration:foursquare:callback')

    def get_setup_callback_url(self):
        return reverse('socialregistration:foursquare:setup')
    
    def get_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, json.dumps({
            'access_token': '456'})
    
    def get_setup_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, json.dumps({
            'response': {
                'user':{
                    'id': '123'}}})
    
    def create_profile(self, user):
        FoursquareProfile.objects.create(user=user, foursquare='123')

    
class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('socialregistration.contrib.foursquare.auth.FoursquareAuth' in settings.AUTHENTICATION_BACKENDS)
