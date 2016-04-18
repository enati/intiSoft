# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0014_turno_ofertatec'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
