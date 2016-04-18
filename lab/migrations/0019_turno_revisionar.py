# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0018_turno_nro_revision'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='revisionar',
            field=models.BooleanField(default=False),
        ),
    ]
