# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0115_auto_20161215_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='rut',
            name='fecha_prevista',
            field=models.DateField(null=True, verbose_name=b'Fecha prevista', blank=True),
        ),
    ]
