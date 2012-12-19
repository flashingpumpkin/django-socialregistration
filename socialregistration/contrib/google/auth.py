from django.contrib.sites.models import Site
from socialregistration.contrib.google.models import GoogleProfile
from django.contrib.auth.backends import ModelBackend


class GoogleAuth(ModelBackend):
    def authenticate(self, id = None):
        try:
            return GoogleProfile.objects.get(
                google_id = id,
                site = Site.objects.get_current()).user
        except GoogleProfile.DoesNotExist:
            return None
