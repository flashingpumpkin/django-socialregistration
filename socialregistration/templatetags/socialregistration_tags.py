import re
from django import template
from django.template import resolve_variable, Variable

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


@register.tag
def open_id_errors(parser, token):
    """
    Retrieve OpenID errors and the provider that caused them from session for display to the user.
    """

    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    m = re.search(r'(\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    request = m.groups()[0]
    return OpenIDErrorsNode(request)

class OpenIDErrorsNode(template.Node):
    def __init__(self, request):
        self.request = Variable(request)

    def render(self, context):
        request = self.request.resolve(context)
        context['openid_error'] = request.session.get('openid_error', False)
        context['openid_provider'] = request.session.get('openid_provider', '')

        # clear the error once it's been displayed once
        if request.session.get('openid_error', False):
            del request.session['openid_error']
        if request.session.get('openid_provider', False):
            del request.session['openid_provider']

        return u''
