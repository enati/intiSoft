# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0054_ofertatec_linea'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertatec_linea',
            name='presupuesto',
            field=models.ForeignKey(default=1, verbose_name=b'Presupuesto', to='adm.Presupuesto'),
            preserve_default=False,
        ),
    ]
