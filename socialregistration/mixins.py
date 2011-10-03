from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import importlib
from django.views.generic.base import TemplateResponseMixin
from socialregistration import signals

SESSION_KEY = getattr(settings, 'SOCIALREGISTRATION_SESSION_KEY', 'socialregistration:')

class CommonMixin(TemplateResponseMixin):
    
    def import_attribute(self, path):
        module = '.'.join(path.split('.')[:-1])
        function = path.split('.')[-1]
        
        module = importlib.import_module(module)
        return getattr(module, function)
    
    def get_next(self, request):
        """
        Returns a url to redirect to after the login
        """
        if 'next' in request.session:
            next = request.session['next']
            del request.session['next']
            return next
        elif 'next' in request.GET:
            return request.GET.get('next')
        elif 'next' in request.POST:
            return request.POST.get('next')
        else:
            return getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def authenticate(self, **kwargs):
        return authenticate(**kwargs)
    
    def login(self, request, user):
        return login(request, user)
    
    def inactive_response(self):
        return self.render_to_response({
            'error': _("This user account is marked as inactive.")})
            
    def redirect(self, request):
        return HttpResponseRedirect(self.get_next(request))

class ClientMixin(object):
    # The client class we'll be working with
    client = None

    def get_client(self):
        if self.client is None:
            raise AttributeError('`self.client` is `None`')
        return self.client

class ProfileMixin(object):
    # The profile model that we'll be working with
    profile = None
        
    def get_model(self):
        if self.profile is None:
            raise AttributeError('`self.profile` is `None`')
        return self.profile

    def create_user(self):
        return User()

    def create_profile(self, user, save=False, **kwargs):
        profile = self.get_model()(user=user, **kwargs)
        
        if save:
            profile.save()
        
        return profile
    
    def get_profile(self, **kwargs):
        return self.get_model().objects.get(**kwargs)
        
    def get_or_create_profile(self, user, save=False, **kwargs):
        try:
            profile = self.get_model().objects.get(user=user, **kwargs)
            return profile, False
        except self.get_model().DoesNotExist:
            profile = self.create_profile(user, save=save, **kwargs)
            return profile, True
    
    def get_lookup_kwargs(self, request, client):
        raise NotImplementedError

class SessionMixin(object):
    def store_profile(self, request, profile):
        request.session['%sprofile' % SESSION_KEY] = profile
    
    def store_user(self, request, user):
        request.session['%suser' % SESSION_KEY] = user
    
    def store_client(self, request, client):
        request.session['%sclient' % SESSION_KEY] = client
        
    def get_session_data(self, request):
        user = request.session['%suser' % SESSION_KEY]
        profile = request.session['%sprofile' % SESSION_KEY]
        client = request.session['%sclient' % SESSION_KEY]
        return user, profile, client
    
    def delete_session_data(self, request):
        del request.session['%suser' % SESSION_KEY]
        del request.session['%sprofile' % SESSION_KEY]
        del request.session['%sclient' % SESSION_KEY] 

class SignalMixin(object):
    def send_login_signal(self, request, user, profile, client):
        signals.login.send(sender=profile.__class__, user=user,
            profile=profile, client=client, request=request)
        
    def send_connect_signal(self, request, user, profile, client):
        signals.connect.send(sender=profile.__class__, user=user, profile=profile,
            client=client, request=request)

class SocialRegistration(CommonMixin, ClientMixin, ProfileMixin, SessionMixin,
    SignalMixin):
    pass
