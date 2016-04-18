# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0015_turno_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='fecha_fin',
            field=models.DateField(null=True, verbose_name=b'Finalizacion estimada', blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_inicio',
            field=models.DateField(null=True, verbose_name=b'Inicio estimado', blank=True),
        ),
    ]
