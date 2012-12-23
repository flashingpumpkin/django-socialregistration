from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class FoursquareProfile(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    foursquare = models.CharField(max_length=255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.foursquare)
        except models.ObjectDoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(foursquare=self.foursquare)

class FoursquareAccessToken(models.Model):
    profile = models.OneToOneField(FoursquareProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)

def save_foursquare_token(sender, user, profile, client, **kwargs):
    try:
        FoursquareAccessToken.objects.get(profile=profile).delete()
    except FoursquareAccessToken.DoesNotExist:
        pass

    FoursquareAccessToken.objects.create(access_token=client.get_access_token(),
        profile=profile)


connect.connect(save_foursquare_token, sender=FoursquareProfile,
    dispatch_uid='socialregistration_foursquare_token')
