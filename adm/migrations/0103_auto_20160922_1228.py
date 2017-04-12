# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0102_auto_20160922_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ot',
            name='fecha_aviso',
        ),
        migrations.AddField(
            model_name='factura',
            name='fecha_aviso',
            field=models.DateField(null=True, verbose_name=b'Aviso de Trabajo Realizado', blank=True),
        ),
    ]
