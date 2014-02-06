# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseForbidden
from django.test import TestCase

from .factories import (OperatorsGroupF, AdminsGroupF,
                        UserF, RichTextPageF,
                        RichTextPageWithGroupF)
from ..middleware import PageAuthMiddleware


class PageAuthMiddlewareTest(TestCase):

    def setUp(self):
        self.goperators = OperatorsGroupF()
        self.gadmins = AdminsGroupF()
        self.app_operator = UserF.create(username='app_operator',
                                           groups=(self.goperators,))
        self.app_admin = UserF.create(username='app_admin',
                                        groups=(self.gadmins,))
        self.n_pages = 3
        self.pages_no_group = [RichTextPageF()
                               for n in range(0, self.n_pages)]
        self.pages_with_group = [RichTextPageWithGroupF()
                                 for n in range(0, self.n_pages)]
        self.middlware = PageAuthMiddleware()

    def test_anonymous_user_access_to_page_without_group(self):
        """
        Test that method 'process_request' of PageAuthMiddleware middleware
        return None if user of request is an 'AnonymousUser' and the request
        page don't have groups associated.
        """
        mock_request = Mock()
        mock_request.user = AnonymousUser()
        mock_request.path = self.pages_no_group[0].slug
        self.assertIsNone(self.middlware.process_request(mock_request))

    def test_anonymous_user_access_to_page_with_group(self):
        """
        Test that method 'process_request' of PageAuthMiddleware middleware
        return None if user of request is an 'AnonymousUser' and the request
        page have groups associated.
        """
        mock_request = Mock()
        mock_request.user = AnonymousUser()
        mock_request.path = self.pages_with_group[0].slug
        self.assertIsInstance(self.middlware.process_request(mock_request),
                              HttpResponseForbidden)

    def test_user_access_to_page_without_group(self):
        """
        Test that method 'process_request' of PageAuthMiddleware middleware
        return None (page is accessible) if user of request is a django user
        and the request page don't have groups associated.
        """
        mock_request = Mock()
        mock_request.user = self.app_operator
        mock_request.path = self.pages_no_group[0].slug
        self.assertIsNone(self.middlware.process_request(mock_request))

    def test_user_access_to_page_with_other_group(self):
        """
        Test that method 'process_request' of PageAuthMiddleware middleware
        return an HttpResponseForbidden object if user of request is a django
        user who is not a member of group associated with the page of the
        request
        """
        mock_request = Mock()
        mock_request.user = self.app_admin
        mock_request.path = self.pages_with_group[0].slug
        self.assertIsInstance(self.middlware.process_request(mock_request),
                              HttpResponseForbidden)

    def test_user_access_to_page_with_group(self):
        """
        Test that method 'process_request' of PageAuthMiddleware middleware
        return None if user of request is a django user member of group
        associated with the page of the request
        """
        mock_request = Mock()
        mock_request.user = self.app_operator
        mock_request.path = self.pages_with_group[0].slug
        self.assertIsNone(self.middlware.process_request(mock_request))
