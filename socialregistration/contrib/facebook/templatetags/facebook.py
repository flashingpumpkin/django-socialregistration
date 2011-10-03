from django import template

from socialregistration.templatetags import button

register = template.Library()

register.tag('facebook_button', button('socialregistration/facebook/facebook_button.html'))