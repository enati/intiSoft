# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0132_auto_20170113_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otml',
            name='vpu',
        ),
        migrations.AddField(
            model_name='otml',
            name='vpr',
            field=models.CharField(max_length=10, null=True, verbose_name=b'VPR', blank=True),
        ),
        migrations.AlterField(
            model_name='otml',
            name='vpuu',
            field=models.CharField(max_length=10, null=True, verbose_name=b'VPUU', blank=True),
        ),
    ]
