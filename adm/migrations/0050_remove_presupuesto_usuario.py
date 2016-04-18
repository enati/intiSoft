# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0049_presupuesto_nro_recepcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presupuesto',
            name='usuario',
        ),
    ]
