# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0008_auto_20150827_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec',
            name='IEM',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
