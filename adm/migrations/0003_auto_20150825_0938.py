# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0002_auto_20150824_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cuit',
            field=models.CharField(default=0, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='mail',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(default='prueba', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='nro_usuario',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='rubro',
            field=models.CharField(default='rubro', max_length=150),
            preserve_default=False,
        ),
    ]
