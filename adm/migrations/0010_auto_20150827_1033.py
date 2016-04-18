# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0009_auto_20150827_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='usuario',
            field=models.ForeignKey(to='adm.Usuario'),
        ),
    ]
