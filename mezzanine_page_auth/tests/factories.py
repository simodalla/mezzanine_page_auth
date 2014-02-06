# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import factory

from django.contrib.auth.models import User, Group

from mezzanine.pages.models import RichTextPage, Link

from ..models import PageAuthGroup

DOMAIN = 'comune.zolapredosa.bo.it'


class GroupF(factory.DjangoModelFactory):
    FACTORY_FOR = Group
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = factory.Sequence(lambda n: 'group_%s' % n)


class OperatorsGroupF(GroupF):
    name = 'goperators'


class AdminsGroupF(GroupF):
    name = 'gadmins'


class UserF(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user_%s' % n)
    password = factory.Sequence(lambda n: 'user_%s' % n)
    email = factory.LazyAttribute(lambda o: '{}@{}'.format(o.username, DOMAIN))
    is_staff = True
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserF, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)


class AdminUserF(UserF):
    username = 'admin'
    password = 'admin'
    email = 'admin@{}'.format(DOMAIN)
    is_superuser = True


class RichTextPageF(factory.DjangoModelFactory):
    FACTORY_FOR = RichTextPage
    FACTORY_DJANGO_GET_OR_CREATE = ('title',)

    status = 2
    title = factory.Sequence(lambda n: u'richtextpage_{}'.format(n))
    description = factory.LazyAttribute(
        lambda page: u'Description of {}'.format(page.title))
    content = factory.LazyAttribute(
        lambda page: u'<h1>{0}</h1><p>Content of page'
                     u' "{0}"</p>'.format(page.title))
    login_required = False
    parent = None


class LinkF(factory.DjangoModelFactory):
    FACTORY_FOR = Link
    FACTORY_DJANGO_GET_OR_CREATE = ('title',)

    status = 2
    title = factory.Sequence(lambda n: u'richtextpage_{}'.format(n))
    slug = factory.LazyAttribute(lambda a: '{}'.format(a.title))
    login_required = False
    parent = None


class RichTextPageWithLoginF(RichTextPageF):
    title = factory.Sequence(
        lambda n: u'richtextpage_{} with login'.format(n))
    login_required = True


class PageAuthGroupF(factory.DjangoModelFactory):
    FACTORY_FOR = PageAuthGroup

    group = factory.SubFactory(GroupF)
    page = factory.SubFactory(RichTextPageWithLoginF)


class GroupWithPageF(GroupF):
    membership = factory.RelatedFactory(PageAuthGroupF, 'group')


class RichTextPageWithGroupF(RichTextPageWithLoginF):
    membership = factory.RelatedFactory(PageAuthGroupF, 'page',
                                        group__name='goperators')
