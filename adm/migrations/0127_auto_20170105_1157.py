# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0126_auto_20161228_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sot',
            name='ot',
            field=models.CharField(max_length=8, null=True, verbose_name=b'Nro. OT', blank=True),
        ),
    ]
