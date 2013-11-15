# -*- coding: utf-8 -*-

from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.models import Page, RichTextPage, Link
from mezzanine.pages.admin import PageAdmin, LinkAdmin

from .models import PageAuthGroup


class PageAuthGroupInline(admin.TabularInline):
    model = PageAuthGroup
    extra = 1


page_inlines = deepcopy(PageAdmin.inlines)
page_inlines.append(PageAuthGroupInline)
link_inlines = deepcopy(LinkAdmin.inlines)
link_inlines.append(PageAuthGroupInline)


class PageAuthGroupAdmin(PageAdmin):
    """
    Admin class for subclassing mezzanine 'PageAdmin' for expose new field
    ``groups``  to the admin interface.
    """
    inlines = page_inlines


class LinkAuthGroupAdmin(LinkAdmin):
    """
    Admin class for subclassing mezzanine 'LinkAdmin' for expose new field
    ``groups``  to the admin interface.
    """
    inlines = page_inlines


admin.site.unregister(Page)
admin.site.unregister(Link)
admin.site.unregister(RichTextPage)
admin.site.register(Page, PageAuthGroupAdmin)
admin.site.register(Link, LinkAuthGroupAdmin)
admin.site.register(RichTextPage, PageAuthGroupAdmin)