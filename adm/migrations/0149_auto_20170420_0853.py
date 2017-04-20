# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0148_auto_20170418_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rut',
            name='fecha_envio_cc',
            field=models.DateField(null=True, verbose_name=b'Fecha de Env\xc3\xado a CC', blank=True),
        ),
        migrations.AlterField(
            model_name='sot',
            name='descuento_fijo',
            field=models.BooleanField(verbose_name=b'Descuento Fijo'),
        ),
    ]
