# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageAuthGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(verbose_name='group', to='auth.Group', related_name='pages')),
                ('page', models.ForeignKey(to='pages.Page', verbose_name='page')),
            ],
            options={
                'verbose_name': 'Page Auth Group',
                'ordering': ('group',),
                'verbose_name_plural': 'Page Auth Group',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='pageauthgroup',
            unique_together=set([('page', 'group')]),
        ),
    ]
