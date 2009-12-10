"""
Created on 22.09.2009

@author: alen
"""
import uuid
from oauth import oauth

from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils.translation import gettext as _
from django.utils.hashcompat import md5_constructor
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.models import Site

from socialregistration.forms import UserForm
from socialregistration.utils import (OAuthClient, OAuthTwitter, OAuthFriendFeed,
    OpenID)
from socialregistration.models import FacebookProfile, TwitterProfile, OpenIDProfile


FB_ERROR = _('We couldn\'t validate your Facebook credentials')

def _get_next(request):
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

def setup(request, template='socialregistration/setup.html',
    form_class=UserForm, extra_context=dict()):
    """
    Setup view to create a username & set email address after authentication
    """
    if not getattr(settings, 'SOCIAL_GENERATE_USERNAME', False):
        # User can pick own username
        if not request.method == "POST":
            form = form_class(
                request.session['socialregistration_user'],
                request.session['socialregistration_profile'],
            )
        else:
            form = form_class(
                request.session['socialregistration_user'],
                request.session['socialregistration_profile'],
                request.POST
            )
            if form.is_valid():
                form.save()
                user = form.profile.authenticate()
                login(request, user)
                del request.session['socialregistration_user']
                del request.session['socialregistration_profile']
                return HttpResponseRedirect(_get_next(request))
    
        extra_context.update(dict(form=form))
    
        return render_to_response(
            template,
            extra_context,
            context_instance=RequestContext(request)
        )
    else:
        # Generate user and profile
        user = request.session['socialregistration_user']
        user.username = str(uuid.uuid4())[:30]
        user.save()
        
        profile = request.session['socialregistration_profile']
        profile.user = user
        profile.save()

        # Authenticate and login
        user = profile.authenticate()
        login(request, user)
        
        # Clear & Redirect
        del request.session['socialregistration_user']
        del request.session['socialregistration_profile']
        return HttpResponseRedirect(getattr(settings, 'LOGIN_REDIRECT_URL', _get_next(request)))
        

def facebook_login(request, template='socialregistration/facebook.html',
    extra_context=dict()):
    """
    View to handle the Facebook login 
    """
    if not request.facebook.check_session(request):
        extra_context.update(
            dict(error=FB_ERROR)
        )
        return render_to_response(
            template, extra_context, context_instance=RequestContext(request)
        )
    
    user = authenticate(uid=request.facebook.uid)
    
    if user is None:
        request.session['socialregistration_user'] = User()
        fb_profile = request.facebook.users.getInfo([request.facebook.uid], ['name', 'pic_square'])[0]
        request.session['socialregistration_profile'] = FacebookProfile(
            uid=request.facebook.uid,
            username=fb_profile['name'],
            avatar=fb_profile['pic_square']
            )
        request.session['next'] = _get_next(request)

        return HttpResponseRedirect(reverse('socialregistration_setup'))

    login(request, user)
    
    return HttpResponseRedirect(getattr(settings, 'LOGIN_REDIRECT_URL', _get_next(request)))

def facebook_connect(request, template='socialregistration/facebook.html',
    extra_context=dict()):
    """
    View to handle connecting existing accounts with facebook
    """
    if not request.facebook.check_session(request) \
        or not request.user.is_authenticated():
        extra_context.update(
            dict(error=FB_ERROR)
        )
        return render_to_response(
            template,
            extra_context,
            context_dict=RequestContext(request)
        )
    
    profile, created = FacebookProfile.objects.get_or_create(
        user=request.user, uid=request.facebook.uid
    )
    
    return HttpResponseRedirect(_get_next(request))

def facebook_logout(request, redirect_url=None):
    """
    Logs the user out of facebook and django.
    """
    logout(request)
    if getattr(request,'facebook',False):
        request.facebook.session_key = None
        request.facebook.uid = None
    url = getattr(settings,'LOGOUT_REDIRECT_URL',redirect_url) or '/'

    return HttpResponseRedirect(url)

def twitter(request):
    """
    Actually setup/login an account relating to a twitter user after the oauth 
    process is finished successfully
    """
    client = OAuthTwitter(
        request, settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET_KEY,
        settings.TWITTER_REQUEST_TOKEN_URL,
    )
    
    user_info = client.get_user_info()

    user = authenticate(twitter_id=user_info['id'])
    
    if user is None:
        profile = TwitterProfile(twitter_id=user_info['id'],
                                 username=user_info['screen_name'],
                                 avatar=user_info['profile_image_url'])
        user = User()
        request.session['socialregistration_profile'] = profile
        request.session['socialregistration_user'] = user
        request.session['next'] = _get_next(request)
        return HttpResponseRedirect(reverse('socialregistration_setup'))

    login(request, user)
    
    return HttpResponseRedirect(getattr(settings, 'LOGIN_REDIRECT_URL', _get_next(request)))


def friendfeed(request):
    """
    Actually setup an account relating to a friendfeed user after the oauth process
    is finished successfully
    """
    raise NotImplementedError()

def oauth_redirect(request, consumer_key=None, secret_key=None,
    request_token_url=None, access_token_url=None, authorization_url=None,
    callback_url=None):
    """
    View to handle the OAuth based authentication redirect to the service provider
    """
    request.session['next'] = _get_next(request)
    client = OAuthClient(request, consumer_key, secret_key,
        request_token_url, access_token_url, authorization_url, callback_url)
    return client.get_redirect()

def oauth_callback(request, consumer_key=None, secret_key=None,
    request_token_url=None, access_token_url=None, authorization_url=None,
    callback_url=None, template='socialregistration/oauthcallback.html',
    extra_context=dict()):
    """
    View to handle final steps of OAuth based authentication where the user 
    gets redirected back to from the service provider
    """
    client = OAuthClient(request, consumer_key, secret_key, request_token_url,
        access_token_url, authorization_url, callback_url)
    
    extra_context.update(dict(oauth_client=client))
    
    if not client.is_valid():
        return render_to_response(
            template, extra_context, context_instance=RequestContext(request)
        )
    
    # We're redirecting to the setup view for this oauth service
    return HttpResponseRedirect(reverse(client.callback_url))

def openid_redirect(request):
    """
    Redirect the user to the openid provider
    """
    request.session['next'] = _get_next(request)
    request.session['openid_provider'] = request.GET.get('openid_provider')
    
    client = OpenID(
        request,
        'http://%s%s' % (
            Site.objects.get_current().domain,
            reverse('openid_callback')
        ),
        request.GET.get('openid_provider')
    )
    return client.get_redirect()

def openid_callback(request, template='socialregistration/openid.html',
    extra_context=dict()):
    """
    Catches the user when he's redirected back from the provider to our site
    """
    client = OpenID(
        request,
        'http://%s%s' % (
            Site.objects.get_current().domain,
            reverse('openid_callback')
        ),
        request.session.get('openid_provider')
    )
    
    if client.is_valid():
        user = authenticate(identity=request.GET.get('openid.claimed_id'))
        if user is None:
            request.session['socialregistration_user'] = User()
            request.session['socialregistration_profile'] = OpenIDProfile(
                identity=request.GET.get('openid.claimed_id')
            )
            return HttpResponseRedirect(reverse('socialregistration_setup'))
        else:
            login(request, user)
            return HttpResponseRedirect(_get_next(request))            
    
    return render_to_response(
        template,
        dict(),
        context_instance=RequestContext(request)
    )
