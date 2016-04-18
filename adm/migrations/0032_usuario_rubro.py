# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0031_remove_usuario_rubro'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='rubro',
            field=models.ForeignKey(verbose_name=b'Rubro', to='adm.Rubro', null=True),
        ),
    ]
