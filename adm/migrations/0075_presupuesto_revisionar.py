# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0074_auto_20160310_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='revisionar',
            field=models.BooleanField(default=False),
        ),
    ]
