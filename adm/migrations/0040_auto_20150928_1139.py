# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0039_auto_20150928_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofertatec',
            name='proveedor',
            field=models.IntegerField(default=b'106', verbose_name=b'Proveedor'),
        ),
    ]
