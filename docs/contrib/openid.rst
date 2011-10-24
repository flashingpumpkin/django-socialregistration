OpenID
======

- Add ``socialregistration.contrib.openid`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.openid'
	)


- Add ``socialregistration.contrib.openid.auth.OpenIDAuth`` to your ``AUTHENTICATION_BACKENDS``

::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'socialregistration.contrib.openid.auth.OpenIDAuth',
    )

- Anywhere in your templates:

::

	{% load openid %}
	{% openid_form %}

Or

::

	{% load openid %}
	{% openid_form 'https://www.google.com/accounts/o8/id' 'login/with/google.png' %}
