from django.conf import settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _
from socialregistration.clients.oauth import OAuthError
from socialregistration.mixins import SocialRegistration

GENERATE_USERNAME = getattr(settings, 'SOCIALREGISTRATION_GENERATE_USERNAME', False)

USERNAME_FUNCTION = getattr(settings, 'SOCIALREGISTRATION_GENERATE_USERNAME_FUNCTION',
    'socialregistration.utils.generate_username')

FORM_CLASS = getattr(settings, 'SOCIALREGISTRATION_SETUP_FORM',
    'socialregistration.forms.UserForm')


class Setup(SocialRegistration, View):
    template_name = 'socialregistration/setup.html'

    def get_form(self):
        return self.import_attribute(FORM_CLASS)
    
    def get_username_function(self):
        """
        Return a function that can generate a username. 
        """
        return self.import_attribute(USERNAME_FUNCTION)
    
    def get_initial_data(self, request, user, profile, client):
        """
        Fetch some initial data for the user setup form.
        """
        return {}

    def generate_username_and_redirect(self, request, user, profile, client):
        """
        Generate a username, save the profile, login and redirect to the next
        page.
        """
        func = self.get_username_function()
        
        user.username = func(user, profile, client)
        user.save()
        
        profile.user = user
        profile.save()
        
        user = profile.authenticate()
        
        self.send_connect_signal(request, user, profile, client)
        
        self.login(request, user)
        
        self.send_login_signal(request, user, profile, client)
        
        self.delete_session_data(request)
        
        return HttpResponseRedirect(self.get_next(request))
        
    def get(self, request):
        try:
            user, profile, client = self.get_session_data(request)
        except KeyError:
            return self.render_to_response(dict(
                error=_("A social profile is missing from your session.")))
         
        if GENERATE_USERNAME:
            return self.generate_username_and_redirect(user, profile, client)
            
        form = self.get_form()(initial=self.get_initial_data(request, user, profile, client))
        
        return self.render_to_response(dict(form=form))
        
    def post(self, request):
        try:
            user, profile, client = self.get_session_data(request)
        except KeyError:
            return self.render_to_response(dict(
                error=_("A social profile is missing from your session.")))
        
        form = self.get_form()(request.POST, request.FILES,
            initial=self.get_initial_data(request, user, profile, client))
        
        if not form.is_valid():
            return self.render_to_response(dict(form=form))
        
        user, profile = form.save(request, user, profile, client)
        
        user = profile.authenticate()
        
        self.send_connect_signal(request, user, profile, client)
        
        self.login(request, user)
        
        self.send_login_signal(request, user, profile, client)
        
        self.delete_session_data(request)
        
        return HttpResponseRedirect(self.get_next(request))


class Logout(View):
    """
    Logs the user out of Django. This is only a wrapper around 
    `django.contrib.auth.logout`. Logging users out of third party apps will
    *not* happen here. 
    """
    def get(self, request):
        logout(request)
        url = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')
        return HttpResponseRedirect(url)


class OAuthRedirect(SocialRegistration, View):
    client = None
    template_name = None
    
    def post(self, request):
        request.session['next'] = self.get_next(request)
        client = self.get_client()()
        request.session[self.get_client().get_session_key()] = client
        try:
            return HttpResponseRedirect(client.get_redirect_url())
        except OAuthError, error:
            return self.render_to_response({'error': error})


class OAuthCallback(SocialRegistration, View):
    def get_redirect(self):
        raise NotImplementedError
    
    def get(self, request):
        client = request.session[self.get_client().get_session_key()]
        try:
            client.complete(dict(request.GET.items()))
            request.session[self.get_client().get_session_key()] = client
            return HttpResponseRedirect(self.get_redirect())
        except OAuthError, error:
            return self.render_to_response({'error': error})

class SetupCallback(SocialRegistration, View):    
    def get(self, request):
        client = request.session[self.get_client().get_session_key()]
        
        lookup_kwargs = self.get_lookup_kwargs(request, client)

        # Logged in user connecting an account
        if request.user.is_authenticated():
            profile, created = self.get_or_create_profile(request.user,
                save=True, **lookup_kwargs)
            
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
        user = self.authenticate(**lookup_kwargs)
        
        if user is None:
            user = self.create_user()
            profile = self.create_profile(user, **lookup_kwargs)
            
            self.store_user(request, user)
            self.store_profile(request, profile)
            self.store_client(request, client)
            
            return HttpResponseRedirect(reverse('socialregistration:setup'))

        if not user.is_active:
            return self.inactive_response()
        
        self.login(request, user)
        
        profile = self.get_profile(user=user, **lookup_kwargs)
        
        self.send_login_signal(request, user, profile, client)
        
        return self.redirect(request)
