# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0118_auto_20161220_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='sot',
            name='solicitante',
            field=models.CharField(default='LIA', max_length=4, choices=[(b'LIA', b'LIA'), (b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'LIM6', b'LIM6'), (b'EXT', b'EXT'), (b'SIS', b'SIS'), (b'DES', b'DES'), (b'CAL', b'CAL'), (b'MEC', b'MEC'), (b'ML', b'ML')]),
            preserve_default=False,
        ),
    ]
