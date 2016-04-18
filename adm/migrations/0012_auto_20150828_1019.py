# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0011_auto_20150828_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='codigo',
            field=models.CharField(max_length=15),
        ),
    ]
