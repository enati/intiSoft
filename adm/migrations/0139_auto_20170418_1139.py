# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0138_auto_20170418_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumento',
            name='detalle',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Detalle', blank=True),
        ),
    ]
