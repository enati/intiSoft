# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-27 17:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0161_auto_20171227_1448'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pdt',
            options={'ordering': ['anio', 'codigo'], 'permissions': (('read_pdt', 'Can read pdt'),)},
        ),
    ]
