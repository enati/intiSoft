# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0020_auto_20150911_1303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presupuesto',
            options={'permissions': (('finish_presupuesto', 'Can finish presupuesto'), ('cancel_presupuesto', 'Can cancel presupuesto'))},
        ),
    ]
