from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.foursquare.views import FoursquareRedirect, \
    FoursquareCallback, FoursquareSetup

 
urlpatterns = patterns('',
    url('^redirect/$', FoursquareRedirect.as_view(), name='redirect'),
    url('^callback/$', FoursquareCallback.as_view(), name='callback'),
    url('^setup/$', FoursquareSetup.as_view(), name='setup'),
)
