# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0127_auto_20170105_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', blank=True, to='adm.Presupuesto', null=True),
        ),
        migrations.AlterField(
            model_name='otml',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', blank=True, to='adm.Presupuesto', null=True),
        ),
        migrations.AlterField(
            model_name='rut',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', blank=True, to='adm.Presupuesto', null=True),
        ),
        migrations.AlterField(
            model_name='si',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', blank=True, to='adm.Presupuesto', null=True),
        ),
        migrations.AlterField(
            model_name='sot',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', blank=True, to='adm.Presupuesto', null=True),
        ),
    ]
