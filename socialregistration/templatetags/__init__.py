from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

def button(template_name):
    def tag(parser, token):
        bits = token.split_contents()
        if len(bits) > 1:
            return ButtonTag(template_name, *bits[1:])
        else:
            # No custom button
            return ButtonTag(template_name)
    return tag

class ButtonTag(template.Node):
    def __init__(self, template_name, *input):
        self.template = template_name
        self.input = input

    def render(self, context):
        output = []
        for bit in self.input:
            if not (bit[0] == bit[-1] and bit[0] in ('"', "'")):
                output.append(template.Variable(bit).resolve(context))
            else:
                output.append(bit[1:-1])
        self.button = ''.join(output)

        if not 'request' in context:
            raise AttributeError(_("Please add 'django.core.context_processors.request' "
                "'to your settings.TEMPLATE_CONTEXT_PROCESSORS'"))

        return template.loader.render_to_string(self.template, {'button': self.button, 'next': context.get('next', None)}, context)
