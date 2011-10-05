Foursquare
==========

- Add ``socialregistration.contrib.foursquare`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.foursquare'
	)

- Add your API keys and (comma seperated) permissions you request:

::

	FOURSQUARE_CLIENT_ID = ''
	FOURSQUARE_CLIENT_SECRET = ''
	FOURSQUARE_REQUEST_PERMISSIONS = ''


- Anywhere in your templates:

::

	{% load foursquare %}
	{% foursquare_button %}

Or:

::

	{% load foursquare %}
	{% foursquare_button 'custom/button/image.png' %}
