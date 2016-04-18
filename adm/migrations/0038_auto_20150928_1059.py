# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0037_usuario_rubro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subrubro',
            old_name='rubro',
            new_name='parent',
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='area',
            field=models.CharField(max_length=15, null=True, verbose_name=b'Area', choices=[(b'AGE', b'AGE'), (b'CORDOBA', b'CORDOBA'), (b'EXT', b'EXT'), (b'INF', b'INF'), (b'LIA', b'LIA'), (b'LIM1', b'LIM1'), (b'LIM2', b'LIM2'), (b'LIM3', b'LIM3'), (b'MEC', b'MEC'), (b'PML', b'PML'), (b'RAFAELA', b'RAFAELA')]),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_solicitado',
            field=models.DateField(null=True, verbose_name=b'Fecha de Solicitud'),
        ),
    ]
