# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0151_auto_20170502_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='si',
            name='estado',
            field=models.CharField(default=b'borrador', max_length=12, verbose_name=b'Estado', choices=[(b'borrador', b'Borrador'), (b'pendiente', b'Pendiente'), (b'finalizada', b'Finalizada'), (b'cancelada', b'Cancelada')]),
        ),
    ]
