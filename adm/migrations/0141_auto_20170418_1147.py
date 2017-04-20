# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0140_auto_20170418_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sot',
            name='fecha_envio_cc',
            field=models.DateField(null=True, verbose_name=b'Fecha de Envio a CC', blank=True),
        ),
        migrations.AlterField(
            model_name='sot',
            name='fecha_envio_ut',
            field=models.DateField(null=True, verbose_name=b'Fecha de Envio a la UT', blank=True),
        ),
        migrations.AlterField(
            model_name='sot',
            name='fecha_prevista',
            field=models.DateField(verbose_name=b'Fecha Prevista'),
        ),
        migrations.AlterField(
            model_name='sot',
            name='firmada',
            field=models.BooleanField(verbose_name=b'Retorno Firmada'),
        ),
        migrations.AlterField(
            model_name='sot',
            name='solicitante',
            field=models.CharField(max_length=4, verbose_name=b'Solicitante', choices=[(b'LIA', b'LIA'), (b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'LIM4', b'LIM4'), (b'LIM5', b'LIM5'), (b'LIM6', b'LIM6'), (b'EXT', b'EXT'), (b'SIS', b'SIS'), (b'DES', b'DES'), (b'CAL', b'CAL'), (b'MEC', b'MEC'), (b'ML', b'ML')]),
        ),
    ]
