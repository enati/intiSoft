# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0114_auto_20161215_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='rut',
            name='ejecutor',
            field=models.ForeignKey(related_name='rut_ejecutor', on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name=b'Usuario', to='adm.Usuario'),
        ),
        migrations.AlterField(
            model_name='rut',
            name='deudor',
            field=models.ForeignKey(related_name='rut_deudor', on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Usuario', to='adm.Usuario'),
        ),
    ]
