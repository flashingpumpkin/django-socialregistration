from django.contrib.sites.models import Site
from socialregistration.contrib.google.models import GoogleProfile
from django.contrib.auth.backends import ModelBackend


class GoogleAuth(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = False

    def authenticate(self, **kwargs):
        uid = kwargs.get('google_id')
        try:
            return GoogleProfile.objects.get(
                google_id = uid,
                site = Site.objects.get_current()).user
        except GoogleProfile.DoesNotExist:
            return None
