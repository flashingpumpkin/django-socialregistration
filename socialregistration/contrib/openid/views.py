from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from socialregistration.contrib.openid.client import OpenIDClient
from socialregistration.contrib.openid.models import OpenIDProfile
from socialregistration.mixins import SocialRegistration
from socialregistration.views import SetupCallback

class OpenIDRedirect(SocialRegistration, View):
    client = OpenIDClient
    
    def post(self, request):
        request.session['next'] = self.get_next(request)

        # We don't want to pass in the whole session object as this might not 
        # be pickleable depending on what session backend one is using. 
        # See issue #73
        client = self.get_client()(dict(request.session.items()),
            request.POST.get('openid_provider'))
        
        request.session[self.get_client().get_session_key()] = client
        
        return HttpResponseRedirect(client.get_redirect_url())

class OpenIDCallback(SocialRegistration, View):
    template_name = 'socialregistration/openid/openid.html'
    profile = OpenIDProfile
    client = OpenIDClient
    
    def get(self, request):
        
        client = request.session[self.get_client().get_session_key()]
        
        client.complete(dict(request.GET.items()), request.get_full_path())
        
        if not client.is_valid():
            if hasattr(client.result, 'message'):
                msg = _("Unfortunately we couldn't validate your identity: %s") % client.result.message
            else:
                msg = _("Unfortunately we couldn't validate your identity")
            return self.render_to_response({'error': msg})
        
        # Save the client back to the session or we're not carrying the result
        # to the next view.
        request.session[self.get_client().get_session_key()] = client
        
        return HttpResponseRedirect(reverse('socialregistration:openid:setup'))

class OpenIDSetup(SetupCallback):
    template_name = 'socialregistration/openid/openid.html'
    profile = OpenIDProfile
    client = OpenIDClient
    
    def get_lookup_kwargs(self, request, client):
        return {'identity': client.get_identity()} 
