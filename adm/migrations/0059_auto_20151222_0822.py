# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0058_auto_20151209_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Usuario', to='adm.Usuario'),
        ),
    ]
