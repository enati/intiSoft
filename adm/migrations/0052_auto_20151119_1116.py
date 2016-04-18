# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0051_presupuesto_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='usuario',
            field=models.ForeignKey(verbose_name=b'Usuario', to='adm.Usuario'),
        ),
    ]
