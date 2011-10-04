from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.tumblr.models import TumblrProfile


class TumblrAuth(ModelBackend):
    def authenticate(self, tumblr=None):
        try:
            return TumblrProfile.objects.get(
                tumblr=tumblr,
                site=Site.objects.get_current()
            ).user
        except TumblrProfile.DoesNotExist:
            return None
