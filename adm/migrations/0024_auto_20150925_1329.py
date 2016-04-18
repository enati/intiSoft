# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0023_auto_20150924_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='area',
            field=models.CharField(max_length=15, verbose_name=b'Area', choices=[(b'AGE', b'AGE'), (b'CORDOBA', b'CORDOBA'), (b'EXTENSION', b'EXTENSION'), (b'INFORMATICA', b'INFORMATICA'), (b'LIA', b'LIA'), (b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'MECANICA', b'MECANICA'), (b'PML', b'PML'), (b'RAFAELA', b'RAFAELA')]),
        ),
    ]
