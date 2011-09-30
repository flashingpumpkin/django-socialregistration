from django.contrib.auth.models import User
from django.contrib.sites.models import Site

#from socialregistration.models import (FacebookProfile, TwitterProfile,
#                                       OpenIDProfile, LinkedInProfile)

class Auth(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
#
#class FacebookAuth(Auth):
#    def authenticate(self, uid=None):
#        try:
#            return FacebookProfile.objects.get(
#                uid=uid,
#                site=Site.objects.get_current()
#            ).user
#        except FacebookProfile.DoesNotExist:
#            return None
#

#

#
