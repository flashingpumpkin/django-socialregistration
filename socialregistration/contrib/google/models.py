from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect

class GoogleProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    google_id = models.CharField(max_length = 255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.google_id)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(google_id=self.google_id)

class GoogleAccessToken(models.Model):
    profile = models.OneToOneField(GoogleProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)

def save_google_token(sender, user, profile, client, **kwargs):
    try:
        GoogleAccessToken.objects.get(profile=profile).delete()
    except GoogleAccessToken.DoesNotExist:
        pass
    
    GoogleAccessToken.objects.create(access_token = client.get_access_token(),
        profile = profile)


connect.connect(save_google_token, sender=GoogleProfile,
    dispatch_uid='socialregistration_google_token')
