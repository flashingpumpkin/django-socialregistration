from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from socialregistration.contrib.linkedin.models import LinkedInProfile


class LinkedInAuth(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = False
    
    def authenticate(self, linkedin_id=None):
        try:
            return LinkedInProfile.objects.get(
                linkedin_id=linkedin_id,
                site=Site.objects.get_current()
            ).user
        except LinkedInProfile.DoesNotExist:
            return None
