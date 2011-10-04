from django.contrib.auth.models import User
from socialregistration.contrib.facebook.auth import FacebookAuth
from socialregistration.contrib.linkedin.auth import LinkedInAuth
from socialregistration.contrib.openid.auth import OpenIDAuth
from socialregistration.contrib.twitter.auth import TwitterAuth

import warnings

warnings.warn("`socialregistration.auth.*` will be removed. "
    "Use `socialregistration.contrib.*.auth.*` instead.")
