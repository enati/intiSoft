# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0078_ot'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ot',
            options={'permissions': ('cancel_ot', 'Can cancel OT'),},
        ),
        migrations.AddField(
            model_name='ot',
            name='estado',
            field=models.CharField(default=b'sin_facturar', max_length=12, verbose_name=b'Estado', choices=[(b'sin_facturar', b'Sin Facturar'), (b'no_pago', b'No Pago'), (b'pagado', b'Pagado')]),
        ),
    ]
