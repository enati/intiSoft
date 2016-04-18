# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0067_auto_20151228_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec',
            name='codigo',
            field=models.CharField(max_length=14, verbose_name=b'Codigo', validators=[django.core.validators.RegexValidator(b'^\\d{14}$')]),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cuit',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(b'^\\d{11}$')]),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nro_usuario',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(b'^\\d{5}$')]),
        ),
    ]
