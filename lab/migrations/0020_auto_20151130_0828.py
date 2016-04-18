# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0053_auto_20151125_0941'),
        ('lab', '0019_turno_revisionar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='ofertatec',
        ),
        migrations.AddField(
            model_name='turno',
            name='ofertatec',
            field=models.ManyToManyField(to='adm.OfertaTec', verbose_name=b'Oferta Tec.', blank=True),
        ),
    ]
