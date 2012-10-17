from django import template


register = template.Library()

@register.inclusion_tag('socialregistration/openid/form.html', takes_context=True)
def openid_form(context, provider=None, *params):
    button = ''.join(params)
    return {
        'provider': provider,
        'button': button,
        'request': context['request']
    }

