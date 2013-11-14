# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def can_view_page(user, page):
    return True