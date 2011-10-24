from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('linkedin_button', button('socialregistration/linkedin/linkedin_button.html'))