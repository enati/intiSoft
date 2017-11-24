# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0156_auto_20171124_0920'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otml',
            options={'permissions': (('cancel_otml', 'Can cancel OT-ML'), ('finish_otml', 'Can finish OT-ML'), ('read_otml', 'Can read OT-ML'))},
        ),
    ]
