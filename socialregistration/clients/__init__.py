from django.conf import settings

USE_HTTPS = bool(getattr(settings, 'SOCIALREGISTRATION_USE_HTTPS', False))

class Client(object):
    """
    Base class for OAuth/OpenID clients. Subclasses must implement all the 
    methods.
    """
    
    def is_https(self):
        """
        Check if the site is using HTTPS. This is controlled with 
        ``SOCIALREGISTRATION_USE_HTTPS`` setting. 
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
        account the value returned by ``self.is_https()``.
        """
        raise NotImplementedError
    
    def request(self, url, method="GET", params=None, headers=None, **kwargs):
        """
        Make signed requests against ``url``. Signing method depends on the 
        protocol used.

        :param url: The API endpoint to request
        :param method: The HTTP method to be used
        :param params: The parameters to be used for the request
        :type params: dict
        :param headers: Additional headers to be sent with the request
        :type headers: dict
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
