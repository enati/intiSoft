# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0007_auto_20150827_0813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presupuesto',
            name='aceptado',
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_aceptado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Aceptacion', blank=True),
        ),
    ]
