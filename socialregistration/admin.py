from django.contrib import admin
from socialregistration.models import (FacebookProfile, TwitterProfile,
    OpenIDProfile, OpenIDStore, OpenIDNonce, LinkedInProfile)

admin.site.register([FacebookProfile, TwitterProfile, LinkedInProfile, 
                     OpenIDProfile, OpenIDStore, OpenIDNonce])


