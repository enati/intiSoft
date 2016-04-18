# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0008_auto_20150911_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='fecha_aceptacion',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='fecha_instrumento',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='fecha_presupuesto',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='fecha_solicitud',
        ),
    ]
