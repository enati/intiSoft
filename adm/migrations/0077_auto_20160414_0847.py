# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0076_auto_20160317_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec',
            name='detalle',
            field=models.CharField(max_length=350, verbose_name=b'Detalle'),
        ),
    ]
