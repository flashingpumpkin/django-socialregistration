from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

def button(template):
    def tag(parser, token):
        bits = token.split_contents()
        try:
            # Is a custom button passed in?
            return ButtonTag(template, bits[1][1:-1])
        except IndexError:
            # No custom button
            return ButtonTag(template)
    return tag

class ButtonTag(template.Node):
    def __init__(self, template, button = None):
        self.template = template
        self.button = button
    
    def render(self, context):
        if not 'request' in context:
            raise AttributeError(_("Please add 'django.core.context_processors.request' "
                "'to your settings.TEMPLATE_CONTEXT_PROCESSORS'"))
        
        return template.loader.render_to_string(self.template, {'button': self.button}, context)
