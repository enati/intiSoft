# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0005_presupuesto_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_realizado',
            field=models.DateField(verbose_name=b'Fecha de Presupuesto'),
        ),
    ]
