from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('foursquare_button', button('socialregistration/foursquare/foursquare_button.html'))
