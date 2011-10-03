from django.contrib.sites.models import Site
from socialregistration.contrib.github.models import GithubProfile
from django.contrib.auth.backends import ModelBackend


class GithubAuth(ModelBackend):
    def authenticate(self, github = None):
        try:
            return GithubProfile.objects.get(
                github = github,
                site = Site.objects.get_current()).user
        except GithubProfile.DoesNotExist:
            return None
