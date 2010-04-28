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
- pyfacebook

Installation
============

#. Add the ``socialregistration`` directory to your ``PYTHON_PATH``.
#. Add ``socialregistration`` to your ``INSTALLED_APPS`` settings of Django.
#. Add ``socialregistration.urls`` to your ``urls.py`` file.

Configuration
=============

Facebook Connect
----------------
#. Add ``FACEBOOK_API_KEY`` and ``FACEBOOK_SECRET_KEY`` to your settings file representing the keys you were given by Facebook.
#. Add ``socialregistration.auth.FacebookAuth`` to ``AUTHENTICATION_BACKENDS`` in your settings file.
#. Add ``facebook.djangofb.FacebookMiddleware`` to ``MIDDLEWARE_CLASSES`` in your settings file. See: http://wiki.developers.facebook.com/index.php/User:PyFacebook_Tutorial#Add_the_middleware
#.  Add tags to your template file::

    {% load facebook_tags %}
    {% facebook_button %}
    {% facebook_js %}

#. If you want to use the pyfacebook library to do API calls to Facebook, add ``socialregistration.middleware.FacebookMiddleware`` to your ``MIDDLEWARE_CLASSES`` setting.


Twitter
-------
#. Add the following variables to your ``settings.py`` file with the values you were given by Twitter::

    TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET_KEY
    TWITTER_REQUEST_TOKEN_URL
    TWITTER_ACCESS_TOKEN_URL
    TWITTER_AUTHORIZATION_URL

#. Add ``socialregistration.auth.TwitterAuth`` to your ``AUTHENTICATION_BACKENDS`` settings.

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
You can use the standard {% url auth_logout %} url to log users out of Django.
Please note that this will not log users out of third party sites though.
When using Facebook Connect, it is recommended to follow the FBConnect developer
wiki. See: http://wiki.developers.facebook.com/index.php/Connect/Authorization_Websites#Logging_Out_Users ::

    <a href="#" onclick="FB.Connect.logoutAndRedirect('{% url auth_logout %}')">Logout</a>

To log users out of other third party sites, I recommend redirecting them further to the OAuth / OpenID providers after they logged out of your site.

HTTPS
-----
If you wish everything to go through HTTPS, set ``SOCIALREGISTRATION_USE_HTTPS`` in your settings file to
``True``.

Other Information
-----------------
If you don't wish your users to be redirected to the setup view to create a username but rather have
a random username generated for them, set ``SOCIALREGISTRATION_GENERATE_USERNAME`` in your settings file to ``True``.
