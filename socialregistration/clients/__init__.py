from django.conf import settings

USE_HTTPS = bool(getattr(settings, 'SOCIALREGISTRATION_USE_HTTPS', False))

class Client(object):
    """
    Base class for OAuth/OpenID clients. 
    """
    def is_https(self):
        return USE_HTTPS
    
    def get_callback_url(self):
        raise NotImplementedError
    
    def get_redirect_url(self):
        raise NotImplementedError
    
    @staticmethod
    def get_session_key():
        raise NotImplementedError
