Twitter
=======

- Add ``socialregistration.contrib.twitter`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.twitter'
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
