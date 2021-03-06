# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0142_auto_20170418_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rut',
            name='descuento_fijo',
            field=models.BooleanField(verbose_name=b'Descuento Fijo'),
        ),
        migrations.AlterField(
            model_name='rut',
            name='deudor',
            field=models.ForeignKey(related_name='rut_deudor', on_delete=django.db.models.deletion.PROTECT, verbose_name=b'UT Deudora', to='adm.Usuario'),
        ),
        migrations.AlterField(
            model_name='rut',
            name='ejecutor',
            field=models.ForeignKey(related_name='rut_ejecutor', on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name=b'UT Ejecutora', to='adm.Usuario'),
        ),
        migrations.AlterField(
            model_name='rut',
            name='fecha_envio_cc',
            field=models.DateField(null=True, verbose_name=b'Fecha de env\xc3\xado a CC', blank=True),
        ),
        migrations.AlterField(
            model_name='rut',
            name='fecha_envio_ut',
            field=models.DateField(null=True, verbose_name=b'Fecha de Env\xc3\xado a la UT', blank=True),
        ),
        migrations.AlterField(
            model_name='rut',
            name='fecha_prevista',
            field=models.DateField(verbose_name=b'Fecha Prevista'),
        ),
        migrations.AlterField(
            model_name='rut',
            name='firmada',
            field=models.BooleanField(verbose_name=b'Retorn\xc3\xb3 Firmada'),
        ),
        migrations.AlterField(
            model_name='rut',
            name='solicitante',
            field=models.CharField(max_length=4, verbose_name=b'Area Solicitante', choices=[(b'LIA', b'LIA'), (b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'LIM4', b'LIM4'), (b'LIM5', b'LIM5'), (b'LIM6', b'LIM6'), (b'EXT', b'EXT'), (b'SIS', b'SIS'), (b'DES', b'DES'), (b'CAL', b'CAL'), (b'MEC', b'MEC'), (b'ML', b'ML')]),
        ),
    ]
