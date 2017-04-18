# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0136_auto_20170417_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cuit',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name=b'Cuit', validators=[django.core.validators.RegexValidator(b'^\\d{11}$')]),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='mail',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Mail', blank=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(unique=True, max_length=150, verbose_name=b'Nombre', error_messages={b'unique': b'Ya existe un usuario con ese nombre.'}),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nro_usuario',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name=b'Nro. Usuario', validators=[django.core.validators.RegexValidator(b'^\\d{5}$')]),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rubro',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Rubro', blank=True),
        ),
    ]
