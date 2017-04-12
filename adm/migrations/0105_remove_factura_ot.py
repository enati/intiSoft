# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0104_auto_20161026_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='ot',
        ),
    ]
