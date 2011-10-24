from django.core.urlresolvers import reverse
from socialregistration.contrib.foursquare.client import Foursquare
from socialregistration.contrib.foursquare.models import FoursquareProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class FoursquareRedirect(OAuthRedirect):
    client = Foursquare
    template_name = 'socialregistration/foursquare/foursquare.html'

class FoursquareCallback(OAuthCallback):
    client = Foursquare
    template_name = 'socialregistration/foursquare/foursquare.html'
    
    def get_redirect(self):
        return reverse('socialregistration:foursquare:setup')

class FoursquareSetup(SetupCallback):
    client = Foursquare
    profile = FoursquareProfile
    template_name = 'socialregistration/foursquare/foursquare.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'foursquare': client.get_user_info()['id']}
    
