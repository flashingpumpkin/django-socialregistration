from django.contrib.sites.models import Site
from socialregistration.auth import Auth
from socialregistration.contrib.facebook.models import FacebookProfile


class FacebookAuth(Auth):
    def authenticate(self, uid = None):
        try:
            return FacebookProfile.objects.get(
                uid = uid,
                site = Site.objects.get_current()).user
        except FacebookProfile.DoesNotExist:
            return None
