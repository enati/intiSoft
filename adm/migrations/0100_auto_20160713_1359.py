# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0099_ot_linea_precio_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ot',
            options={'permissions': (('cancel_ot', 'Can cancel OT'), ('finish_ot', 'Can finish OT'))},
        ),
    ]
