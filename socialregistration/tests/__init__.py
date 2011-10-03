from django.core.urlresolvers import reverse
from django.test import TestCase
from socialregistration.tests.templatetags import *

class SocialRegistrationTestCase(TestCase):
    def url(self, name, *args):
        return reverse(name, args=args)

        