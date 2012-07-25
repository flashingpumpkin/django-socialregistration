from django.core.urlresolvers import reverse
from socialregistration.contrib.instagram.client import Instagram
from socialregistration.contrib.instagram.models import InstagramProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class InstagramRedirect(OAuthRedirect):
    client = Instagram
    template_name = 'socialregistration/instagram/instagram.html'

class InstagramCallback(OAuthCallback):
    client = Instagram
    template_name = 'socialregistration/instagram/instagram.html'
    
    def get_redirect(self):
        return reverse('socialregistration:instagram:setup')

class InstagramSetup(SetupCallback):
    client = Instagram
    profile = InstagramProfile
    template_name = 'socialregistration/instagram/instagram.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'instagram': client.get_user_info()}
    
