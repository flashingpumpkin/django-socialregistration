from django.core.urlresolvers import reverse
from socialregistration.contrib.google.client import Google
from socialregistration.contrib.google.models import GoogleProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class GoogleRedirect(OAuthRedirect):
    client = Google
    template_name = 'socialregistration/google/google.html'

class GoogleCallback(OAuthCallback):
    client = Google
    template_name = 'socialregistration/google/google.html'
    
    def get_redirect(self):
        return reverse('socialregistration:google:setup')

class GoogleSetup(SetupCallback):
    client = Google
    profile = GoogleProfile
    template_name = 'socialregistration/google/google.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'google_id': client.get_user_info()['id']}
    
