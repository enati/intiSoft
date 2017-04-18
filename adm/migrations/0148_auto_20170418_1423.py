# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0147_auto_20170418_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumento',
            name='nro_recepcion',
            field=models.CharField(max_length=15, verbose_name=b'Nro. Recibo de Recepci\xc3\xb3n'),
        ),
    ]
