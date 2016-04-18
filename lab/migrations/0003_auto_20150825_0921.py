# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0002_auto_20150825_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='cantidad',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_aceptacion',
            field=models.DateField(null=True, verbose_name=b'Aceptacion del presupuesto', blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_instrumento',
            field=models.DateField(null=True, verbose_name=b'Llegada de instrumento', blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_presupuesto',
            field=models.DateField(null=True, verbose_name=b'Envio del presupuesto', blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_solicitud',
            field=models.DateField(null=True, verbose_name=b'Solicitud', blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='observaciones',
            field=models.TextField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='oferta_tec',
            field=models.ForeignKey(default=4, to='adm.OfertaTec'),
            preserve_default=False,
        ),
    ]
