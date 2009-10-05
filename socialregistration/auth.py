"""
Created on 22.09.2009

@author: alen
"""
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from socialregistration.models import (FacebookProfile, TwitterProfile,
    FriendFeedProfile, OpenIDProfile)

class Auth(object):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class FacebookAuth(Auth):
    def authenticate(self, uid=None):
        try:
            return FacebookProfile.objects.get(
                uid=uid,
                site=Site.objects.get_current()
            ).user
        except:
            return None

class TwitterAuth(Auth):
    def authenticate(self, twitter_id=None):
        try:
            return TwitterProfile.objects.get(
                twitter_id=twitter_id,
                site=Site.objects.get_current()
            ).user
        except:
            return None
        
class OpenIDAuth(Auth):
    def authenticate(self, identity=None):
        try:
            return OpenIDProfile.objects.get(
                identity=identity,
                site=Site.objects.get_current()
            ).user
        except:
            return None