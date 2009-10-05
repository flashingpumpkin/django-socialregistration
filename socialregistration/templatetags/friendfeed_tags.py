"""
Created on 25.09.2009

@author: alen
"""
from django import template

register = template.Library()

@register.inclusion_tag('socialregistration/friendfeed_button.html')
def friendfeed_button():
    return {}