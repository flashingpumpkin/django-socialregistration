Github
=======

- Add ``socialregistration.contrib.github`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.github'
	)


- Add ``socialregistration.contrib.github.auth.GithubAuth`` to your ``AUTHENTICATION_BACKENDS``

::

	AUTHENTICATION_BACKENDS = (
		'django.contrib.auth.backends.ModelBackend',
		'socialregistration.contrib.github.auth.GithubAuth',
	)

- Add your API keys and (comma seperated) permissions you request:

::

	GITHUB_CLIENT_ID = ''
	GITHUB_CLIENT_SECRET = ''
	GITHUB_REQUEST_PERMISSIONS = ''

- Anywhere in your templates:

::

	{% load github %}
	{% github_button %}

Or:

::

	{% load github %}
	{% github_button 'custom/button/image.png' %}
