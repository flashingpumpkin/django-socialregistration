from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from oauth2 import Client
import mock
import urllib
import urlparse

class TemplateTagTest(object):
    def get_tag(self):
        """
        Return the appropriate {% load %} and {% button %} tag to try rendering
        as a tuple:
        
                ('facebook', 'facebook_button')

        """
        raise NotImplementedError
    
    def test_tag_renders_correctly(self):
        load, button = self.get_tag()
        
        tpl = """{%% load %s %%}{%% %s %%}""" % (load, button)
        
        self.assertTrue('form' in template.Template(tpl).render(template.Context({'request': None})))
        
        tpl = """{%% load %s %%}{%% %s 'custom/button/url.jpg' %%}""" % (load, button)
        
        self.assertTrue('custom/button/url.jpg' in template.Template(tpl).render(template.Context({'request': None})))


def get_mock_func(func):
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped


class OAuthTest(object):
    def get_redirect_url(self):
        raise NotImplementedError
    
    def get_callback_url(self):
        raise NotImplementedError
    
    def get_callback_setup_url(self):
        raise NotImplementedError
    
    def get_user_info(self):
        raise NotImplementedError
    
    def get_redirect_mock_response(self, *args, **kwargs):
        raise NotImplementedError
    
    def get_callback_mock_response(self, *args, **kwargs):
        raise NotImplementedError
    
    def get_setup_callback_mock_response(self, *args, **kwargs):
        raise NotImplementedError
    
    def create_profile(self):
        raise NotImplementedError
    
    def create_user(self):
        user = User.objects.create(username='alen')
        user.set_password('test')
        user.save()
        return user
    
    def login(self):
        self.client.login(username='alen', password='test')
    
    @mock.patch('oauth2.Client.request')
    def redirect(self, MockRequest):
        MockRequest.side_effect = get_mock_func(self.get_redirect_mock_response)
        response = self.client.post(self.get_redirect_url())
        return response
    
    @mock.patch('oauth2.Client.request')
    def callback(self, MockRequest):
        MockRequest.side_effect = get_mock_func(self.get_callback_mock_response)
        response = self.client.get(self.get_callback_url(), {'oauth_verifier': 'abc'})
        return response
    
    @mock.patch('oauth2.Client.request')
    def setup_callback(self, MockRequest):
        MockRequest.side_effect = get_mock_func(self.get_setup_callback_mock_response)
        response = self.client.get(self.get_setup_callback_url())
        return response
    
    def test_redirect_should_redirect_a_user(self,):
        response = self.redirect()
        self.assertEqual(302, response.status_code, response.content)        
    
    def test_callback_should_redirect_a_user(self):
        self.redirect()
        response = self.callback()
        self.assertEqual(302, response.status_code, response.content)

    def test_setup_callback_should_redirect_a_new_user(self):
        self.redirect()
        self.callback()
        response = self.setup_callback()
        self.assertEqual(302, response.status_code, response.content)
        self.assertEqual(urlparse.urlparse(response['Location']).path, reverse('socialregistration:setup'))
    
    def test_setup_callback_should_redirect_a_logged_in_user(self):
        self.create_user()
        self.login()
        
        self.redirect()
        self.callback()
        response = self.setup_callback()
        self.assertEqual(302, response.status_code, response.content)
        self.assertNotEqual(urlparse.urlparse(response['Location']).path, reverse('socialregistration:setup'))

    def test_connected_user_should_be_logged_in(self):
        user = self.create_user()
        
        self.assertFalse(self.client.session.get('_auth_user_id', False))
        
        self.create_profile(user)
        
        self.redirect()
        self.callback()
        self.setup_callback()

        self.assertEqual(1, self.client.session['_auth_user_id'])

class TestContextProcessors(TestCase):
    def test_request_is_in_context(self):
        self.assertTrue('django.core.context_processors.request' in settings.TEMPLATE_CONTEXT_PROCESSORS)

