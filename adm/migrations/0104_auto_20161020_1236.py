# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0103_auto_20160922_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ot',
            name='importe',
        ),
        migrations.AddField(
            model_name='ot',
            name='descuento',
            field=models.FloatField(default=0, null=True, verbose_name=b'Descuento'),
        ),
        migrations.AddField(
            model_name='ot',
            name='importe_bruto',
            field=models.FloatField(default=0, null=True, verbose_name=b'Importe Bruto'),
        ),
        migrations.AddField(
            model_name='ot',
            name='importe_neto',
            field=models.FloatField(default=0, null=True, verbose_name=b'Importe Neto'),
        ),
    ]
