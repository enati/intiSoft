# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0089_auto_20160428_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='fecha',
            field=models.DateField(null=True, verbose_name=b'Fecha'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='numero',
            field=models.CharField(max_length=15, verbose_name=b'Nro. Factura'),
        ),
    ]
