# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0028_auto_20160310_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec_linea',
            name='cant_horas',
            field=models.FloatField(null=True, verbose_name=b'Horas', blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='estado',
            field=models.CharField(default=b'en_espera', max_length=10, choices=[(b'en_espera', b'En Espera'), (b'activo', b'Activo'), (b'finalizado', b'Finalizado'), (b'cancelado', b'Cancelado')]),
        ),
    ]
