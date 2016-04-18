# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0005_auto_20150909_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='validez',
        ),
        migrations.AlterField(
            model_name='turno',
            name='cantidad',
            field=models.IntegerField(default=1, blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_fin',
            field=models.DateField(null=True, verbose_name=b'Finalizacion estimada', blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_inicio',
            field=models.DateField(null=True, verbose_name=b'Inicio estimado', blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='observaciones',
            field=models.TextField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='oferta_tec',
            field=models.ForeignKey(blank=True, to='adm.OfertaTec', null=True),
        ),
    ]
