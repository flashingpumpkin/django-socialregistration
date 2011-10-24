from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('tumblr_button', button('socialregistration/tumblr/tumblr_button.html'))
