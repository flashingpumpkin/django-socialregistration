from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('openid_form', button('socialregistration/openid/form.html'))
