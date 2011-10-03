from django.contrib.auth.models import User

class Auth(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
