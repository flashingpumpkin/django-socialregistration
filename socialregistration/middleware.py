from django.utils.translation import gettext as _

class FacebookMiddleware(object):
    def process_request(self, request):
        if getattr(request, 'facebook', None):
            raise AttributeError(_('Please make sure you have *facebook.djangofb.FacebookMiddleware* installed as a middleware.'))
        else:
            request.facebook.check_session(request)