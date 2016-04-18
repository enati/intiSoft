# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0010_auto_20150827_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='codigo',
            field=models.CharField(max_length=15, verbose_name=b'Codigo'),
        ),
    ]
