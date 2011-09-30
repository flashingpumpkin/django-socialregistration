from django.db import models
from django.conf import settings

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from socialregistration.signals import login, connect

class FacebookProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    uid = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.uid)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(uid=self.uid)

class FacebookAccessToken(models.Model):
    profile = models.OneToOneField(FacebookProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)

class TwitterProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    twitter_id = models.PositiveIntegerField()

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.twitter_id)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(twitter_id=self.twitter_id)

class TwitterRequestToken(models.Model):
    profile = models.OneToOneField(TwitterProfile, related_name='request_token')
    oauth_token = models.CharField(max_length=80)
    oauth_token_secret = models.CharField(max_length=80)

class TwitterAccessToken(models.Model):
    profile = models.OneToOneField(TwitterProfile, related_name='access_token')
    oauth_token = models.CharField(max_length=80)
    oauth_token_secret = models.CharField(max_length=80)

class LinkedInProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    linkedin_id = models.CharField(max_length=25)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.linkedin_id)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(linkedin_id=self.linkedin_id)

class LinkedInRequestToken(models.Model):
    profile = models.OneToOneField(LinkedInProfile, related_name='request_token')
    oauth_token = models.CharField(max_length=80)
    oauth_token_secret = models.CharField(max_length=80)

class LinkedInAccessToken(models.Model):
    profile = models.OneToOneField(LinkedInProfile, related_name='access_token')
    oauth_token = models.CharField(max_length=80)
    oauth_token_secret = models.CharField(max_length=80)


def save_facebook_token(sender, user, profile, client, **kwargs):
    if not 'offline_access' in getattr(settings, 'FACEBOOK_REQUEST_PERMISSIONS', ''):
        return
    
    try:
        FacebookAccessToken.objects.get(profile=profile).delete()
    except FacebookAccessToken.DoesNotExist:
        pass
    
    FacebookAccessToken.objects.create(profile=profile,
        access_token=client.graph.access_token)

def save_twitter_token(sender, user, profile, client, **kwargs):
    try:
        TwitterRequestToken.objects.get(profile=profile).delete()
    except TwitterRequestToken.DoesNotExist:
        pass
    try:
        TwitterAccessToken.objects.get(profile=profile).delete()
    except TwitterAccessToken.DoesNotExist:
        pass
    
    TwitterRequestToken.objects.create(profile=profile,
        oauth_token=client.request_token['oauth_token'],
        oauth_token_secret=client.request_token['oauth_token_secret'])
    
    TwitterAccessToken.objects.create(profile=profile,
        oauth_token=client.access_token['oauth_token'],
        oauth_token_secret=client.access_token['oauth_token_secret'])
    
def save_linkedin_token(sender, user, profile, client, **kwargs):
    try:
        LinkedInRequestToken.objects.get(profile=profile).delete()
    except LinkedInRequestToken.DoesNotExist:
        pass
    try:
        LinkedInAccessToken.objects.get(profile=profile).delete()
    except LinkedInAccessToken.DoesNotExist:
        pass
    
    LinkedInRequestToken.objects.create(profile=profile,
        oauth_token=client.request_token['oauth_token'],
        oauth_token_secret=client.request_token['oauth_token_secret'])
    
    LinkedInAccessToken.objects.create(profile=profile,
        oauth_token=client.access_token['oauth_token'],
        oauth_token_secret=client.access_token['oauth_token_secret'])
    
connect.connect(save_facebook_token, sender=FacebookProfile,
    dispatch_uid='socialregistration_facebook_token')
connect.connect(save_twitter_token, sender=TwitterProfile,
    dispatch_uid='socialregistration_twitter_token')
connect.connect(save_linkedin_token, sender=LinkedInProfile,
    dispatch_uid='socialregistration_linkedin_token')
