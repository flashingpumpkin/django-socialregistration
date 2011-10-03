from django.db import models
from django.conf import settings

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from socialregistration.signals import login, connect






