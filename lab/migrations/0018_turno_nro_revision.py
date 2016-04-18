# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0017_auto_20151119_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='nro_revision',
            field=models.IntegerField(default=0),
        ),
    ]
