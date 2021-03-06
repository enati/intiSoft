# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0077_auto_20160414_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='estado',
            field=models.CharField(default=b'borrador', max_length=10, verbose_name=b'Estado', choices=[(b'borrador', b'Borrador'), (b'aceptado', b'Aceptado'), (b'en_proceso_de_facturacion', b'En Proceso de Facturacion'), (b'finalizado', b'Finalizado'), (b'cancelado', b'Cancelado')]),
        ),
    ]
