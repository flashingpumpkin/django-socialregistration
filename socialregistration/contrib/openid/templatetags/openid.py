from django import template
from socialregistration.templatetags import resolve, get_bits

register = template.Library()

@register.tag
def openid_form(parser, token):
    """
    Render OpenID form. Allows to pre set the provider::

    	{% openid_form "https://www.google.com/accounts/o8/id" %}

    Also creates custom button URLs by concatenating all arguments
    after the provider's URL

    	{% openid_form "https://www.google.com/accounts/o8/id" STATIC_URL "image/for/google.jpg" %}

    """

    bits = get_bits(token)

    if len(bits) > 1:
        return FormNode(bits[0], bits[1:])
    if len(bits) == 1:
        return FormNode(bits[0])
    return FormNode(None)

class FormNode(template.Node):
    def __init__(self, provider, params = []):
        self.provider = provider
        self.params = params

    def render(self, context):
        if self.provider:
            provider = resolve(self.provider, context)
        else:
            provider = None

        if self.params:
            button = ''.join([resolve(bit, context) for bit in self.params])
        else:
            button = None

        return template.loader.render_to_string(
            'socialregistration/openid/form.html',{
                'provider': provider,
                'button': button},
            context_instance = context)
