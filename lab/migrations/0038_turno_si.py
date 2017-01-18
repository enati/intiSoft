# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0132_auto_20170113_1143'),
        ('lab', '0037_auto_20170112_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='si',
            field=models.ForeignKey(blank=True, to='adm.SI', null=True),
        ),
    ]
