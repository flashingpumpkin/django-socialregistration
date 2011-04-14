==========================
Django Social Registration
==========================

Django Social Registration enables developers to add alternative registration
methods based on third party sites.


Requirements
============
- django
- oauth2
- python-openid
- python-sdk_ 

Installation
============
::
	pip install django-socialregistration
	pip install -e git+https://github.com/facebook/python-sdk.git#egg=FacebookSDK


Configuration
============= 

#. Add ``socialregistration`` to your ``INSTALLED_APPS`` 
#. Add ``django.core.context_processors.request`` to your ``TEMPLATE_CONTEXT_PROCESSORS``
#. Include ``socialregistration.urls`` in your top level urls::
   
   urlpatterns = patterns('',
       # ... 	
   	   url('^social/',include('socialregistration.urls')))

#. Make sure you are using a ``RequestContext``_ wherever you are displaying the buttons::

   from django.template import RequestContext
   def login(request):
       return render_to_response('login.html', {}, context_instance = RequestContext(request))   


Facebook Connect
----------------
#. Add ``FACEBOOK_API_KEY`` and ``FACEBOOK_SECRET_KEY`` to your settings file representing the keys you were given by Facebook.
#. Add ``socialregistration.auth.FacebookAuth`` to ``AUTHENTICATION_BACKENDS`` in your settings
#. Add ``socialregistration.middleware.FacebookMiddleware`` to ``MIDDLEWARE_CLASSES`` in your settings
#.  Add tags to your template file::

    {% load facebook_tags %}
    {% facebook_button %}
    {% facebook_js %}

Twitter
-------
#. Add the following variables to your settings with the values you were given by Twitter::

    TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET_KEY
    TWITTER_REQUEST_TOKEN_URL
    TWITTER_ACCESS_TOKEN_URL
    TWITTER_AUTHORIZATION_URL

#. Add ``socialregistration.auth.TwitterAuth`` to your ``AUTHENTICATION_BACKENDS`` settings

#. Add tags to your template file::

    {% load twitter_tags %}
    {% twitter_button %}


Other OAuth Services
--------------------
Please refer to the Twitter implementation of the signup / login process to
extend your own application to act as a consumer of other OAuth providers.
Basically it's just plugging together some urls and creating an auth backend,
a model and a view.


OpenID
------
#. Add ``socialregistration.auth.OpenIDAuth`` to ``AUTHENTICATION_BACKENDS`` in your settings.
#. Add tags to your template file::

    {% load openid_tags %}
    {% openid_form %}

Logging users out
-----------------
You can use the standard ``{% url auth_logout %}`` url to log users out of Django. 
Alternatively there is also a wrapper around `auth_logout`: ``{% url social_logout %}``
Please note that this will not log users out of third party sites though. Logging out a 
Facebook user might look something like this:: 

    <a href="#" onclick="javascript:FB.logout(function(response){ document.location = '{% url auth_logout %}' })">Logout</a>

To log users out of other third party sites, I recommend redirecting them further to the OAuth / OpenID providers after they logged out of your site.

HTTPS
-----
If you wish everything to go through HTTPS, set ``SOCIALREGISTRATION_USE_HTTPS`` in your settings file to
``True``.

Other Information
-----------------
If you don't wish your users to be redirected to the setup view to create a username but rather have
a random username generated for them, set ``SOCIALREGISTRATION_GENERATE_USERNAME`` in your settings file to ``True``.

.. _python-sdk: http://github.com/facebook/python-sdk
.. _``RequestContext``: http://docs.djangoproject.com/en/1.3/ref/templates/api/#subclassing-context-requestcontext
