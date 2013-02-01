from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('google_button', button('socialregistration/google/google_button.html'))