from django import template
from django.conf import settings
from django.test import TestCase


class TestTemplateTag(TestCase):
    def test_tag_renders_correctly(self):
        tpl = """{% load openid %}{% openid_form %}"""
       
        self.assertTrue('form' in template.Template(tpl).render(template.Context({'request': None})))
        
        tpl = """{% load openid %}{% openid_form "https://www.google.com/accounts/o8/id" "image/for/google.jpg" %}"""
        
        self.assertTrue('https://www.google.com/accounts/o8/id' in template.Template(tpl).render(template.Context({'request': None})))
        self.assertTrue('image/for/google.jpg' in template.Template(tpl).render(template.Context({'request': None})))



class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('socialregistration.contrib.openid.auth.OpenIDAuth' in settings.AUTHENTICATION_BACKENDS)
