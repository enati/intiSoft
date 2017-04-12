# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0119_sot_solicitante'),
    ]

    operations = [
        migrations.AddField(
            model_name='sot',
            name='descuento_fijo',
            field=models.BooleanField(default=False, verbose_name=b'Descuento fijo'),
            preserve_default=False,
        ),
    ]
