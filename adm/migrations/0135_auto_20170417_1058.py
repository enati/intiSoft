# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0134_auto_20170120_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='asistencia',
            field=models.BooleanField(default=False, verbose_name=b'Asistencia'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='calibracion',
            field=models.BooleanField(default=False, verbose_name=b'Calibraci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='in_situ',
            field=models.BooleanField(default=False, verbose_name=b'In Situ'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='lia',
            field=models.BooleanField(default=False, verbose_name=b'LIA'),
        ),
    ]
