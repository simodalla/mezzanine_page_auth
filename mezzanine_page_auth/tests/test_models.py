# -*- coding: utf-8 -*-

from unittest import skip

from django.contrib.auth.models import Group, User, AnonymousUser
from django.test import TestCase

from mezzanine.pages.models import Page
from ..models import PageAuthGroup
from .factories import (GroupWithPageFactory, UserFactory, AdminUserFactory,
                        RichTextPageFactory)


class UnauthorizedListPagesPageAuthGroupTest(TestCase):

    def setUp(self):
        self.n_groups = 3
        self.n_pages = 3
        self.groups = [GroupWithPageFactory() for n in range(0, self.n_groups)]
        self.users = [UserFactory.create(username='user_of_{}'.format(g.name),
                                         groups=(g,)) for g in self.groups]
        self.pages_no_group = [RichTextPageFactory()
                               for n in range(0, self.n_pages)]

    @skip("Printing fixtures data for debug")
    def test_fixtures(self):
        print("************************")
        print(User.objects.all())
        print(Group.objects.all())
        print(Page.objects.all())
        print("************************")
        ##print(self.goperators.page_set.all())
        #
        #for page in Page.objects.all():
        #    print("********")
        #    print(page.slug)
        #    response = self.client.get('/' + page.slug + '/')
        #    try:
        #        print(response.context['user'])
        #    except TypeError:
        #        pass
        #    print(response.status_code)
        #    print(page.groups.all())
        #    print("********")

    def test_unauthorized_list_pages_with_anonymous_user(self):
        """
        Test that the call of unauthorized_list_pages with an anonymous user
        returns a list with all page id's of pages with associated groups
        """
        pks = [pk for pks in [g.page_set.values_list('pk', flat=True)
                              for g in self.groups] for pk in pks]
        self.assertListEqual(
            pks, PageAuthGroup.unauthorized_pages(AnonymousUser()))

    def test_unauthorized_list_pages_with_admin_user(self):
        """
        Test that the call of unauthorized_list_pages with an admin user
        returns an empty list
        """
        self.assertListEqual(
            [], PageAuthGroup.unauthorized_pages(AdminUserFactory()))

    def test_unauthorized_list_pages_with_user_without_group(self):
        """
        Test that the call of unauthorized_list_pages with an user without
        associated groups
        """
        pks = [pk for pks in [g.page_set.values_list('pk', flat=True)
                              for g in self.groups] for pk in pks]
        self.assertListEqual(
            pks, PageAuthGroup.unauthorized_pages(
                UserFactory.create(username='user_without_group')))

    def test_unauthorized_list_pages_with_user_with_one_group(self):
        """
        Test that the call of unauthorized_list_pages with an user with one
        associated group
        """
        user = self.users[0]
        pks_auth = [pk for pks in [g.page_set.values_list('pk', flat=True)
                                   for g in user.groups.all()] for pk in pks]
        pks = list(set(PageAuthGroup.objects.exclude(
            pk__in=pks_auth).values_list('page__pk', flat=True)))
        self.assertListEqual(pks, PageAuthGroup.unauthorized_pages(user))

    #def test_user_access_to_page_without_group(self):
    #    self.assertTrue(check_page_access(self.app_operator,
    #                                      self.pages_no_group[0]))
    #
    #def test_user_access_to_page_with_other_group(self):
    #    self.assertFalse(check_page_access(self.app_admin,
    #                                       self.pages_with_group[0]))
    #
    #def test_user_access_to_page_with_group(self):
    #    self.assertTrue(check_page_access(self.app_operator,
    #                                      self.pages_with_group[0]))
