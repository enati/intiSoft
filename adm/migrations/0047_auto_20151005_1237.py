# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0046_auto_20151005_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ofertatec',
            options={'ordering': ['codigo']},
        ),
    ]
