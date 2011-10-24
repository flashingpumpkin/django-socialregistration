from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.openid.views import OpenIDRedirect, \
    OpenIDCallback, OpenIDSetup

urlpatterns = patterns('',
    url('^redirect/$', OpenIDRedirect.as_view(), name='redirect'),
    url('^callback/$', OpenIDCallback.as_view(), name='callback'),
    url('^setup/$', OpenIDSetup.as_view(), name='setup'),
)
