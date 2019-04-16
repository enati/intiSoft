# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-16 13:07
from __future__ import unicode_literals

import adm.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0180_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='removed',
            field=models.DateTimeField(blank=True, default=None, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='pdt',
            name='anio',
            field=models.CharField(choices=[(b'2017', b'2017'), (b'2018', b'2018'), (b'2019', b'2019'), (b'2020', b'2020'), (b'2021', b'2021')], default=adm.models.yearNow, max_length=4, null=True, verbose_name=b'A\xc3\xb1o'),
        ),
        migrations.AlterUniqueTogether(
            name='contacto',
            unique_together=set([('usuario', 'nombre', 'telefono', 'mail')]),
        ),
        migrations.AlterUniqueTogether(
            name='direccionusuario',
            unique_together=set([('calle', 'numero', 'piso', 'localidad', 'provincia', 'usuario')]),
        ),
    ]
