# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0023_auto_20151210_0802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ofertatec_linea',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='ofertatec_linea',
            name='precio_hora',
        ),
        migrations.AddField(
            model_name='turno',
            name='fecha_fin_real',
            field=models.DateField(null=True, verbose_name=b'Finalizacion', blank=True),
        ),
    ]
