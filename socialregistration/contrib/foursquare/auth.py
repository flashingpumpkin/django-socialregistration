from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.foursquare.models import FoursquareProfile

class FoursquareAuth(ModelBackend):
    def authenticate(self, foursquare=None):
        try:
            return FoursquareProfile.objects.get(
                foursquare=foursquare,
                site=Site.objects.get_current()).user
        except FoursquareProfile.DoesNotExist:
            return None
