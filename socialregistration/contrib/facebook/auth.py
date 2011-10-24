from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.facebook.models import FacebookProfile


class FacebookAuth(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = False
    
    def authenticate(self, uid = None):
        try:
            return FacebookProfile.objects.get(
                uid = uid,
                site = Site.objects.get_current()).user
        except FacebookProfile.DoesNotExist:
            return None
