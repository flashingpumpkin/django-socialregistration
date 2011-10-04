from django.conf import settings

USE_HTTPS = bool(getattr(settings, 'SOCIALREGISTRATION_USE_HTTPS', False))

class Client(object):
    """
    Base class for OAuth/OpenID clients. Subclasses must implement at least:
    
    * `get_callback_url`
        The URL where the remote service should redirect the user back to
    * `get_redirect_url` 
        The url where the user should be redirected to to request permissions
    * `request`
        Do signed requests against the API
    * `get_session_key`
        A unique identifier for storing the client in the user's session
        
    """
    
    def is_https(self):
        """
        Check if the site is using HTTPS. This is controlled with the 
        `SOCIALREGISTRATION_USE_HTTPS` setting. Default value is `False`.
        """        
        return USE_HTTPS
    
    def get_redirect_url(self, **kwargs):
        """
        Returns the URL where we'll be requesting access/permissions from the 
        user.
        """
        raise NotImplementedError
    
    def get_callback_url(self):
        """
        Returns the URL where the service should redirect the user back to
        once permissions/access were granted - or not. This should take in
        account the `SOCIALREGISTRATION_USE_HTTPS` setting.
        """
        raise NotImplementedError
    
    def request(self, url, method="GET", params=None, headers=None, **kwargs):
        """
        Make signed requests against `url`. Signing method depends on the 
        protocol used.
        """        
        raise NotImplementedError
    
    def get_user_info(self):
        """
        Return the current user's information.
        """
        raise NotImplementedError
    
    @staticmethod
    def get_session_key():
        """
        Return a unique identifier to store this client in the user's session
        for the duration of the authentication/authorization process.
        """
        raise NotImplementedError
