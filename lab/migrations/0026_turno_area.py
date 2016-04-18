# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0025_auto_20151230_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='area',
            field=models.CharField(default='LIM1', max_length=10, choices=[(b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'LIM6', b'LIM6'), (b'EXT', b'EXT'), (b'SIS', b'SIS'), (b'DES', b'DES')]),
            preserve_default=False,
        ),
    ]
