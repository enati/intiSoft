# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfertaTec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proveedor', models.IntegerField()),
                ('codigo', models.CharField(max_length=14)),
                ('rubro', models.CharField(max_length=150)),
                ('subrubro', models.CharField(max_length=150)),
                ('tipo_servicio', models.CharField(max_length=150)),
                ('area', models.CharField(max_length=150)),
                ('detalle', models.CharField(max_length=150)),
                ('precio', models.FloatField()),
                ('iem', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='OT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aceptado', models.BooleanField(default=False)),
                ('codigo', models.CharField(max_length=15)),
                ('fecha_realizado', models.DateTimeField(verbose_name=b'Realizado')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
    ]
