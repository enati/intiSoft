# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0063_auto_20151228_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cuit',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(b'^\\d{11}$')]),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nro_usuario',
            field=models.CharField(blank=True, max_length=6, unique=True, null=True, validators=[django.core.validators.RegexValidator(b'^\\d{6}$')]),
        ),
    ]
