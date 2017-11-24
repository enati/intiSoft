# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0155_auto_20171124_0841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ot',
            options={'permissions': (('cancel_ot', 'Can cancel OT'), ('finish_ot', 'Can finish OT'), ('read_ot', 'Can read OT'))},
        ),
    ]
