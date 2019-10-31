# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-06-10 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0185_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rut',
            name='codigo',
            field=models.CharField(default=b'7100000000', error_messages={b'unique': b'Ya existe una RUT con ese n\xc3\xbamero.'}, max_length=11, unique=True, verbose_name=b'Nro. RUT'),
        ),
        migrations.AlterField(
            model_name='sot',
            name='codigo',
            field=models.CharField(default=b'7100000000', error_messages={b'unique': b'Ya existe una SOT con ese n\xc3\xbamero.'}, max_length=11, unique=True, verbose_name=b'Nro. SOT'),
        ),
    ]