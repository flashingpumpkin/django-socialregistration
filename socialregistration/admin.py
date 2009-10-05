"""
Created on 22.09.2009

@author: alen
"""
from django.contrib import admin
from socialregistration.models import (FacebookProfile, TwitterProfile,
    OpenIDProfile, OpenIDStore, OpenIDNonce)

admin.site.register([FacebookProfile, TwitterProfile, OpenIDProfile, OpenIDStore, OpenIDNonce])


