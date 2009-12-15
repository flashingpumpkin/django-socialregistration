from django.conf import settings
from django.contrib.auth import logout

from socialregistration.models import FacebookProfile, TwitterProfile

def auth(request):
    profile = None
    if request.user.is_authenticated():
        if request.session['_auth_user_backend'].endswith('FacebookAuth'):
            try:
                profile = FacebookProfile.objects.get(user=request.user)
            except FacebookProfile.DoesNotExist:
                logout(request)
        elif request.session['_auth_user_backend'].endswith('TwitterAuth'):
            try:
                profile = TwitterProfile.objects.get(user=request.user)
            except TwitterProfile.DoesNotExist:
                logout(request)
        
    return {
        'request': request,
        'profile': profile,
        'avatar': get_avatar(request, profile)
        }

def get_avatar(request, profile):
    avatar_url = None
    if profile.__class__.__name__ == 'FacebookProfile':
        avatar_url = request.facebook.users.getInfo([profile.uid], ['pic_square_with_logo'])[0]['pic_square_with_logo']
    elif profile.__class__.__name__ == 'TwitterProfile':
        client = OAuthTwitter(
            request, settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET_KEY,
            settings.TWITTER_REQUEST_TOKEN_URL,
            )
    
        user_info = client.get_user_info()
        avatar_url = user_info['profile_image_url']

    return avatar_url
