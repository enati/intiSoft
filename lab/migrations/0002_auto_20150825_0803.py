# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='presupuesto',
            field=models.ForeignKey(blank=True, to='adm.Presupuesto', null=True),
        ),
    ]
