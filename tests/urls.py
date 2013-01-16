from socialregistration.compat.urls import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('socialregistration.urls', namespace='socialregistration')),
    url(r'^$', 'tests.app.views.index', name='index'),
)
