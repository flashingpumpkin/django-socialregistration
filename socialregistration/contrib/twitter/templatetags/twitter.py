from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('twitter_button', button('socialregistration/twitter/twitter_button.html'))