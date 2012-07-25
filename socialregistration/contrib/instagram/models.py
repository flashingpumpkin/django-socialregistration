from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect

class InstagramProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    instagram = models.CharField(max_length = 255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.instagram)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(instagram=self.instagram)

class InstagramAccessToken(models.Model):
    profile = models.OneToOneField(InstagramProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)
    
def save_instagram_token(sender, user, profile, client, **kwargs):
    try:
        InstagramAccessToken.objects.get(profile=profile).delete()
    except InstagramAccessToken.DoesNotExist:
        pass
    
    InstagramAccessToken.objects.create(access_token = client.get_access_token(),
        profile = profile)


connect.connect(save_instagram_token, sender=InstagramProfile,
    dispatch_uid='socialregistration_instagram_token')
