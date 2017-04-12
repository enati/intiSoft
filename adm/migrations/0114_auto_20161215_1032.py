# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0113_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sot',
            name='ejecutor',
            field=models.ForeignKey(related_name='sot_ejecutor', on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name=b'Usuario', to='adm.Usuario'),
        ),
    ]
