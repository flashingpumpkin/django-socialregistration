from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.linkedin.views import LinkedInRedirect, \
    LinkedInCallback, LinkedInSetup
 
urlpatterns = patterns('',
    url('^redirect/$', LinkedInRedirect.as_view(), name='redirect'),
    url('^callback/$', LinkedInCallback.as_view(), name='callback'),
    url('^setup/$', LinkedInSetup.as_view(), name='setup'),
)
