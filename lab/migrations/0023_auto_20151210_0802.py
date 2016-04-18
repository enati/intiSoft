# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0022_ofertatec_linea_cantidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='observaciones',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='ofertatec',
        ),
    ]
