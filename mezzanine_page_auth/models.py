# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.pages.models import Page


class PageAuthGroup(models.Model):
    page = models.ForeignKey(Page, verbose_name=_('page'))
    group = models.ForeignKey(Group, verbose_name=_('group'),
                              related_name='pages')

    class Meta:
        verbose_name = _("Page Auth Group")
        verbose_name_plural = _("Page Auth Group")
        ordering = ("group",)

    def __unicode__(self):
        return u"{}: {} has {}".format(self._meta.module_name, self.group.name,
                                       self.page)

    @classmethod
    def unauthorized_pages(cls, user):
        """
        Returns a list of pks of page that user is unauthorized to access
        """
        if user.is_superuser:
            return list()
        groups = user.groups.all()
        if user.is_anonymous() or len(groups) == 0:
            return list(set(cls.objects.values_list('page__pk', flat=True)))
        return list((cls.objects.exclude(group__in=groups).values_list(
            'page__pk', flat=True)))

