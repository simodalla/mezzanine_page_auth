# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageAuthGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('group', models.ForeignKey(verbose_name='group', to='auth.Group', related_name='pages')),
                ('page', models.ForeignKey(verbose_name='page', to='pages.Page')),
            ],
            options={
                'ordering': ('group',),
                'verbose_name': 'Page Auth Group',
                'verbose_name_plural': 'Page Auth Group',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='pageauthgroup',
            unique_together=set([('page', 'group')]),
        ),
    ]
