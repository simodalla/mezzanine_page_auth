# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured

from django.http import HttpResponseForbidden

from mezzanine.pages.models import Page

from .models import PageAuthGroup


class PageAuthMiddleware(object):
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The PageAuthMiddleware middleware requires the"
                " authentication middleware to be installed. Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the PageAuthMiddleware class.")
        slug = request.path
        if slug != '/':
            slug = slug.strip('/')
        request.unauthorized_pages = PageAuthGroup.unauthorized_pages(
            request.user)
        try:
            page = Page.objects.get(slug=slug)
            if page.pk in request.unauthorized_pages:
                return HttpResponseForbidden()
        except Page.DoesNotExist:
            pass