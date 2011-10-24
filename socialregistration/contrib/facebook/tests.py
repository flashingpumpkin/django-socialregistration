from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from socialregistration.contrib.facebook.models import FacebookProfile
from socialregistration.tests import TemplateTagTest, OAuth2Test, get_mock_func
import json
import mock
import urllib

class TestTemplateTag(TemplateTagTest, TestCase):
    def get_tag(self):
        return 'facebook', 'facebook_button'

class TestFacebook(OAuth2Test, TestCase):
    profile = FacebookProfile

    def get_redirect_url(self):
        return reverse('socialregistration:facebook:redirect')
    
    def get_callback_url(self):
        return reverse('socialregistration:facebook:callback')

    def get_setup_callback_url(self):
        return reverse('socialregistration:facebook:setup')
    
    def get_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, urllib.urlencode({
            'access_token': '456'})
    
    def get_setup_callback_mock_response(self, *args, **kwargs):
        return {'status': '200'}, json.dumps({'id': '123'})
    
    def create_profile(self, user):
        FacebookProfile.objects.create(user=user, uid='123')

    def get_facebook_data(self, *args, **kwargs):
        return {'id': '123'}
    
    @mock.patch('socialregistration.clients.oauth.OAuth2.request')
    @mock.patch('facebook.GraphAPI.request')
    def callback(self, MockFacebook, MockRequest):
        MockRequest.side_effect = get_mock_func(self.get_callback_mock_response)
        MockFacebook.side_effect = get_mock_func(self.get_facebook_data)
        response = self.client.get(self.get_callback_url(), {'code': 'abc'})
        return response
    
    @mock.patch('socialregistration.clients.oauth.OAuth2.request')
    @mock.patch('facebook.GraphAPI.request')
    def setup_callback(self, MockFacebook, MockRequest):
        MockRequest.side_effect = get_mock_func(self.get_setup_callback_mock_response)
        MockFacebook.side_effect = get_mock_func(self.get_facebook_data)
        response = self.client.get(self.get_setup_callback_url())
        return response

class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('socialregistration.contrib.facebook.auth.FacebookAuth' in settings.AUTHENTICATION_BACKENDS)
