from django.contrib.sites.models import Site
from socialregistration.contrib.instagram.models import InstagramProfile
from django.contrib.auth.backends import ModelBackend


class InstagramAuth(ModelBackend):
    def authenticate(self, instagram = None):
        try:
            return InstagramProfile.objects.get(
                instagram = instagram,
                site = Site.objects.get_current()).user
        except InstagramProfile.DoesNotExist:
            return None
