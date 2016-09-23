# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0100_auto_20160713_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remito',
            name='factura',
            field=models.ForeignKey(verbose_name=b'Factura', to='adm.Factura', null=True),
        ),
    ]
