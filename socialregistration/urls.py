"""
Created on 22.09.2009

@author: alen
"""
from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url('^setup/$', 'socialregistration.views.setup',
        name='socialregistration_setup'),
)

# Setup Facebook URLs if there's an API key specified
if getattr(settings, 'FACEBOOK_API_KEY', None) is not None:
    urlpatterns = urlpatterns + patterns('',
        url('^facebook/login/$', 'socialregistration.views.facebook_login',
            name='facebook_login'),
        
        url('^facebook/connect/$', 'socialregistration.views.facebook_connect',
            name='facebook_connect'),
        
        url('^xd_receiver.html$', 'django.views.generic.simple.direct_to_template',
            {'template':'socialregistration/xd_receiver.html'},
            name='facebook_xd_receiver'),
    )

#Setup Twitter URLs if there's an API key specified
if getattr(settings, 'TWITTER_CONSUMER_KEY', None) is not None:
    urlpatterns = urlpatterns + patterns('',
        url('^twitter/redirect/$', 'socialregistration.views.oauth_redirect',
            dict(
                consumer_key=settings.TWITTER_CONSUMER_KEY,
                secret_key=settings.TWITTER_CONSUMER_SECRET_KEY,
                request_token_url=settings.TWITTER_REQUEST_TOKEN_URL,
                access_token_url=settings.TWITTER_ACCESS_TOKEN_URL,
                authorization_url=settings.TWITTER_AUTHORIZATION_URL,
                callback_url='twitter_callback'
            ),
            name='twitter_redirect'),
        
        url('^twitter/callback/$', 'socialregistration.views.oauth_callback',
            dict(
                consumer_key=settings.TWITTER_CONSUMER_KEY,
                secret_key=settings.TWITTER_CONSUMER_SECRET_KEY,
                request_token_url=settings.TWITTER_REQUEST_TOKEN_URL,
                access_token_url=settings.TWITTER_ACCESS_TOKEN_URL,
                authorization_url=settings.TWITTER_AUTHORIZATION_URL,
                callback_url='twitter'
            ),
            name='twitter_callback'
        ),
        url('^twitter/$', 'socialregistration.views.twitter', name='twitter'),
    )
    
# Setup FriendFeed URLs if there's an API key specified
if getattr(settings, 'FRIENDFEED_CONSUMER_KEY', None) is not None:
    urlpatterns = urlpatterns + patterns('',
        url('^friendfeed/redirect/$', 'socialregistration.views.oauth_redirect',
            dict(
                consumer_key=settings.FRIENDFEED_CONSUMER_KEY,
                secret_key=settings.FRIENDFEED_CONSUMER_SECRET_KEY,
                request_token_url=settings.FRIENDFEED_REQUEST_TOKEN_URL,
                access_token_url=settings.FRIENDFEED_ACCESS_TOKEN_URL,
                authorization_url=settings.FRIENDFEED_AUTHORIZATION_URL,
                callback_url='friendfeed_callback'
            ),
            name='friendfeed_redirect'),
        
        url('^friendfeed/callback/$', 'socialregistration.views.oauth_callback',
            dict(
                consumer_key=settings.FRIENDFEED_CONSUMER_KEY,
                secret_key=settings.FRIENDFEED_CONSUMER_SECRET_KEY,
                request_token_url=settings.FRIENDFEED_REQUEST_TOKEN_URL,
                access_token_url=settings.FRIENDFEED_ACCESS_TOKEN_URL,
                authorization_url=settings.FRIENDFEED_AUTHORIZATION_URL,
                callback_url='friendfeed'
            ),
            name='friendfeed_callback'
        ),
        url('^friendfeed/$', 'socialregistration.views.friendfeed', name='friendfeed'),
    )

urlpatterns = urlpatterns + patterns('',
    url('^openid/redirect/', 'socialregistration.views.openid_redirect', name='openid_redirect'),
    url('^openid/callback/', 'socialregistration.views.openid_callback', name='openid_callback')
)
