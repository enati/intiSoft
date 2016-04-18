# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0068_auto_20160309_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(unique=True, max_length=150, error_messages={b'unique': b'Ya existe un usuario con ese nombre.'}),
        ),
    ]
