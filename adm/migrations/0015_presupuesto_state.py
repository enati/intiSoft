# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0014_auto_20150904_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='state',
            field=models.CharField(default=b'borrador', max_length=10, choices=[(b'borrador', b'Borrador'), (b'aceptado', b'Aceptado'), (b'finalizado', b'Finalizado'), (b'cancelado', b'Cancelado')]),
        ),
    ]
