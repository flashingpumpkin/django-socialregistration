Signals
=======

Socialregistration comes with two signals that you can subscribe to:

.. currentmodule:: socialregistration.signals

.. attribute:: connect

	The ``connect`` signal is fired every time a *new* social profile of sorts
	is created. The signal handler should accept four arguments. An additional
	fifth, the current request object, is passed in too:

	::
		
		from socialregistration import signals
		from socialregistration.contrib.facebook.models import FacebookProfile
		
		def connect_handler(sender, user, profile, client, request = None, **kwargs):
			data = client.graph.request('me')
		
		signals.connect.connect(connect_handler, sender = FacebookProfile,
			dispatch_uid = 'facebook.connect')


.. attribute:: login

	The ``login`` signal is fired every time a user signs into your Django 
	application via a third party API. The signal handler here should also
	accept four arguments and take an optional fifth argument, being the current
	request:

	::

		def login_handler(sender, user, profile, client, request = None, **kwargs):
			data = client.graph.request('me')
		
		signals.login.connect(login_handler, sender = FacebookProfile,
			dispatch_uid = 'facebook.connect')

