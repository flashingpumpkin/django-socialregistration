import facebook
from django.conf import settings


class Facebook(object):
    def __init__(self, user=None):
        self.user = user
        if user:
            self.uid = user.get('user_id', '')

        self.access_token = ''

    def get_graph(self):
        if self.user and not self.access_token:
            user_code = self.user.get('code', '')
            if user_code:
                self.access_token = facebook.get_user_access_token(
                    user_code,
                    getattr(
                        settings,
                        'FACEBOOK_APP_ID',
                        settings.FACEBOOK_API_KEY
                    ),
                    settings.FACEBOOK_SECRET_KEY
                ).get('access_token', '')

        return self.access_token and facebook.GraphAPI(self.access_token) or None


class FacebookMiddleware(object):
    def process_request(self, request):
        """
        Enables ``request.facebook`` and ``request.facebook.get_graph`` in your views
        once the user authenticated the  application and connected with facebook. 
        You might want to use this if you don't feel confortable with the 
        javascript library.
        """
        data = facebook.parse_signed_request(
            request.COOKIES.get(
                'fbsr_' + getattr(
                    settings,
                    'FACEBOOK_APP_ID',
                    settings.FACEBOOK_API_KEY
                    ),
                '',
                ),
            settings.FACEBOOK_SECRET_KEY,
            ) or {}

        request.facebook = Facebook(data)
        
        return None
