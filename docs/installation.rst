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
    pip install -e git+https://github.com/pythonforfacebook/facebook-sdk#egg=FacebookSDK



Configuration
=============

The most basic configuration is to add ``socialregistration`` and
``django.contrib.sites`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
        'django.contrib.sites',
        'socialregistration'
	)

.. note::

    To make sure that your redirects and callbacks work properly you'll have to set
    the domain in the `Sites app <https://docs.djangoproject.com/en/1.3/ref/contrib/sites/>`_
    to the correct value. 
    
    If you find yourself redirected to example.com, check your Sites configuration through the 
    Django admin interface.

Include ``socialregistration.urls`` into your root ``urls.py`` file

::

	urlpatterns = patterns('',
    	# Here be other urls ...
		url(r'^social/', include('socialregistration.urls',
			namespace = 'socialregistration')))

.. note::

	The ``namespace = 'socialregistration'`` argument is required.

Include ``django.core.context_processors.request`` in your TEMPLATE_CONTEXT_PROCESSORS in your settings file

::

	TEMPLATE_CONTEXT_PROESSORS = (
        'django.core.context_processors.request',
	)

.. note::

	When your views render templates that include social registration tags (such as {% twitter_button %}) 
	they will need to pass the RequestContext in as a parameter

::

	return render_to_response('template.html', c, context_instance=RequestContext(request))

Note on sessions
================

When starting the registration process, all the user's temporary data is stored
in the user's session. If you're developing on http://127.0.0.1:8000, you will
have to set your callback URLs to begin with http://127.0.0.1:8000 too or you will get
a new session when returning to the site and socialregistration won't be able
to find the temporary data and subsequently throw a ``KeyError``.

Also not that Twitter for example will not accept http://localhost:8000 as a
valid domain for the callback URL so you'll have to use http://127.0.0.1:8000
when developing your site.
