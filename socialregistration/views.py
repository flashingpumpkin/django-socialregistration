from django.conf import settings
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import importlib
from django.utils.translation import gettext as _
from django.views.generic.base import View, TemplateResponseMixin
from socialregistration import signals
from socialregistration.forms import UserForm
from socialregistration.models import FacebookProfile, TwitterProfile, \
    LinkedInProfile, OpenIDProfile
from socialregistration.utils import OAuthClient, OAuthTwitter, OpenID, _https, \
    DiscoveryFailure
import uuid


try:
    from django.views.decorators.csrf import csrf_protect
    has_csrf = True
except ImportError:
    has_csrf = False


SESSION_KEY = getattr(settings, 'SOCIALREGISTRATION_SESSION_KEY', 'socialregistration_')
GENERATE_USERNAME = getattr(settings, 'SOCIALREGISTRATION_GENERATE_USERNAME', False)
USERNAME_FUNCTION = getattr(settings, 'SOCIALREGISTRATION_GENERATE_USERNAME_FUNCTION',
    'socialregistration.utils.generate_username')

class ClientMixin(object):
    # The client class we'll be working with
    client = None

    def get_client(self):
        if self.client is None:
            raise AttributeError('`self.client` is `None`')
        return self.client

class ProfileMixin(object):
    # The profile model that we'll be working with
    model = None
        
    def get_model(self):
        if self.model is None:
            raise AttributeError('`self.model` is `None`')
        return self.model

    def create_user(self):
        return User()

    def create_profile(self, user, save=False, **kwargs):
        profile = self.get_model()(user=user, **kwargs)
        
        if save:
            profile.save()
        
        return profile
    
    def get_profile(self, **kwargs):
        self.get_model().objects.get(**kwargs)
        
    def get_or_create_profile(self, user, save=False, **kwargs):
        try:
            profile = self.get_model().objects.get(user=user, **kwargs)
            return profile, False
        except self.get_model().DoesNotExist:
            profile = self.create_profile(user, save=save, **kwargs)
            return profile, True

class SessionMixin(object):
    def store_profile(self, request, profile):
        request.session['%sprofile' % SESSION_KEY] = profile
    
    def store_user(self, request, user):
        request.session['%suser' % SESSION_KEY] = user
    
    def store_client(self, request, client):
        request.session['%sclient' % SESSION_KEY] = client
        
    def get_session_data(self, request):
        user = request.session['%s_user' % SESSION_KEY]
        profile = request.session['%s_profile' % SESSION_KEY]
        client = request.session['%s_client' % SESSION_KEY]
        return user, profile, client
    
    def delete_session_data(self, request):
        del request.session['%s_user' % SESSION_KEY]
        del request.session['%s_profile' % SESSION_KEY]
        del request.session['%s_client' % SESSION_KEY] 

class SignalMixin(object):
    def send_login_signal(self, request, user, profile, client):
        signals.login.send(sender=profile.__class__, user=user,
            profile=profile, client=client, request=request)
        
    def send_connect_signal(self, request, user, profile, client):
        signals.connect.send(sender=profile.__class__, user=user, profile=profile,
            client=client, request=request)

class SocialRegistration(TemplateResponseMixin, View):    
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
        
def Setup(SocialReg):
    template_name = 'socialregistration/setup.html'
    
    def get_username_function(self):
        """
        Return a function that can generate a username. 
        """
        module = '.'.join(USERNAME_FUNCTION.split('.')[:-1])
        function = USERNAME_FUNCTION.split('.')[-1]
        
        module = importlib.import_module(module)
        
        return getattr(module, function)
    
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
            user, profile, client = self.get_models(request)
        except KeyError:
            return self.render_to_response(dict(
                error=_("A social profile is missing from your session.")))
         
        if GENERATE_USERNAME:
            return self.generate_username_and_redirect(user, profile, client)
            
        form = self.form(initial=self.get_initial(request, user, profile, client))
        
        return self.render_to_response(dict(form=form))
        
    def post(self, request):
        try:
            user, profile, client = self.get_models(request)
        except KeyError:
            return self.render_to_response(dict(
                error=_("A social profile is missing from your session.")))
        
        form = self.form(request.POST, initial=self.get_initial(request, user, profile, client))
        
        if not form.is_valid():
            return self.render_to_response(dict(form=form))
        
        (user, profile) = form.save(request)
        
        user = profile.authenticate()
        
        self.send_connect_signal(request, user, profile, client)
        
        self.login(request, user, profile, client)
        
        self.send_login_signal(request, user, profile, client)
        
        self.delete_session_data(request)
        
        return HttpResponseRedirect(self.get_next(request))

class OAuthRedirect(SocialReg):
    def get(self, request):
        request.session['next'] = self.get_next(request)
        client = self.client(request, self.api_key, self.secret_key)
        request.session[self.client.get_session_key()] = client
        return HttpResponseRedirect(client.get_redirect_url())

class OAuthCallback(SocialReg):
    def get(self, request):
        request.session['next'] = self.get_next(request)
        client = request.session[self.client.get_session_key()]
        client.get_auth_token()
        return HttpResponseRedirect(reverse(self.callback_url))


            
            
        
        
def facebook_login(request, template='socialregistration/facebook.html',
    extra_context=dict(), account_inactive_template='socialregistration/account_inactive.html'):
    """
    View to handle the Facebook login
    """

    if not hasattr(request.facebook, 'uid'):
        extra_context.update(dict(error=FB_ERROR))
        return render_to_response(template, extra_context,
            context_instance=RequestContext(request))

    user = authenticate(uid=request.facebook.uid)

    if user is None:
        request.session['socialregistration_user'] = User()
        request.session['socialregistration_profile'] = FacebookProfile(uid=request.facebook.uid)
        request.session['socialregistration_client'] = request.facebook
        request.session['next'] = _get_next(request)
        return HttpResponseRedirect(reverse('socialregistration_setup'))

    if not user.is_active:
        return render_to_response(account_inactive_template, extra_context,
            context_instance=RequestContext(request))

    request.facebook.request = request
    _login(request, user, FacebookProfile.objects.get(user=user), request.facebook)

    return HttpResponseRedirect(_get_next(request))

def facebook_connect(request, template='socialregistration/facebook.html',
    extra_context=dict()):
    """
    View to handle connecting existing django accounts with facebook
    """
    if request.facebook.uid is None or request.user.is_authenticated() is False:
        extra_context.update(dict(error=FB_ERROR))
        return render_to_response(template, extra_context,
            context_instance=RequestContext(request))

    try:
        profile = FacebookProfile.objects.get(uid=request.facebook.uid)
    except FacebookProfile.DoesNotExist:
        profile = FacebookProfile.objects.create(user=request.user,
            uid=request.facebook.uid)
        request.facebook.request = request
        _connect(request.user, profile, request.facebook)

    return HttpResponseRedirect(_get_next(request))

def logout(request, redirect_url=None):
    """
    Logs the user out of django. This is only a wrapper around
    django.contrib.auth.logout. Logging users out of Facebook for instance
    should be done like described in the developer wiki on facebook.
    http://wiki.developers.facebook.com/index.php/Connect/Authorization_Websites#Logging_Out_Users
    """
    auth_logout(request)

    url = redirect_url or getattr(settings, 'LOGOUT_REDIRECT_URL', '/')

    return HttpResponseRedirect(url)

def twitter(request, account_inactive_template='socialregistration/account_inactive.html',
    extra_context=dict(), client_class=None):
    """
    Actually setup/login an account relating to a twitter user after the oauth
    process is finished successfully
    """
    client = client_class(
        request, settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET_KEY,
        settings.TWITTER_REQUEST_TOKEN_URL,
    )

    user_info = client.get_user_info()

    if request.user.is_authenticated():
        # Handling already logged in users connecting their accounts
        try:
            profile = TwitterProfile.objects.get(twitter_id=user_info['id'])
        except TwitterProfile.DoesNotExist: # There can only be one profile!
            profile = TwitterProfile.objects.create(user=request.user, twitter_id=user_info['id'])
            _connect(request.user, profile, client)

        return HttpResponseRedirect(_get_next(request))

    user = authenticate(twitter_id=user_info['id'])

    if user is None:
        profile = TwitterProfile(twitter_id=user_info['id'])
        user = User()
        request.session['socialregistration_profile'] = profile
        request.session['socialregistration_user'] = user
        # Client is not pickleable with the request on it
        client.request = None
        request.session['socialregistration_client'] = client
        request.session['next'] = _get_next(request)
        return HttpResponseRedirect(reverse('socialregistration_setup'))

    if not user.is_active:
        return render_to_response(
            account_inactive_template,
            extra_context,
            context_instance=RequestContext(request)
        )

    _login(request, user, TwitterProfile.objects.get(user=user), client)

    return HttpResponseRedirect(_get_next(request))


def linkedin(request, account_inactive_template='socialregistration/account_inactive.html',
    extra_context=dict(), client_class=None):
    """
    Actually setup/login an account relating to a linkedin user after the oauth
    process is finished successfully
    """
    client = client_class(
        request, settings.LINKEDIN_CONSUMER_KEY,
        settings.LINKEDIN_CONSUMER_SECRET_KEY,
        settings.LINKEDIN_REQUEST_TOKEN_URL,
    )

    user_info = client.get_user_info()

    if request.user.is_authenticated():
        # Handling already logged in users connecting their accounts
        try:
            profile = LinkedInProfile.objects.get(linkedin_id=user_info['id'])
        except LinkedInProfile.DoesNotExist: # There can only be one profile!
            profile = LinkedInProfile.objects.create(user=request.user, linkedin_id=user_info['id'])
            _connect(request.user, profile, client)

        return HttpResponseRedirect(_get_next(request))

    user = authenticate(linkedin_id=user_info['id'])

    if user is None:
        profile = LinkedInProfile(linkedin_id=user_info['id'])
        user = User()
        request.session['socialregistration_profile'] = profile
        request.session['socialregistration_user'] = user
        # Client is not pickleable with the request on it
        client.request = None
        request.session['socialregistration_client'] = client
        request.session['next'] = _get_next(request)
        return HttpResponseRedirect(reverse('socialregistration_setup'))

    if not user.is_active:
        return render_to_response(
            account_inactive_template,
            extra_context,
            context_instance=RequestContext(request)
        )

    _login(request, user, LinkedInProfile.objects.get(user=user), client)

    return HttpResponseRedirect(_get_next(request))

def oauth_redirect(request, consumer_key=None, secret_key=None,
    request_token_url=None, access_token_url=None, authorization_url=None,
    callback_url=None, parameters=None, client_class=None):
    """
    View to handle the OAuth based authentication redirect to the service provider
    """
    request.session['next'] = _get_next(request)
    client = client_class(request, consumer_key, secret_key,
        request_token_url, access_token_url, authorization_url, callback_url, parameters)
    return client.get_redirect()

def oauth_callback(request, consumer_key=None, secret_key=None,
    request_token_url=None, access_token_url=None, authorization_url=None,
    callback_url=None, template='socialregistration/oauthcallback.html',
    extra_context=dict(), parameters=None, client_class=None):
    """
    View to handle final steps of OAuth based authentication where the user
    gets redirected back to from the service provider
    """
    client = client_class(request, consumer_key, secret_key, request_token_url,
        access_token_url, authorization_url, callback_url, parameters)

    extra_context.update(dict(oauth_client=client))
    if not client.is_valid():
        return render_to_response(
            template, extra_context, context_instance=RequestContext(request)
        )

    # We're redirecting to the setup view for this oauth service
    return HttpResponseRedirect(reverse(client.callback_url))

def openid_redirect(request, client_class=None):
    """
    Redirect the user to the openid provider
    """
    request.session['next'] = _get_next(request)
    request.session['openid_provider'] = request.GET.get('openid_provider')

    client = client_class(
        request,
        'http%s://%s%s' % (
            _https(),
            Site.objects.get_current().domain,
            reverse('openid_callback')
        ),
        request.GET.get('openid_provider')
    )
    try:
        return client.get_redirect()
    except DiscoveryFailure:
        request.session['openid_error'] = True
        return HttpResponseRedirect(settings.LOGIN_URL)

def openid_callback(request, template='socialregistration/openid.html',
    extra_context=dict(), account_inactive_template='socialregistration/account_inactive.html',
    client_class=None):
    """
    Catches the user when he's redirected back from the provider to our site
    """
    client = client_class(
        request,
        'http%s://%s%s' % (
            _https(),
            Site.objects.get_current().domain,
            reverse('openid_callback')
        ),
        request.session.get('openid_provider')
    )

    if client.is_valid():
        identity = client.result.identity_url
        if request.user.is_authenticated():
            # Handling already logged in users just connecting their accounts
            try:
                profile = OpenIDProfile.objects.get(identity=identity)
            except OpenIDProfile.DoesNotExist: # There can only be one profile with the same identity
                profile = OpenIDProfile.objects.create(user=request.user,
                    identity=identity)
                _connect(request.user, profile, client)

            return HttpResponseRedirect(_get_next(request))

        user = authenticate(identity=identity)
        if user is None:
            request.session['socialregistration_user'] = User()
            request.session['socialregistration_profile'] = OpenIDProfile(
                identity=identity
            )
            # Client is not pickleable with the request on it
            client.request = None
            request.session['socialregistration_client'] = client
            return HttpResponseRedirect(reverse('socialregistration_setup'))

        if not user.is_active:
            return render_to_response(
                account_inactive_template,
                extra_context,
                context_instance=RequestContext(request)
            )

        _login(request, user, OpenIDProfile.objects.get(user=user), client)
        return HttpResponseRedirect(_get_next(request))

    return render_to_response(
        template,
        dict(),
        context_instance=RequestContext(request)
    )
