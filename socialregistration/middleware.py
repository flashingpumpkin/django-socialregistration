import facebook
from django.conf import settings

APP_ID = getattr(settings, 'FACEBOOK_APP_ID', getattr(settings, 'FACEBOOK_API_KEY', None))
SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')

if not APP_ID:
    raise ValueError('You must specify a FACEBOOK_APP_ID setting')

if not SECRET_KEY:
    raise ValueError('You must specify a FACEBOOK_SECRET_KEY setting')

class Facebook(object):
    def __init__(self, user):
        self.user = user
        
        self.uid = user.get('user_id', '')
        
        self.access_token = ''

    def get_graph(self):
        try:
            user_code = self.user.get('code', '')
            self.access_token = facebook.get_user_access_token(
                user_code, APP_ID, SECRET_KEY).get('access_token', '')
            
            if self.access_token:
                return facebook.GraphAPI(self.access_token)
            return None
        except TypeError:
            return None


class FacebookMiddleware(object):
    def process_request(self, request):
        """
        Enables ``request.facebook`` and ``request.facebook.get_graph`` in your views
        once the user authenticated the  application and connected with facebook. 
        You might want to use this if you don't feel confortable with the 
        javascript library.
        """
        # Try get the new OAuth cookie
        cookie = request.COOKIES.get('fbsr_%s' % APP_ID, '')
        
        data = facebook.parse_signed_request(cookie, SECRET_KEY)
        
        if not data:
            # Whoopsie, no new OAuth cookie. Maybe an old one?
            data = facebook.get_user_from_cookie(request.COOKIES, APP_ID, SECRET_KEY)
        
        request.facebook = Facebook(data or {})        
        
        return None
