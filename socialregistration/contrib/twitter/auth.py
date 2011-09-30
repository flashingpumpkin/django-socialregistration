from django.contrib.sites.models import Site
from socialregistration.auth import Auth
from socialregistration.contrib.twitter.models import TwitterProfile


class TwitterAuth(Auth):
    def authenticate(self, twitter_id=None):
        try:
            return TwitterProfile.objects.get(
                twitter_id=twitter_id,
                site=Site.objects.get_current()
            ).user
        except TwitterProfile.DoesNotExist:
            return None
