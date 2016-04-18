# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0011_auto_20150928_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='observaciones',
            field=models.TextField(max_length=100, blank=True),
        ),
    ]
