from socialregistration.auth import Auth
from django.contrib.sites.models import Site


from socialregistration.contrib.openid.models import OpenIDProfile

class OpenIDAuth(Auth):
    def authenticate(self, identity=None):
        try:
            return OpenIDProfile.objects.get(
                identity=identity,
                site=Site.objects.get_current()
            ).user
        except OpenIDProfile.DoesNotExist:
            return None
