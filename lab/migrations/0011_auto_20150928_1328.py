# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0010_auto_20150924_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='oferta_tec',
        ),
    ]
