"""
Created on 24.09.2009

@author: alen
"""
from django import template

register = template.Library()

@register.inclusion_tag('socialregistration/openid_form.html')
def openid_form():
    return {}
