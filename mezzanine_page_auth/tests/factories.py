# -*- coding: utf-8 -*-

import factory

from django.contrib.auth.models import User, Group

from mezzanine.pages.models import RichTextPage

from ..models import PageAuthGroup

DOMAIN = 'comune.zolapredosa.bo.it'


class GroupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Group
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = factory.Sequence(lambda n: 'group_%s' % n)


class OperatorsGroupFactory(GroupFactory):
    name = 'goperators'


class AdminsGroupFactory(GroupFactory):
    name = 'gadmins'


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user_%s' % n)
    password = factory.Sequence(lambda n: 'user_%s' % n)
    email = factory.LazyAttribute(lambda o: '{}@{}'.format(o.username, DOMAIN))
    is_staff = True
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
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


class AdminUserFactory(UserFactory):
    username = 'admin'
    password = 'admin'
    email = 'admin@{}'.format(DOMAIN)
    is_superuser = True


class RichTextPageFactory(factory.DjangoModelFactory):
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


class RichTextPageWithLoginFactory(RichTextPageFactory):
    title = factory.Sequence(
        lambda n: u'richtextpage_{} with login'.format(n))
    login_required = True


class PageAuthGroupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PageAuthGroup

    group = factory.SubFactory(GroupFactory)
    page = factory.SubFactory(RichTextPageWithLoginFactory)


class GroupWithPageFactory(GroupFactory):
    membership = factory.RelatedFactory(PageAuthGroupFactory, 'group')


class RichTextPageWithGroupFactory(RichTextPageWithLoginFactory):
    membership = factory.RelatedFactory(PageAuthGroupFactory, 'page',
                                        group__name='goperators')