# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0012_auto_20150828_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='IEM',
            field=models.CharField(max_length=150, verbose_name=b'IEM'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='area',
            field=models.CharField(max_length=150, verbose_name=b'Area'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='codigo',
            field=models.CharField(max_length=15, verbose_name=b'Codigo'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='usuario',
            field=models.ForeignKey(verbose_name=b'Usuario', to='adm.Usuario'),
        ),
    ]
