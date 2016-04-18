# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adm.models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0042_auto_20150929_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='codigo',
            field=models.CharField(default=adm.models.nextCode, unique=True, max_length=15, verbose_name=b'Nro. Presupuesto'),
        ),
    ]
