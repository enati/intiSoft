# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adm.models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0111_auto_20161111_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rut',
            name='codigo',
            field=models.CharField(default=adm.models.nextRUTCode, unique=True, max_length=15, verbose_name=b'Nro. RUT', error_messages={b'unique': b'Ya existe una RUT con ese n\xc3\xbamero.'}),
        ),
    ]
