from django.contrib.sites.models import Site
from socialregistration.auth import Auth
from socialregistration.contrib.github.models import GithubProfile

class GithubAuth(Auth):
    def authenticate(self, github = None):
        try:
            return GithubProfile.objects.get(
                github = github,
                site = Site.objects.get_current()).user
        except GithubProfile.DoesNotExist:
            return None
