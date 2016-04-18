# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0016_auto_20150907_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='estado',
            field=models.CharField(default=b'borrador', max_length=10, blank=True, choices=[(b'borrador', b'Borrador'), (b'aceptado', b'Aceptado'), (b'finalizado', b'Finalizado'), (b'cancelado', b'Cancelado')]),
        ),
    ]
