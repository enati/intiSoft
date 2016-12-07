# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0109_auto_20161031_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='ot_linea',
            name='codigo',
            field=models.CharField(default=0, max_length=14, verbose_name=b'Codigo', validators=[django.core.validators.RegexValidator(b'^\\d{14}$')]),
            preserve_default=False,
        ),
    ]
