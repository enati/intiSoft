# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-26 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0169_auto_20180418_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot_linea',
            name='cant_horas',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name=b'Horas'),
        ),
        migrations.AlterField(
            model_name='ot_linea',
            name='cantidad',
            field=models.PositiveIntegerField(default=1, verbose_name=b'Cantidad'),
        ),
    ]
