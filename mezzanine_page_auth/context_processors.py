# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def page_auth(request):
    """
    Returns context variables required for check authorizations on Mezzanine
    pages.

    If there is no 'unauthorized_pages' attribute in the request, uses empty
    list (all pages are authorized and accesible).
    """
    unauthorized_pages = []
    if hasattr(request, 'unauthorized_pages'):
        unauthorized_pages = request.unauthorized_pages

    return {
        'unauthorized_pages': unauthorized_pages,
    }
