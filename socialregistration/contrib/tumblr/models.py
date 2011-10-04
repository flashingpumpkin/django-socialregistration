from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect

class TumblrProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    tumblr = models.CharField(max_length=100)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.tumblr_name)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(tumblr=self.tumblr)

class TumblrRequestToken(models.Model):
    profile = models.OneToOneField(TumblrProfile, related_name='request_token')
    oauth_token = models.CharField(max_length=80)
    oauth_token_secret = models.CharField(max_length=80)

class TumblrAccessToken(models.Model):
    profile = models.OneToOneField(TumblrProfile, related_name='access_token')
    oauth_token = models.CharField(max_length=80)
    oauth_token_secret = models.CharField(max_length=80)

def save_tumblr_token(sender, user, profile, client, **kwargs):
    try:
        TumblrRequestToken.objects.get(profile=profile).delete()
    except TumblrRequestToken.DoesNotExist:
        pass
    try:
        TumblrAccessToken.objects.get(profile=profile).delete()
    except TumblrAccessToken.DoesNotExist:
        pass
    
    TumblrRequestToken.objects.create(profile=profile,
        oauth_token=client.get_request_token().key,
        oauth_token_secret=client.get_request_token().secret)
    
    TumblrAccessToken.objects.create(profile=profile,
        oauth_token=client.get_access_token().key,
        oauth_token_secret=client.get_access_token().secret)

connect.connect(save_tumblr_token, sender=TumblrProfile,
    dispatch_uid='socialregistration_tumblr_token')
