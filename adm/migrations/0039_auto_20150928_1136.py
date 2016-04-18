# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0038_auto_20150928_1059'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OT',
        ),
        migrations.RemoveField(
            model_name='ofertatec',
            name='IEM',
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='area',
            field=models.CharField(max_length=15, verbose_name=b'Area'),
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='codigo',
            field=models.CharField(max_length=14, verbose_name=b'Codigo'),
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='detalle',
            field=models.CharField(max_length=100, verbose_name=b'Detalle'),
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='precio',
            field=models.FloatField(verbose_name=b'Precio'),
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='proveedor',
            field=models.IntegerField(verbose_name=b'Proveedor'),
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='rubro',
            field=models.CharField(max_length=50, verbose_name=b'Rubro'),
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='subrubro',
            field=models.CharField(max_length=50, verbose_name=b'Subrubro'),
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='tipo_servicio',
            field=models.CharField(max_length=20, verbose_name=b'Tipo de Servicio'),
        ),
    ]
