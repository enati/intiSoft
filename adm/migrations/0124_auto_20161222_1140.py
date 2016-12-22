# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0123_auto_20161222_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea_linea',
            name='arancel',
            field=models.FloatField(null=True, verbose_name=b'Arancel', blank=True),
        ),
    ]
