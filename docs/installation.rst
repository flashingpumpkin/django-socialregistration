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

The most basic configuration is to add ``socialregistration`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration'
	)


Include ``socialregistration.urls`` into your root ``urls.py`` file

::

	urlpatterns = patterns('', 
		url(r'^social/', include('socialregistration.urls', 
			namespace = 'socialregistration')))

.. note:: 

	The ``namespace = 'socialregistration'`` argument is required.
