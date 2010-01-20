from django.utils.translation import gettext as _

class FacebookMiddleware(object):
    def process_request(self, request):
        """
        Enables request.facebook in your views once the user authenticated the
        application and connected with facebook. You might want to use this
        if you don't feel confortable with the javascript library.
        """
        if getattr(request, 'facebook', None) is None:
            raise AttributeError(_('Please make sure you have *facebook.djangofb.FacebookMiddleware* installed as a middleware.'))
        else:
            request.facebook.check_session(request)
        return None