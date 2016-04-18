# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0073_remove_presupuesto_nro_revision'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='asistencia',
            field=models.BooleanField(default=False, verbose_name=b'Asistencia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='calibracion',
            field=models.BooleanField(default=False, verbose_name=b'Calibraci\xc3\xb3n'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='in_situ',
            field=models.BooleanField(default=False, verbose_name=b'In Situ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='lia',
            field=models.BooleanField(default=False, verbose_name=b'LIA'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='nro_revision',
            field=models.IntegerField(default=0),
        ),
    ]
