# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0007_auto_20150911_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='fecha_fin',
            field=models.DateField(default=datetime.datetime(2015, 9, 11, 15, 39, 44, 434688, tzinfo=utc), verbose_name=b'Finalizacion estimada'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_inicio',
            field=models.DateField(default=datetime.datetime(2015, 9, 11, 15, 39, 52, 497381, tzinfo=utc), verbose_name=b'Inicio estimado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='turno',
            name='oferta_tec',
            field=models.ForeignKey(default=1, to='adm.OfertaTec'),
            preserve_default=False,
        ),
    ]
