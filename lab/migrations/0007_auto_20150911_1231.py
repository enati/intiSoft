# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0006_auto_20150911_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='observaciones',
            field=models.TextField(default='asdf', max_length=150, blank=True),
            preserve_default=False,
        ),
    ]
