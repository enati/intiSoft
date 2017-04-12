# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0101_auto_20160922_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remito',
            name='factura',
        ),
        migrations.AddField(
            model_name='remito',
            name='ot',
            field=models.ForeignKey(default=1, verbose_name=b'OT', to='adm.OT'),
            preserve_default=False,
        ),
    ]
