from django import template
from django.conf import settings
from django.test import TestCase


class TestTemplateTag(TestCase):
    def test_tag_renders_correctly(self):
        render = lambda tpl: template.Template(
            tpl).render(template.Context({'request':None}))
        
        tpl = """{% load openid %}{% openid_form %}"""
       
        rendered = render(tpl)

        self.assertTrue('form' in rendered)
        
        tpl = """
	{% load openid %}
	{% openid_form "https://www.google.com/accounts/o8/id" "image/for/google.jpg" %}
	"""
        
        rendered = render(tpl)

        self.assertTrue('https://www.google.com/accounts/o8/id' in rendered)

        self.assertTrue('image/for/google.jpg' in rendered)



class TestAuthenticationBackend(TestCase):
    def test_authentication_backend_should_be_configured_in_settings(self):
        self.assertTrue('socialregistration.contrib.openid.auth.OpenIDAuth' in settings.AUTHENTICATION_BACKENDS)
