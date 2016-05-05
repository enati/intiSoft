# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0095_remito'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factura',
            options={'ordering': ['id'], 'permissions': (('cancel_factura', 'Can cancel factura'),)},
        ),
        migrations.AddField(
            model_name='factura',
            name='estado',
            field=models.CharField(default=b'activa', max_length=12, verbose_name=b'Estado', choices=[(b'activa', b'Activa'), (b'cancelada', b'Cancelada')]),
        ),
    ]
