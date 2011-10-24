from django.conf import settings
from django.conf.urls.defaults import *
from socialregistration.contrib.github.views import GithubRedirect, \
    GithubCallback, GithubSetup
 
urlpatterns = patterns('',
    url('^redirect/$', GithubRedirect.as_view(), name='redirect'),
    url('^callback/$', GithubCallback.as_view(), name='callback'),
    url('^setup/$', GithubSetup.as_view(), name='setup'),
)
