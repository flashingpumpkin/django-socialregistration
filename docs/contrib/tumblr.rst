Tumblr
======

- Add ``socialregistration.contrib.tumblr`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.tumblr'
	)

- Add your API keys:

::

	TUMBLR_CONSUMER_KEY = ''
	TUMBLR_CONSUMER_SECRET_KEY = ''


- Anywhere in your templates:

::

	{% load tumblr %}
	{% tumblr_button %}

Or:

::

	{% load tumblr %}
	{% tumblr_button 'custom/button/image.png' %}
