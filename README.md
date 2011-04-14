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

* Add `socialregistration` to your `INSTALLED_APPS`
* Add `django.core.context_processors.request` to the [TEMPLATE_CONTEXT_PROCESSORS](http://docs.djangoproject.com/en/1.3/ref/settings/#template-context-processors)
* Include `socialregistration.urls` in your top level urls:

		urlpatterns = patterns('', 
			# ...
			url(r'^social/', include('socialregistration.urls')))

* Make sure you are using a [RequestContext](http://docs.djangoproject.com/en/1.3/ref/templates/api/#subclassing-context-requestcontext) wherever you are planning to display the
  login buttons
  
		from django.template import RequestContext
	
		def login(request):
			# ...
			return render_to_response('login.html',
				{}, context_instance = RequestContext(request))

---

### Facebook Connect

#### Configuration

* Add the Facebook API keys to the your settings, variable names are

		FACEBOOK_API_KEY = ''
		FACEBOOK_SECRET_KEY = ''

* Add `socialregistration.auth.FacebookAuth` to [AUTHENTICATION_BACKENDS](http://docs.djangoproject.com/en/1.3/ref/settings/#authentication-backends)
* Add `socialregistration.middleware.FacebookMiddleware` to [MIDDLEWARE_CLASSES](http://docs.djangoproject.com/en/1.3/ref/settings/#middleware-classes)

#### Usage

* Add tags to your template file

		{% load facebook_tags %}
		{% facebook_button %}
		{% facebook_js %}
	
  You want to keep the `{% facebook_js %}` as far down in your HTML structure as possible to 
  not impact the load time of the page.
  
  Also make sure you followed the steps to include a `RequestContext` in your template that 
  is using these tags.
  
---

### Twitter

#### Configuration  

* Add the Twitter API keys and endpoints to your settings, variable names are

		TWITTER_CONSUMER_KEY = ''
	    TWITTER_CONSUMER_SECRET_KEY = ''
	    TWITTER_REQUEST_TOKEN_URL = ''
	    TWITTER_ACCESS_TOKEN_URL = ''
	    TWITTER_AUTHORIZATION_URL = ''
		
* Add `socialregistration.auth.TwitterAuth` to `AUTHENTICATION_BACKENDS`

#### Usage

* Add tags to your template file

		{% load twitter_tags %}
		{% twitter_button %}
		
  Same note here. Make sure you're serving the page with a `RequestContext`
  
  
