from django.core.urlresolvers import reverse
from socialregistration.contrib.tumblr.client import Tumblr
from socialregistration.contrib.tumblr.models import TumblrProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class TumblrRedirect(OAuthRedirect):
    client = Tumblr
    template_name = 'socialregistration/tumblr/tumblr.html'

class TumblrCallback(OAuthCallback):
    client = Tumblr
    template_name = 'socialregistration/tumblr/tumblr.html'
    
    def get_redirect(self):
        return reverse('socialregistration:tumblr:setup')

class TumblrSetup(SetupCallback):
    client = Tumblr
    profile = TumblrProfile
    template_name = 'socialregistration/tumblr/tumblr.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'tumblr': client.get_user_info()['name']}
    
