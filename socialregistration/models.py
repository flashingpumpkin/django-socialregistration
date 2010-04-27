from django.db import models

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site 

class FacebookProfile(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    uid = models.CharField(max_length=255, blank=False, null=False)
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.uid)
    
    def authenticate(self):
        return authenticate(uid=self.uid)

class TwitterProfile(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    twitter_id = models.PositiveIntegerField()
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.twitter_id)
    
    def authenticate(self):
        return authenticate(twitter_id=self.twitter_id)

class OpenIDProfile(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    identity = models.TextField()
    
    def __unicode__(self):
        return u'OpenID Profile for %s, via provider %s' % (self.user, self.identity)

    def authenticate(self):
        return authenticate(identity=self.identity)

class OpenIDStore(models.Model):
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.TextField()
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField()

    def __unicode__(self):
        return u'OpenID Store %s for %s' % (self.server_url, self.site)

class OpenIDNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'OpenID Nonce for %s' % self.server_url
