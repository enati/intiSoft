# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0144_auto_20170418_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot_linea',
            name='codigo',
            field=models.CharField(max_length=14, verbose_name=b'C\xc3\xb3digo', validators=[django.core.validators.RegexValidator(b'^\\d{14}$')]),
        ),
        migrations.AlterField(
            model_name='ot_linea',
            name='observaciones',
            field=models.TextField(max_length=100, verbose_name=b'Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='ot_linea',
            name='precio',
            field=models.FloatField(verbose_name=b'Precio Unitario'),
        ),
    ]
