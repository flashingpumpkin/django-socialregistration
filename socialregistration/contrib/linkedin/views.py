from django.core.urlresolvers import reverse
from socialregistration.contrib.linkedin.client import LinkedIn
from socialregistration.contrib.linkedin.models import LinkedInProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class LinkedInRedirect(OAuthRedirect):
    client = LinkedIn
    template_name = 'socialregistration/linkedin/linkedin.html'

class LinkedInCallback(OAuthCallback):
    client = LinkedIn
    template_name = 'socialregistration/linkedin/linkedin.html'
    
    def get_redirect(self):
        return reverse('socialregistration:linkedin:setup')

class LinkedInSetup(SetupCallback):
    client = LinkedIn
    profile = LinkedInProfile
    template_name = 'socialregistration/linkedin/linkedin.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'linkedin_id': client.get_user_info()['id']}
    
