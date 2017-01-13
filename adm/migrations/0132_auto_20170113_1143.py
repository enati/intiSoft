# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0131_auto_20170113_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presupuesto',
            name='fecha_instrumento',
        ),
        migrations.RemoveField(
            model_name='presupuesto',
            name='nro_recepcion',
        ),
    ]
