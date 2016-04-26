# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0079_auto_20160426_0906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ot',
            options={'permissions': (('cancel_ot', 'Can cancel OT'),)},
        ),
    ]
