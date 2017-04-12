# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0133_auto_20170120_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otml',
            name='vpr',
            field=models.CharField(max_length=8, null=True, verbose_name=b'VPR', blank=True),
        ),
        migrations.AlterField(
            model_name='otml',
            name='vpuu',
            field=models.CharField(max_length=8, null=True, verbose_name=b'VPUU', blank=True),
        ),
    ]
