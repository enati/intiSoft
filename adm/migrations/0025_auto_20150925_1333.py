# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0024_auto_20150925_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='area',
            field=models.CharField(max_length=15, verbose_name=b'Area', choices=[(b'AGE', b'AGE'), (b'CORDOBA', b'CORDOBA'), (b'EXT', b'EXT'), (b'INF', b'INF'), (b'LIA', b'LIA'), (b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'MEC', b'MEC'), (b'PML', b'PML'), (b'RAFAELA', b'RAFAELA')]),
        ),
    ]
