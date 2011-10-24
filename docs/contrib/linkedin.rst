LinkedIn
========

- Add ``socialregistration.contrib.linkedin`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.linkedin'
	)


- Add ``socialregistration.contrib.linkedin.auth.LinkedInAuth`` to your ``AUTHENTICATION_BACKENDS``

::

	AUTHENTICATION_BACKENDS = (
		'django.contrib.auth.backends.ModelBackend',
		'socialregistration.contrib.linkedin.auth.LinkedInAuth',
	)

- Add your API keys:

::

	LINKEDIN_CONSUMER_KEY = ''
	LINKEDIN_CONSUMER_SECRET_KEY = ''


- Anywhere in your templates:

::

	{% load linkedin %}
	{% linkedin_button %}

Or:

::

	{% load linkedin %}
	{% linkedin_button 'custom/button/image.png' %}
