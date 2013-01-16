from django.conf import settings
from socialregistration.compat.urls import *
from socialregistration.contrib.twitter.views import TwitterRedirect, \
    TwitterCallback, TwitterSetup

urlpatterns = patterns('',
    url('^redirect/$', TwitterRedirect.as_view(), name='redirect'),
    url('^callback/$', TwitterCallback.as_view(), name='callback'),
    url('^setup/$', TwitterSetup.as_view(), name='setup'),
)
