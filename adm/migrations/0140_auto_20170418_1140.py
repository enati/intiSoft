# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0139_auto_20170418_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumento',
            name='presupuesto',
            field=models.ForeignKey(verbose_name=b'Presupuesto', to='adm.Presupuesto'),
        ),
    ]
