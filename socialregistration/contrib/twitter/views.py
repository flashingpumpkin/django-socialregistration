from django.core.urlresolvers import reverse
from socialregistration.contrib.twitter.client import Twitter
from socialregistration.contrib.twitter.models import TwitterProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class TwitterRedirect(OAuthRedirect):
    client = Twitter
    template_name = 'socialregistration/twitter/twitter.html'

class TwitterCallback(OAuthCallback):
    client = Twitter
    template_name = 'socialregistration/twitter/twitter.html'
    
    def get_redirect(self):
        return reverse('socialregistration:twitter:setup')

class TwitterSetup(SetupCallback):
    client = Twitter
    profile = TwitterProfile
    template_name = 'socialregistration/twitter/twitter.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'twitter_id': client.get_user_info()['user_id']}
    
