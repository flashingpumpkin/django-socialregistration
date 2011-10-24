from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('socialregistration.urls',
        namespace='socialregistration')),
    url(r'^$', 'example.app.views.index', name='index'),
)
