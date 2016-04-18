# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0048_remove_presupuesto_ofertatec'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='nro_recepcion',
            field=models.CharField(max_length=15, unique=True, null=True, verbose_name=b'Nro. Recibo de Recepcion', blank=True),
        ),
    ]
