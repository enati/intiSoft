# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0137_auto_20170418_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec',
            name='codigo',
            field=models.CharField(max_length=14, verbose_name=b'C\xc3\xb3digo', validators=[django.core.validators.RegexValidator(b'^\\d{14}$')]),
        ),
    ]
