# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0047_auto_20151005_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presupuesto',
            name='ofertatec',
        ),
    ]
