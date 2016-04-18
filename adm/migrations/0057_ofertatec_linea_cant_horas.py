# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0056_presupuesto_nro_revision'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertatec_linea',
            name='cant_horas',
            field=models.IntegerField(null=True, verbose_name=b'Horas', blank=True),
        ),
    ]
