# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0055_ofertatec_linea_presupuesto'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='nro_revision',
            field=models.IntegerField(default=0),
        ),
    ]
