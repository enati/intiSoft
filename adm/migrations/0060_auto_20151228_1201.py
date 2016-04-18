# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0059_auto_20151222_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cuit',
            field=models.CharField(max_length=11, validators=[django.core.validators.MaxValueValidator(99999999999)]),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nro_usuario',
            field=models.PositiveIntegerField(blank=True, unique=True, null=True, validators=[django.core.validators.MaxValueValidator(99999)]),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rubro',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
