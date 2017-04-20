# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0149_auto_20170420_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='si',
            name='fecha_fin_real',
            field=models.DateField(null=True, verbose_name=b'Fecha de Finalizaci\xc3\xb3n', blank=True),
        ),
    ]
