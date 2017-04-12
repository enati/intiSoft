# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0120_sot_descuento_fijo'),
    ]

    operations = [
        migrations.AddField(
            model_name='rut',
            name='descuento_fijo',
            field=models.BooleanField(default=False, verbose_name=b'Descuento fijo'),
            preserve_default=False,
        ),
    ]
