# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0152_auto_20170502_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='si',
            name='fecha_prevista',
        ),
    ]
