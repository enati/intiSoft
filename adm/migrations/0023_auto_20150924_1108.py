# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0022_auto_20150924_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iem',
            name='nombre',
            field=models.CharField(max_length=30),
        ),
    ]
