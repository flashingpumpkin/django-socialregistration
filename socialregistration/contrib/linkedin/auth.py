from django.contrib.sites.models import Site
from socialregistration.auth import Auth
from socialregistration.contrib.linkedin.models import LinkedInProfile


class LinkedInAuth(Auth):
    def authenticate(self, linkedin_id=None):
        try:
            return LinkedInProfile.objects.get(
                linkedin_id=linkedin_id,
                site=Site.objects.get_current()
            ).user
        except LinkedInProfile.DoesNotExist:
            return None
