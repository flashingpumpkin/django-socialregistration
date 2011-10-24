Twitter
=======

- Add ``socialregistration.contrib.twitter`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.twitter'
	)

- Add ``socialregistration.contrib.twitter.auth.TwitterAuth`` to your ``AUTHENTICATION_BACKENDS``

::

	AUTHENTICATION_BACKENDS = (
		'django.contrib.auth.backends.ModelBackend',
		'socialregistration.contrib.twitter.auth.TwitterAuth',
	)

- Add your API keys:

::

	TWITTER_CONSUMER_KEY = ''
	TWITTER_CONSUMER_SECRET_KEY = ''


- Anywhere in your templates:

::

	{% load twitter %}
	{% twitter_button %}

Or:

::

	{% load twitter %}
	{% twitter_button 'custom/button/image.png' %}
