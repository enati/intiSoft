# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0003_auto_20150825_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_realizado',
            field=models.DateTimeField(verbose_name=b'Fecha de Presupuesto'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='mail',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
