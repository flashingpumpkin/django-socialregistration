from django.core.urlresolvers import reverse
from socialregistration.contrib.github.client import Github
from socialregistration.contrib.github.models import GithubProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class GithubRedirect(OAuthRedirect):
    client = Github
    template_name = 'socialregistration/github/github.html'

class GithubCallback(OAuthCallback):
    client = Github
    template_name = 'socialregistration/github/github.html'
    
    def get_redirect(self):
        return reverse('socialregistration:github:setup')

class GithubSetup(SetupCallback):
    client = Github
    profile = GithubProfile
    template_name = 'socialregistration/github/github.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'github': client.get_user_info()['login']}
    
