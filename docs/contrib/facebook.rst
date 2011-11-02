Facebook
========

- Add ``socialregistration.contrib.facebook`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.facebook'
	)


- Add ``socialregistration.contrib.facebook.auth.FacebookAuth`` to your ``AUTHENTICATION_BACKENDS``

::

	AUTHENTICATION_BACKENDS = (
		'django.contrib.auth.backends.ModelBackend',
		'socialregistration.contrib.facebook.auth.FacebookAuth',
	)

- Add your API keys and (comma seperated) permissions you request:

::

	FACEBOOK_APP_ID = ''
	FACEBOOK_SECRET_KEY = ''
	FACEBOOK_REQUEST_PERMISSIONS = ''

- Anywhere in your templates:

::

	{% load facebook %}
	{% facebook_button %}

Or:

::

	{% load facebook %}
	{% facebook_button 'custom/button/image.png' %}
