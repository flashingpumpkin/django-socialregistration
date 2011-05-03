# Django Social Registration

Django Social Registration enables developers to add alternative registration
methods based on third party sites.

Supported methods currently are:

* OpenID
* OAuth
* Facebook Connect

## Requirements

* [Django](http://pypi.python.org/pypi/django/)
* [oauth2](http://pypi.python.org/pypi/oauth2/)
* [python-openid](http://pypi.python.org/pypi/python-openid)
* [python-sdk](https://github.com/facebook/python-sdk)

## Installation

		pip install django-socialregistration
		pip install -e git+https://github.com/facebook/python-sdk.git#egg=FacebookSDK
	
## Configuration

1. Add `socialregistration` to your `INSTALLED_APPS`
2. Add `django.core.context_processors.request` to the [TEMPLATE_CONTEXT_PROCESSORS](http://docs.djangoproject.com/en/1.3/ref/settings/#template-context-processors)
3. Include `socialregistration.urls` in your top level urls:

		urlpatterns = patterns('', 
			# ...
			url(r'^social/', include('socialregistration.urls')))

4. Make sure you are using a [RequestContext](http://docs.djangoproject.com/en/1.3/ref/templates/api/#subclassing-context-requestcontext) wherever you are planning to display the
   login buttons
  
		from django.template import RequestContext
	
		def login(request):
			# ...
			return render_to_response('login.html',
				{}, context_instance = RequestContext(request))
				
5. Once you're done, and configured, etc, don't forget to `python manage.py syncdb` your project.

## Facebook Connect

#### Configuration

1. Add the Facebook API keys to the your settings, variable names are

		FACEBOOK_APP_ID = ''
		FACEBOOK_API_KEY = ''
		FACEBOOK_SECRET_KEY = ''

2. Add `socialregistration.auth.FacebookAuth` to [AUTHENTICATION_BACKENDS](http://docs.djangoproject.com/en/1.3/ref/settings/#authentication-backends)
3. Add `socialregistration.middleware.FacebookMiddleware` to [MIDDLEWARE_CLASSES](http://docs.djangoproject.com/en/1.3/ref/settings/#middleware-classes)
4. (Optional) Add `FACEBOOK_REQUEST_PERMISSIONS` to your settings. This is a comma seperated list of the permissions you need. e.g:

		FACEBOOK_REQUEST_PERMISSIONS = 'email,user_about_me'
        


#### Usage

* Add tags to your template file

		{% load facebook_tags %}
		{% facebook_button %}
		{% facebook_js %}
	
  You can also specify your own custom button image by appending it to the `facebook_button` template tag:

		{% facebook_button 'http://example.com/other_facebook_button.png' %}

  You want to keep the `{% facebook_js %}` as far down in your HTML structure as possible to 
  not impact the load time of the page.
  
  Also make sure you followed the steps to include a `RequestContext` in your template that 
  is using these tags.
  
## Twitter

#### Configuration  

1. Add the Twitter API keys and endpoints to your settings, variable names are

		TWITTER_CONSUMER_KEY = ''
	    TWITTER_CONSUMER_SECRET_KEY = ''
	    TWITTER_REQUEST_TOKEN_URL = ''
	    TWITTER_ACCESS_TOKEN_URL = ''
	    TWITTER_AUTHORIZATION_URL = ''
		
2. Add `socialregistration.auth.TwitterAuth` to `AUTHENTICATION_BACKENDS`
3. Add the right callback URL to your Twitter account

#### Usage

* Add tags to your template file

		{% load twitter_tags %}
		{% twitter_button %}
		
  Same note here. Make sure you're serving the page with a `RequestContext`

  You can also specify your own custom button image by appending it to the `twitter_button` template tag:

		{% twitter_button 'http://example.com/other_twitter_button.png' %}


## OAuth

Check out how the Twitter authentication works. Basically it's just plugging
together some urls and creating an auth backend, a model and a view.

## OpenID

#### Configuration

* Add `socialregistration.auth.OpenIDAuth` to `AUTHENTICATION_BACKENDS`

#### Usage

* Add tags to your template file

		{% load openid_tags %}
		{% openid_form %}
		
## Logging users out

You can use the standard `{% url auth_logout %}`. Alternatively there is also `{% url social_logout %}`
which is basically a wrapper around `auth_logout`.

*This will log users only out of your site*. 

To make sure they're logged out of other sites too, use something like this:

		<a href="#" onclick:"javascript:FB.logout(function(resp){ document.location = '{% url social_logout %}'; })">Logout</a>
		
Or redirect them to the provider they logged in from.

## Additional Settings

		SOCIALREGISTRATION_USE_HTTP = False
		SOCIALREGISTRATION_GENERATE_USERNAME = False

Set either `True` if you want to enable HTTPS or have the users skip the username form.


## Signals

The app provides two signals that fire when users connect their accounts and log in:

		socialregistration.signals.connect
		socialregistration.signals.login

The signal handlers needs to accept three arguments, and can listen on specific profiles:

		from socialregistration import signals
		from socialregistration import models
		
		def connect_facebook(user, profile, client, **kwargs):
			# Do fancy stuff like fetching more user info with the client
			pass
		
		def login_facebook(user, profile, client, **kwargs):
			# Do fancy stuff like finding logged in friends
			pass
		
		signals.connect.connect(connect_facebook, sender = models.FacebookProfile)
		signals.login.connect(login_facebook, sender = models.FacebookProfile)

This works too with OpenID and OAuth profiles.
