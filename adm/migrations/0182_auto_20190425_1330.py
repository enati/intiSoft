# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-25 16:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0181_auto_20190416_1007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ofertatec',
            options={'ordering': ['codigo'], 'permissions': (('restore_ofertatec', 'Can restore ofertatec'),)},
        ),
    ]
