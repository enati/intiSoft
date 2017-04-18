# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0146_auto_20170418_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibo',
            name='comprobante_cobro',
            field=models.CharField(max_length=20, verbose_name=b'Comprobante de Cobro', choices=[(b'recibo', b'Recibo'), (b'nota_credito', b'Nota De Credito')]),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='numero',
            field=models.CharField(max_length=15, verbose_name=b'N\xc3\xbamero'),
        ),
        migrations.AlterField(
            model_name='remito',
            name='numero',
            field=models.CharField(max_length=15, verbose_name=b'N\xc3\xbamero'),
        ),
    ]
