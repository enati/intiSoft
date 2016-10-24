# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0105_otml'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', to='adm.Presupuesto', null=True),
        ),
        migrations.AlterField(
            model_name='otml',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', to='adm.Presupuesto', null=True),
        ),
    ]
