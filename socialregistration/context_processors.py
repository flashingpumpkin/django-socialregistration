from django.contrib.contenttypes.models import ContentType
from facebook.djangofb import Facebook,get_facebook_client

from socialregistration.models import FacebookProfile

def settings(request):
    profile = None
    if request.user.is_authenticated():
        if request.session['_auth_user_backend'].endswith('FacebookAuth'):
            profile = FacebookProfile.objects.get(user=request.user)
        
    return {
        'request': request,
        'profile': profile
        }
