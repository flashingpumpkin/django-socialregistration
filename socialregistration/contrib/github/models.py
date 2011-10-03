from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect

class GithubProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    github = models.CharField(max_length = 255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.github)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(github=self.github)

class GithubAccessToken(models.Model):
    profile = models.OneToOneField(GithubProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)
    
def save_github_token(sender, user, profile, client, **kwargs):
    try:
        GithubAccessToken.objects.get(profile=profile).delete()
    except GithubAccessToken.DoesNotExist:
        pass
    
    GithubAccessToken.objects.create(access_token = client.get_access_token(),
        profile = profile)


connect.connect(save_github_token, sender=GithubProfile,
    dispatch_uid='socialregistration_github_token')
