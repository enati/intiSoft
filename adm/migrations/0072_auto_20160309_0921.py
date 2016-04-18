# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adm.models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0071_auto_20160309_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='codigo',
            field=models.CharField(default=adm.models.nextCode, unique=True, max_length=15, verbose_name=b'Nro. Presupuesto', error_messages={b'unique': b'Ya existe un presupuesto con ese n\xc3\xbamero.'}),
        ),
    ]
