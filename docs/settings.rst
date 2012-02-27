Settings
--------

.. currentmodule:: socialregistration.conf.settings

.. attribute:: SOCIALREGISTRATION_USE_HTTPS

	:Default: ``False``

	Whether your callback URLs are served via SSL.


.. attribute:: SOCIALREGISTRATION_SESSION_KEY

	:Default: ``'socialreg:'``

	The session key prefix to store temporary user information with while the
	user is setting up an account.


.. attribute:: SOCIALREGISTRATION_GENERATE_USERNAME

	:Default: ``False``

	If set to ``True`` the username will be generated automatically


.. attribute:: SOCIALREGISTRATION_GENERATE_USERNAME_FUNCTION

	:Default: ``'socialregistration.utils.generate_username'``

	If ``SOCIALREGISTRATION_GENERATE_USERNAME`` is ``True``, this function will
	be called and should return a username. The function will receive three
	arguments:

	- A user model
	- A profile model
	- An API client


.. attribute:: SOCIALREGISTRATION_SETUP_FORM

	:Default: ``'socialregistration.forms.UserForm'``

	IF ``SOCIALREGISTRATION_GENERATE_USERNAME`` is ``False``, this form will be
	used to capture data from the user, such as username and email address.


.. attribute:: SOCIALREGISTRATION_INITIAL_DATA_FUNCTION

	:Default: ``None``

	A function that should return some initial data for the
	``SOCIALREGISTRATION_SETUP_FORM``. The function takes four parameters:

	- The request object
	- A user model
	- A profile model
	- An API client


