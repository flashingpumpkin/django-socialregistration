from django import template

register = template.Library()

@register.inclusion_tag('socialregistration/openid_form.html', takes_context=True)
def openid_form(context):
    if not 'request' in context:
        raise AttributeError, 'Please add the ``django.core.context_processors.request`` context processors to your settings.TEMPLATE_CONTEXT_PROCESSORS set'
    logged_in = context['request'].user.is_authenticated()
    next = context['next'] if 'next' in context else None
    return dict(next=next, logged_in=logged_in)
