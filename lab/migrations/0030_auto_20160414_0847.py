# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0029_auto_20160315_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec_linea',
            name='detalle',
            field=models.CharField(max_length=350, null=True, verbose_name=b'Detalle', blank=True),
        ),
    ]
