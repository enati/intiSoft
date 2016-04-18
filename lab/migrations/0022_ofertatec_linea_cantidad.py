# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0021_ofertatec_linea'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertatec_linea',
            name='cantidad',
            field=models.IntegerField(default=1, verbose_name=b'Cantidad'),
        ),
    ]
