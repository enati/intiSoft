# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0143_auto_20170418_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='si',
            name='ejecutor',
            field=models.CharField(max_length=4, verbose_name=b'UT Ejecutora', choices=[(b'LIA', b'LIA'), (b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'LIM4', b'LIM4'), (b'LIM5', b'LIM5'), (b'LIM6', b'LIM6'), (b'EXT', b'EXT'), (b'SIS', b'SIS'), (b'DES', b'DES'), (b'CAL', b'CAL'), (b'MEC', b'MEC'), (b'ML', b'ML')]),
        ),
        migrations.AlterField(
            model_name='si',
            name='fecha_fin_real',
            field=models.DateField(null=True, verbose_name=b'Fecha de Finalizacion', blank=True),
        ),
        migrations.AlterField(
            model_name='si',
            name='fecha_prevista',
            field=models.DateField(null=True, verbose_name=b'Fecha Prevista', blank=True),
        ),
        migrations.AlterField(
            model_name='si',
            name='solicitante',
            field=models.CharField(max_length=4, verbose_name=b'UT Solicitante', choices=[(b'LIA', b'LIA'), (b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'LIM4', b'LIM4'), (b'LIM5', b'LIM5'), (b'LIM6', b'LIM6'), (b'EXT', b'EXT'), (b'SIS', b'SIS'), (b'DES', b'DES'), (b'CAL', b'CAL'), (b'MEC', b'MEC'), (b'ML', b'ML')]),
        ),
    ]
