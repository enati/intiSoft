# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-13 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0167_auto_20180409_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='observaciones',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name=b'Observaciones'),
        ),
    ]
