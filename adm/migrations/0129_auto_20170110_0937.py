# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0128_auto_20170109_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sot',
            name='expediente',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Expediente', blank=True),
        ),
        migrations.AlterField(
            model_name='sot',
            name='ot',
            field=models.CharField(max_length=15, null=True, verbose_name=b'Nro. OT', blank=True),
        ),
    ]
