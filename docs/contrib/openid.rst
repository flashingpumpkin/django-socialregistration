OpenID
======

- Add ``socialregistration.contrib.openid`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.openid'
	)

- Anywhere in your templates:

::

	{% load openid %}
	{% openid_form %}

Or

::

	{% load openid %}
	{% openid_form 'https://www.google.com/accounts/o8/id' 'login/with/google.png' %}
