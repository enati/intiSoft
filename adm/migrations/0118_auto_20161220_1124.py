# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0117_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='sot',
            name='fecha_envio_cc',
            field=models.DateField(null=True, verbose_name=b'Fecha de envio a CC', blank=True),
        ),
        migrations.AddField(
            model_name='sot',
            name='fecha_envio_ut',
            field=models.DateField(null=True, verbose_name=b'Fecha de envio a la UT', blank=True),
        ),
        migrations.AddField(
            model_name='sot',
            name='firmada',
            field=models.BooleanField(default=False, verbose_name=b'Retorno firmada'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rut',
            name='fecha_prevista',
            field=models.DateField(default=datetime.datetime(2016, 12, 20, 14, 24, 4, 615513, tzinfo=utc), verbose_name=b'Fecha prevista'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sot',
            name='fecha_prevista',
            field=models.DateField(default=datetime.datetime(2016, 12, 20, 14, 24, 53, 139924, tzinfo=utc), verbose_name=b'Fecha prevista'),
            preserve_default=False,
        ),
    ]
