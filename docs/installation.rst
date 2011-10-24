Setup
-----

Requirements
============

-  `oauth2 <http://pypi.python.org/pypi/oauth2/>`_
-  `python-openid <http://pypi.python.org/pypi/python-openid>`_
-  `facebook-python-sdk <https://github.com/facebook/python-sdk>`_

Installation
============

::

    pip install django-socialregistration
    pip install -e git+https://github.com/facebook/python-sdk.git#egg=FacebookSDK


Configuration
=============

The most basic configuration is to add ``socialregistration`` and
``django.contrib.sites`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
        'django.contrib.sites',
		'socialregistration'
	)

..note::

    To make sure that your redirects and callbacks work properly you'll have to set
    the domain in the `Sites app <https://docs.djangoproject.com/en/1.3/ref/contrib/sites/>`_
    to the correct value.

Include ``socialregistration.urls`` into your root ``urls.py`` file

::

	urlpatterns = patterns('',
		url(r'^social/', include('socialregistration.urls',
			namespace = 'socialregistration')))

.. note::

	The ``namespace = 'socialregistration'`` argument is required.

Note on sessions
================

When starting the registration process, all the user's temporary data is stored
in the user's session. If you're developing on `http://127.0.0.1:8000`_, you will
have to set your callback URLs to use `http://127.0.0.1:8000`_ too or you will get
a new session when returning to the site and socialregistration won't be able
to find the temporary data and subsequently throw a ``KeyError``.

Also not that Twitter for example will not accept `http://localhost:8000`_ as a
valid domain for the callback URL so you'll have to use `http://127.0.0.1:8000`_
when developing your site.