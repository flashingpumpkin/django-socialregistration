from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.google.views import GoogleRedirect, \
    GoogleCallback, GoogleSetup
 
urlpatterns = patterns('',
    url('^redirect/$', GoogleRedirect.as_view(), name='redirect'),
    url('^callback/$', GoogleCallback.as_view(), name='callback'),
    url('^setup/$', GoogleSetup.as_view(), name='setup'),
)
