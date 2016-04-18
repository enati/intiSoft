# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0066_auto_20151228_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='nro_usuario',
            field=models.CharField(blank=True, max_length=6, unique=True, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\d{5}$', message=b'Se esperan 5 digitos')]),
        ),
    ]
