# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0154_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presupuesto',
            options={'permissions': (('finish_presupuesto', 'Can finish presupuesto'), ('cancel_presupuesto', 'Can cancel presupuesto'), ('read_presupuesto', 'Can read presupuesto'))},
        ),
    ]
