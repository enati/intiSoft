# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0110_sot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sot',
            name='usuario_final',
            field=models.ForeignKey(related_name='sot_usuario_final', on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Usuario OT', blank=True, to='adm.Usuario', null=True),
        ),
    ]
