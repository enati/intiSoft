# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0157_auto_20171124_0921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rut',
            options={'permissions': (('cancel_rut', 'Can cancel RUT'), ('finish_rut', 'Can finish RUT'), ('read_rut', 'Can read RUT'))},
        ),
        migrations.AlterModelOptions(
            name='si',
            options={'permissions': (('cancel_si', 'Can cancel SOT'), ('finish_si', 'Can finish SOT'), ('read_si', 'Can read SI'))},
        ),
        migrations.AlterModelOptions(
            name='sot',
            options={'permissions': (('cancel_sot', 'Can cancel SOT'), ('finish_sot', 'Can finish SOT'), ('read_sot', 'Can read SOT'))},
        ),
    ]
