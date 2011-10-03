from django import template
from socialregistration.templatetags import button

register = template.Library()

register.tag('github_button', button('socialregistration/github/github_button.html'))