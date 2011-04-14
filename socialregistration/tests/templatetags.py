from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.test import TestCase

class MockHttpRequest(HttpRequest):

    def __init__(self, *args, **kwargs):
        super(MockHttpRequest, self).__init__(*args, **kwargs)

        self.session = {}

class SocialRegistrationTemplateTagTests(TestCase):

    def setUp(self):
        # set up a site object in case the current site ID doesn't exist
        site = Site.objects.get_or_create(pk=settings.SITE_ID)

    def render(self, template_string, context={}):
        """Return the rendered string or the exception raised while rendering."""
        try:
            t = template.Template(template_string)
            c = template.Context(context)
            return t.render(c)
        except Exception, e:
            return e

    def test_open_id_error(self):
        request = MockHttpRequest()

        request.session['openid_error'] = True
        request.session['openid_provider'] = 'whizzle'

        template = """{% load socialregistration_tags %}{% open_id_errors request %}{{ openid_error }}|{{ openid_provider }}"""
        result = self.render(template, {'request': request,})
        self.assertEqual(result, u'True|whizzle')

        # but accessing it a second time, the error should have cleared.
        template = """{% load socialregistration_tags %}{% open_id_errors request %}{{ openid_error }}|{{ openid_provider }}"""
        result = self.render(template, {'request': request,})
        self.assertEqual(result, u'False|')

