# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0150_auto_20170420_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot',
            name='fecha_realizado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Realizaci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='otml',
            name='fecha_realizado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Realizaci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='rut',
            name='fecha_realizado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Realizaci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='si',
            name='fecha_realizado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Realizaci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='sot',
            name='fecha_realizado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Realizaci\xc3\xb3n'),
        ),
    ]
