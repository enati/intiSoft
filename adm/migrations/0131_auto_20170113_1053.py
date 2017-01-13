# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0130_auto_20170112_1438'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instrumento',
            options={'ordering': ['fecha_llegada']},
        ),
    ]
