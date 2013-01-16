try:
    from django.conf.urls import patterns, url, include
except ImportError: # django 1.3
    from django.conf.urls.defaults import patterns, url, include
