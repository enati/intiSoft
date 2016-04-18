# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0052_auto_20151119_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='nro_recepcion',
            field=models.CharField(max_length=15, null=True, verbose_name=b'Nro. Recibo de Recepcion', blank=True),
        ),
    ]
