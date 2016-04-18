# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0027_auto_20160310_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertatec_linea',
            name='detalle',
            field=models.CharField(max_length=150, null=True, verbose_name=b'Detalle', blank=True),
        ),
        migrations.AddField(
            model_name='ofertatec_linea',
            name='tipo_servicio',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Tipo de Servicio', blank=True),
        ),
    ]
