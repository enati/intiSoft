# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0080_auto_20160426_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot',
            name='estado',
            field=models.CharField(default=b'sin_facturar', max_length=12, verbose_name=b'Estado', choices=[(b'sin_facturar', b'Sin Facturar'), (b'no_pago', b'No Pago'), (b'pagado', b'Pagado'), (b'cancelada', b'Cancelada')]),
        ),
    ]
