from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

def resolve(what, context):
    try:
        return template.Variable(what).resolve(context)
    except template.VariableDoesNotExist:
        return what

def get_bits(token):
    bits = token.split_contents()
    return [bit.replace("'","").replace('"','') for bit in bits[1:]]

def button(template_name):
    def tag(parser, token):
        return ButtonTag(template_name, get_bits(token))
    return tag

class ButtonTag(template.Node):
    def __init__(self, template_name, params = []):
        self.template_name = template_name
        self.params = params

    def render(self, context):
        if not 'request' in context:
            raise AttributeError(_("Please add 'django.core.context_processors.request' "
                "'to your settings.TEMPLATE_CONTEXT_PROCESSORS'"))

        button = ''.join([resolve(bit, context) for bit in self.params])
        
        return template.loader.render_to_string(self.template_name, {
                'button': button}, context)
