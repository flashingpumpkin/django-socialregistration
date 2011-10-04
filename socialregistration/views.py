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

INITAL_DATA_FUNCTION = getattr(settings, 'SOCIALREGISTRATION_INITIAL_DATA_FUNCTION',
    None)


class Setup(SocialRegistration, View):
    """
    Setup view to create new Django users from OAuth / OpenID providers.
    """
    template_name = 'socialregistration/setup.html'

    def get_form(self):
        """
        If `SOCIALREGISTRATION_GENERATE_USERNAME` is not set, this method will
        return the form to be used when signing up a new user. The form can 
        be controlled either by subclassing this view and overriding the URL
        or by modifying the `SOCIALREGISTRATION_SETUP_FORM` setting.
        """
        return self.import_attribute(FORM_CLASS)
    
    def get_username_function(self):
        """
        Return a function that can generate a username. The function can be 
        changed by modifying the `SOCIALREGISTRATION_GENERATE_USERNAME_FUNCTION`.
        """
        return self.import_attribute(USERNAME_FUNCTION)
    
    def get_initial_data(self, request, user, profile, client):
        """
        Return initial data for the `SOCIALREGISTRATION_SETUP_FORM`. This 
        function looks if `SOCIALREGISTRATION_INITIAL_DATA_FUNCTION` is set and if so
        calls the configured function with four parameters:
        
        * `request` 
            The current request
        * `user`
            The newly created user - not saved yet
        * `profile` 
            The social profile - not saved yet
        * `client` 
            The API client that can be used to fetch data remotely
        """
        if INITAL_DATA_FUNCTION:
            func = self.import_attribute(INITAL_DATA_FUNCTION)
            return func(request, user, profile, client)
        return {}

    def generate_username_and_redirect(self, request, user, profile, client):
        """
        This method is called when `SOCIALREGISTRATION_GENERATE_USERNAME` is
        set. It skips displaying a setup form, saves the user and profile,
        sends off the connect and login signals and the nredirects the user
        to the correct place.
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
        """
        Callback to all newly signed up users. When 
        `SOCIALREGISTRATION_GENERATE_USERNAME` is *not* set, this displays
        a configured form for user creation. The default form includes a 
        username and email field. 
        """
        try:
            user, profile, client = self.get_session_data(request)
        except KeyError:
            return self.render_to_response(dict(
                error=_("Social profile is missing from your session.")))
         
        if GENERATE_USERNAME:
            return self.generate_username_and_redirect(request, user, profile, client)
            
        form = self.get_form()(initial=self.get_initial_data(request, user, profile, client))
        
        return self.render_to_response(dict(form=form))
        
    def post(self, request):
        """
        Callback to the user creation form. This saves the user and the profile,
        logs the user in and sends the connect and login signals before redirecting
        to the correct place.
        """
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
    """
    Base class for both OAuth{1,2} redirect views.
    """
    
    # The OAuth{1,2} client to be used
    client = None
    
    # The template to render in case of errors
    template_name = None
    
    def post(self, request):
        """
        Create a client, store it in the user's session and redirect the user
        to the API provider to authorize our app and permissions.
        """
        request.session['next'] = self.get_next(request)
        client = self.get_client()()
        request.session[self.get_client().get_session_key()] = client
        try:
            return HttpResponseRedirect(client.get_redirect_url())
        except OAuthError, error:
            return self.render_to_response({'error': error})


class OAuthCallback(SocialRegistration, View):
    """
    Base class for OAuth{1,2} callback views.
    """
    
    # The OAuth{1,2} client to be used
    client = None
    
    # The template to render in case of errors
    template_name = None
    
    def get_redirect(self):
        """
        Return a URL where we'll deal with the current service's specific 
        signup requirements.
        """
        raise NotImplementedError
    
    def get(self, request):
        """
        Called after a user authorizes (or not) our application with the API
        provider. In case authorization was granted, we're redirecting the 
        user one step further where we'll deal with the API profile setup.
        """
        client = request.session[self.get_client().get_session_key()]
        try:
            client.complete(dict(request.GET.items()))
            request.session[self.get_client().get_session_key()] = client
            return HttpResponseRedirect(self.get_redirect())
        except OAuthError, error:
            return self.render_to_response({'error': error})

class SetupCallback(SocialRegistration, View):
    """
    Base class for OAuth{1,2} profile setup.
    """
    
    def get(self, request):
        """
        Called after authorization was granted and the OAuth{1,2} flow 
        successfully completed. 
        
        We're checking if the user is already logged in and has a profile or not.
        """
        
        client = request.session[self.get_client().get_session_key()]
        
        # Get the lookup dictionary to find the user's profile
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
        
        # No user existing - create a new one and redirect to the final setup view
        if user is None:
            user = self.create_user()
            profile = self.create_profile(user, **lookup_kwargs)
            
            self.store_user(request, user)
            self.store_profile(request, profile)
            self.store_client(request, client)
            
            return HttpResponseRedirect(reverse('socialregistration:setup'))

        # Inactive user - displaying an error message.
        if not user.is_active:
            return self.inactive_response()
        
        # Active user with existing profile: login, send signal and redirect
        self.login(request, user)
        
        profile = self.get_profile(user=user, **lookup_kwargs)
        
        self.send_login_signal(request, user, profile, client)
        
        return self.redirect(request)
