import warnings
from django import template
from django.conf import settings
from socialregistration.utils import _https

register = template.Library()

@register.inclusion_tag('socialregistration/facebook_js.html')
def facebook_js():
    id = getattr(settings, 'FACEBOOK_APP_ID', None)
    key = getattr(settings, 'FACEBOOK_API_KEY', None)
    perms = getattr(settings, 'FACEBOOK_REQUEST_PERMISSIONS', None)
    if not id:
        warnings.warn("django-socialregistration: Please update your settings.py and add a FACEBOOK_APP_ID key", Warning)
    return {'facebook_app_id': id, 'facebook_api_key': key, 'is_https' : bool(_https()), 'facebook_req_perms' : perms }

@register.inclusion_tag('socialregistration/facebook_button.html', takes_context=True)
def facebook_button(context, button=None):
    if not 'request' in context:
        raise AttributeError, 'Please add the ``django.core.context_processors.request`` context processors to your settings.TEMPLATE_CONTEXT_PROCESSORS set'
    logged_in = context['request'].user.is_authenticated()
    if 'next' in context:
        next = context['next']
    else:
        next = None
    return dict(next=next, logged_in=logged_in, button=button, request=context['request'])
