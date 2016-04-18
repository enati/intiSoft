# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0050_remove_presupuesto_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='usuario',
            field=models.ForeignKey(verbose_name=b'Usuario', to='adm.Usuario', null=True),
        ),
    ]
