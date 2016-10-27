# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0106_auto_20161027_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ot_linea',
            name='ot',
        ),
    ]
