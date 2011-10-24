from django.utils.functional import SimpleLazyObject
from socialregistration.contrib.facebook.models import FacebookAccessToken, \
    FacebookProfile
import facebook

def get_uid(user):
    try:
        return FacebookProfile.objects.get(user = user).uid
    except FacebookProfile.DoesNotExist:
        return ''

def get_access_token(user):
    try:
        return FacebookAccessToken.objects.get(profile__user = user).access_token
    except FacebookAccessToken.DoesNotExist:
        return ''
    
def get_graph(user):
    def wrapped(self):
        if not self.access_token:
            return None
        return facebook.GraphAPI(self.access_token)
    return wrapped

def get_facebook_object(user):
    def wrapped():
        return type('Facebook', (object,), {'uid': get_uid(user), 
            'access_token': get_access_token(user), 'get_graph': get_graph(user)})()    
    return wrapped

class FacebookMiddleware(object):
    def process_request(self, request):
        """
        Enables ``request.facebook`` in your views for authenticated users.
        It's a lazy object that does database lookups.
        """
        
        request.facebook = SimpleLazyObject(get_facebook_object(request.user))
        
        return None