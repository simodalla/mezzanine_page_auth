# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_page_auth', '0001_initial'),
        ('auth', '0001_initial'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mezzanine.pages.page',
            name='groups',
            field=models.ManyToManyField(blank=True, null=True, verbose_name='groups', to='auth.Group', through='mezzanine_page_auth.PageAuthGroup'),
            preserve_default=True,
        ),
    ]
