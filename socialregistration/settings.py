from django.conf import settings

SESSION_KEY = getattr(settings, 'SOCIALREGISTRATION_SESSION_KEY', 'socialreg:')