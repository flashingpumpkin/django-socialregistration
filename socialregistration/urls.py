from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',)

if 'socialregistration.contrib.openid' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url('openid/', include('socialregistration.contrib.openid.urls',
            namespace='openid')))

if 'socialregistration.contrib.twitter' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url('twitter/', include('socialregistration.contrib.twitter.urls',
            namespace='twitter')))

if 'socialregistration.contrib.linkedin' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url('twitter/', include('socialregistration.contrib.linkedin.urls',
            namespace='linkedin')))

if 'socialregistration.contrib.facebook' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url('twitter/', include('socialregistration.contrib.facebook.urls',
            namespace='facebook')))

