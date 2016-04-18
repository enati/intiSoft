# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0057_ofertatec_linea_cant_horas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ofertatec_linea',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ofertatec_linea',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='ofertatec_linea',
            name='ofertatec',
        ),
        migrations.RemoveField(
            model_name='ofertatec_linea',
            name='presupuesto',
        ),
        migrations.DeleteModel(
            name='OfertaTec_Linea',
        ),
    ]
