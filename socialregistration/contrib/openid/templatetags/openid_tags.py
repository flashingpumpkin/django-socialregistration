import warnings 

warnings.warn("{% load openid_tags %} will be removed. Use {% load openid %} instead")

from openid import *
