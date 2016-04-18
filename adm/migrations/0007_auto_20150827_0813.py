# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0006_auto_20150826_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='IEM',
            field=models.CharField(default='Asistencia tecnica', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='area',
            field=models.CharField(default='LIM1', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='fecha_aceptado',
            field=models.DateField(default=datetime.datetime(2015, 8, 27, 11, 13, 25, 670427, tzinfo=utc), verbose_name=b'Fecha de Aceptacion'),
            preserve_default=False,
        ),
    ]
