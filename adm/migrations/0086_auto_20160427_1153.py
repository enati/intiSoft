# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0085_auto_20160426_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot',
            name='fecha_realizado',
            field=models.DateField(null=True, verbose_name=b'Fecha'),
        ),
        migrations.AlterField(
            model_name='ot',
            name='importe',
            field=models.FloatField(default=0, null=True, verbose_name=b'Importe'),
        ),
    ]
