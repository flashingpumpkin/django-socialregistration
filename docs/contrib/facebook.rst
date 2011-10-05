Facebook
========

- Add ``socialregistration.contrib.facebook`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.facebook'
	)

- Add your API keys and (comma seperated) permissions you request:

::

	FACEBOOK_APP_ID = ''
	FACEBOOK_SECRET_KEY = ''
	FOURSQUARE_REQUEST_PERMISSIONS = ''

- Anywhere in your templates:

::

	{% load facebook %}
	{% facebook_button %}

Or:

::

	{% load facebook %}
	{% facebook_button 'custom/button/image.png' %}
