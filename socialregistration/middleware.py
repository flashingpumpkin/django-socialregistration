import facebook
from django.conf import settings


class Facebook(object):
    def __init__(self, user=None):
        if user is None:
            self.uid = None
        else:
            self.uid = user['uid']
            self.user = user

        self.access_token = None

    def get_graph(self):
        if not self.access_token:
            self.access_token = facebook.get_user_access_token(
                self.user.get('code', ''),
                getattr(
                    settings,
                    'FACEBOOK_APP_ID',
                    settings.FACEBOOK_API_KEY
                ),
                settings.FACEBOOK_SECRET_KEY
            ).get('access_token', None)

        return facebook.GraphAPI(self.access_token)


class FacebookMiddleware(object):
    def process_request(self, request):
        """
        Enables ``request.facebook`` and ``request.facebook.graph`` in your views 
        once the user authenticated the  application and connected with facebook. 
        You might want to use this if you don't feel confortable with the 
        javascript library.
        """
        
        data = facebook.get_user_from_cookie(request.COOKIES,
            getattr(settings, 'FACEBOOK_APP_ID', settings.FACEBOOK_API_KEY), settings.FACEBOOK_SECRET_KEY)

        if data is None:
            # maybe OAuth 2
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
                )
            if data:
                data['uid'] = data['user_id']
            else:
                data = None

        request.facebook = Facebook(data)
        
        return None
