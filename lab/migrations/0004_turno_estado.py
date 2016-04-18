# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0003_auto_20150825_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='estado',
            field=models.CharField(default=b'en_espera', max_length=10, choices=[(b'en_espera', b'En Espera'), (b'activo', b'Activo'), (b'finalizado', b'Finalizado'), (b'cancelado', b'Cancelado')]),
        ),
    ]
