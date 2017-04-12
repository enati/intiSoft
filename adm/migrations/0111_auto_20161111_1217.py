# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0110_rut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rut',
            name='fecha_envio_cc',
            field=models.DateField(null=True, verbose_name=b'Fecha de envio a CC', blank=True),
        ),
        migrations.AlterField(
            model_name='rut',
            name='fecha_envio_ut',
            field=models.DateField(null=True, verbose_name=b'Fecha de envio a la UT', blank=True),
        ),
    ]
