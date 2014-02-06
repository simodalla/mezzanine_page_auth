# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mock import patch, Mock
from django.contrib.admin import AdminSite
from django.contrib.messages import INFO
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from mezzanine.pages.models import RichTextPage, Link
from ..models import PageAuthGroup
from ..admin import PageAuthGroupAdmin, LinkAuthGroupAdmin
from .factories import UserF, GroupF, RichTextPageF, LinkF


class PageAuthGroupAdminMixinSaveRelatedTest(TestCase):

    def setUp(self):
        self.user = UserF()
        self.prefix_url = 'admin:pages_richtextpage_'
        self.factory = RequestFactory()
        self.mock_form = Mock()
        self.mock_form_formset = Mock()
        self.parent_page = RichTextPageF()
        [PageAuthGroup.objects.create(
            page=self.parent_page, group=GroupF()) for i in range(0, 3)]

    def tearDown(self):
        self.mock_form.reset_mock()
        self.mock_form_formset.reset_mock()

    def get_request(self, viewname, args=None, kwargs=None, query_string=None):
        url = reverse(viewname, args=args, kwargs=kwargs)
        if query_string:
            url += '?' + query_string
        return self.factory.get(url)

    @patch('mezzanine_page_auth.admin.PageAuthGroupAdmin.message_user')
    @patch('mezzanine_page_auth.admin.PageAdmin.save_related')
    def test_add_page_with_parent_and_without_pag_inserted(
            self, mock_save_related, mock_message_user):
        """
        save_related() on adding page and without PageAuthGroup inserted
        set related PageAuthGroup objects as parent
        """
        page_admin = PageAuthGroupAdmin(RichTextPage, AdminSite())
        page = RichTextPageF()
        page.parent = self.parent_page
        page.save()
        self.mock_form.instance = page
        request = self.get_request(self.prefix_url + 'add',
                                   query_string='parent={}'.format(
                                       self.parent_page.pk))
        page_admin.save_related(
            request, self.mock_form, self.mock_form_formset, False)
        mock_save_related.assert_called_once_with(request, self.mock_form,
                                                  self.mock_form_formset, False)
        self.assertListEqual(
            sorted(self.parent_page.pageauthgroup_set.values_list('group_id',
                                                                  flat=True)),
            sorted(page.pageauthgroup_set.values_list('group_id', flat=True)))
        mock_message_user.assert_called_once_with(
            request,
            'The page "{}" has inherited the protections from'
            ' parent "{}"'.format(page.title, self.parent_page.title),
            INFO)

    @patch('mezzanine_page_auth.admin.PageAuthGroupAdmin.message_user')
    @patch('mezzanine_page_auth.admin.PageAdmin.save_related')
    def test_add_page_with_parent_and_with_pag_inserted(
            self, mock_save_related, mock_message_user):
        """
        save_related() on adding page and with PageAuthGroup inserted
        not set related PageAuthGroup objects as parent
        """
        page_admin = PageAuthGroupAdmin(RichTextPage, AdminSite())
        page = RichTextPageF()
        page.parent = self.parent_page
        page.save()
        pags_page = [PageAuthGroup.objects.create(
            page=page, group=GroupF()) for i in range(0, 2)]

        self.mock_form.instance = page
        request = self.get_request(self.prefix_url + 'add',
                                   query_string='parent={}'.format(
                                       self.parent_page.pk))
        with patch('mezzanine_page_auth.admin.PageAuthGroup.objects.create') \
                as mock_create:
            page_admin.save_related(
                request, self.mock_form, self.mock_form_formset, False)
            mock_save_related.assert_called_once_with(
                request, self.mock_form, self.mock_form_formset, False)
            self.assertListEqual(
                sorted([pag.group_id for pag in pags_page]),
                sorted(page.pageauthgroup_set.values_list('group_id',
                                                          flat=True)))
            self.assertFalse(mock_message_user.called)
            self.assertFalse(mock_create.called)

    @patch('mezzanine_page_auth.admin.LinkAuthGroupAdmin.message_user')
    @patch('mezzanine_page_auth.admin.PageAdmin.save_related')
    def test_add_link_with_parent_and_without_pag_inserted(
            self, mock_save_related, mock_message_user):
        """
        save_related() on adding page and without PageAuthGroup inserted
        set related PageAuthGroup objects as parent
        """
        page_admin = LinkAuthGroupAdmin(Link, AdminSite())
        page = LinkF()
        page.parent = self.parent_page
        page.save()
        self.mock_form.instance = page
        request = self.get_request(self.prefix_url + 'add',
                                   query_string='parent={}'.format(
                                       self.parent_page.pk))
        page_admin.save_related(
            request, self.mock_form, self.mock_form_formset, False)
        mock_save_related.assert_called_once_with(request,
                                                  self.mock_form,
                                                  self.mock_form_formset,
                                                  False)
        self.assertListEqual(
            sorted(self.parent_page.pageauthgroup_set.values_list(
                'group_id',
                flat=True)),
            sorted(page.pageauthgroup_set.values_list('group_id',
                                                      flat=True)))
        mock_message_user.assert_called_once_with(
            request,
            'The page "{}" has inherited the protections from'
            ' parent "{}"'.format(page.title, self.parent_page.title),
            INFO)

    @patch('mezzanine_page_auth.admin.LinkAuthGroupAdmin.message_user')
    @patch('mezzanine_page_auth.admin.LinkAdmin.save_related')
    def test_add_link_with_parent_and_with_pag_inserted(
            self, mock_save_related, mock_message_user):
        """
        save_related() on adding page and with PageAuthGroup inserted
        not set related PageAuthGroup objects as parent
        """
        page_admin = LinkAuthGroupAdmin(Link, AdminSite())
        page = LinkF()
        page.parent = self.parent_page
        page.save()
        pags_page = [PageAuthGroup.objects.create(
            page=page, group=GroupF()) for i in range(0, 2)]

        self.mock_form.instance = page
        request = self.get_request(self.prefix_url + 'add',
                                   query_string='parent={}'.format(
                                       self.parent_page.pk))
        with patch(
                'mezzanine_page_auth.admin.PageAuthGroup.objects.create') \
                as mock_create:
            page_admin.save_related(
                request, self.mock_form, self.mock_form_formset, False)
            mock_save_related.assert_called_once_with(
                request, self.mock_form, self.mock_form_formset, False)
            self.assertListEqual(
                sorted([pag.group_id for pag in pags_page]),
                sorted(page.pageauthgroup_set.values_list('group_id',
                                                          flat=True)))
            self.assertFalse(mock_message_user.called)
            self.assertFalse(mock_create.called)
