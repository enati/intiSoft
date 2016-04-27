# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0083_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='ot',
            field=models.ForeignKey(default=1, verbose_name=b'OT', to='adm.OT'),
            preserve_default=False,
        ),
    ]
