# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-03 14:45
from __future__ import unicode_literals

import adm.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0165_auto_20180103_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdt',
            name='anio',
            field=models.CharField(choices=[(b'2017', b'2017'), (b'2018', b'2018'), (b'2019', b'2019'), (b'2020', b'2020')], default=adm.models.yearNow, max_length=4, null=True, verbose_name=b'A\xc3\xb1o'),
        ),
        migrations.AlterField(
            model_name='pdt',
            name='cantidad_contratos',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name=b'Cantidad de OT/SOT/RUT Anuales'),
        ),
        migrations.AlterField(
            model_name='pdt',
            name='cantidad_servicios',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name=b'Cantidad de Servicios'),
        ),
        migrations.AlterField(
            model_name='pdt',
            name='facturacion_prevista',
            field=models.FloatField(default=0, null=True, verbose_name=b'Facturaci\xc3\xb3n Anual Prevista por OT'),
        ),
        migrations.AlterField(
            model_name='pdt',
            name='generacion_neta',
            field=models.FloatField(default=0, null=True, verbose_name=b'Generaci\xc3\xb3n Neta'),
        ),
        migrations.AlterField(
            model_name='pdt',
            name='tipo',
            field=models.CharField(choices=[(b'POA', b'POA'), (b'PDI', b'PDI')], max_length=3, null=True, verbose_name=b'Tipo de Plan'),
        ),
    ]