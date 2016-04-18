# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0009_auto_20150918_1210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='turno',
            options={'permissions': (('finish_turno', 'Can finish turno'), ('cancel_turno', 'Can cancel turno'))},
        ),
    ]
