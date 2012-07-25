from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('instagram_button', button('socialregistration/instagram/instagram_button.html'))