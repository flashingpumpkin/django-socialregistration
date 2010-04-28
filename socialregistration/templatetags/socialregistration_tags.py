from django import template

register = template.Library()

@register.tag
def social_csrf_token(parser, token):
    """
    Wrapper around the ``{% csrf_token %}`` template tag to make socialregistration
    work with both Django v1.2 and Django < v1.2
    """
    return CsrfNode()
    
class CsrfNode(template.Node):
    def render(self, context):
        try:
            from django.template.defaulttags import CsrfTokenNode
            return CsrfTokenNode().render(context)
        except ImportError:
            return u''