# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0060_auto_20151228_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cuit',
            field=models.CharField(max_length=11, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nro_usuario',
            field=models.PositiveIntegerField(unique=True, null=True, blank=True),
        ),
    ]
