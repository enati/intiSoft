# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0018_auto_20150907_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='codigo',
            field=models.CharField(unique=True, max_length=15, verbose_name=b'Nro. Presupuesto'),
        ),
    ]
