# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0030_auto_20160414_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertatec_linea',
            name='precio_total',
            field=models.FloatField(default=0, verbose_name=b'Precio Total'),
            preserve_default=False,
        ),
    ]
