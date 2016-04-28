# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0091_recibo'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='ot',
            field=models.ForeignKey(default=1, verbose_name=b'OT', to='adm.OT'),
            preserve_default=False,
        ),
    ]
