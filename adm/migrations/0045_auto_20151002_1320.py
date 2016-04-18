# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0044_auto_20150929_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec',
            name='detalle',
            field=models.CharField(max_length=150, verbose_name=b'Detalle'),
        ),
    ]
