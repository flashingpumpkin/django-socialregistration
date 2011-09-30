from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _
from socialregistration.contrib.openid.client import OpenIDClient
from socialregistration.contrib.openid.models import OpenIDProfile
from socialregistration.mixins import SocialRegistration

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
    model = OpenIDProfile
    client = OpenIDClient
    
    def get(self, request):
        
        client = request.session[self.get_client().get_session_key()]
        
        client.complete(dict(request.GET.items()), request.get_full_path())
        
        if not client.is_valid():
            return self.render_to_response(dict(
                error=_("Unfortunately we couldn't validate your identity: %s") % client.result.message))
        
        # Logged in user connecting an account
        if request.user.is_authenticated():
            profile, created = self.get_or_create_profile(user=request.user,
                identity=client.get_identity(), save=True)
            
            # Profile already existed - just redirect where the user wanted to
            # go
            if not created:
                return self.redirect(request)
            
            # Profile didn't exist - store the profile, send the connect signal
            # and redirect where the user wanted to go
            self.send_connect_signal(request, request.user, profile, client)
            
            return self.redirect(request)

        # Logged out user - let's see if we've got the identity saved already.
        # If so - just log the user in. If not, create profile and redirect
        # to the setup view        
        user = self.authenticate(identity=client.get_identity())
        
        if user is None:
            user = self.create_user()
            profile = self.create_profile(user, identity=client.get_identity())
            
            self.store_user(request, user)
            self.store_profile(request, profile)
            self.store_client(request, client)
            
            return HttpResponseRedirect(reverse('socialregistration:setup'))

        if not user.is_active:
            return self.inactive_response()
        
        self.login(request, user)
        
        profile = self.get_profile(user=user, identity=client.get_identity())
        
        self.send_login_signal(request, user, profile, client)
        
        return self.redirect(request)
        
