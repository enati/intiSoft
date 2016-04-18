# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0040_auto_20150928_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presupuesto',
            name='IEM',
        ),
        migrations.RemoveField(
            model_name='presupuesto',
            name='area',
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='ofertatec',
            field=models.ForeignKey(verbose_name=b'Oferta Tec.', to='adm.OfertaTec', null=True),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='estado',
            field=models.CharField(default=b'borrador', max_length=10, verbose_name=b'Estado', choices=[(b'borrador', b'Borrador'), (b'aceptado', b'Aceptado'), (b'finalizado', b'Finalizado'), (b'cancelado', b'Cancelado')]),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='fecha_solicitado',
            field=models.DateField(verbose_name=b'Fecha de Solicitud'),
        ),
    ]
