# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0019_auto_20150907_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='fecha_instrumento',
            field=models.DateField(null=True, verbose_name=b'Llegada de instrumento', blank=True),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='fecha_solicitado',
            field=models.DateField(default=datetime.datetime(2015, 9, 11, 16, 3, 56, 432665, tzinfo=utc), verbose_name=b'Fecha de Solicitud'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_realizado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Presupuesto', blank=True),
        ),
    ]
