# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0135_auto_20170417_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_aceptado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Aceptaci\xc3\xb3n', blank=True),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_realizado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Realizaci\xc3\xb3n', blank=True),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='nro_revision',
            field=models.IntegerField(default=0, verbose_name=b'Nro. Revisi\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='revisionar',
            field=models.BooleanField(default=False, verbose_name=b'Revisionar'),
        ),
    ]
