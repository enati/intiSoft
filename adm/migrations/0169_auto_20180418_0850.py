# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-18 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0168_recibo_observaciones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presupuesto',
            name='asistencia',
        ),
        migrations.RemoveField(
            model_name='presupuesto',
            name='calibracion',
        ),
        migrations.RemoveField(
            model_name='presupuesto',
            name='in_situ',
        ),
        migrations.RemoveField(
            model_name='presupuesto',
            name='lia',
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='tipo',
            field=models.CharField(choices=[(b'calibracion', b'Calibraci\xc3\xb3n'), (b'asistencia', b'Asistencia'), (b'in_situ', b'In Situ'), (b'lia', b'LIA'), (b'mat_ref', b'Materiales de Referencia')], default=b'calibracion', max_length=11, verbose_name=b'Tipo'),
        ),
    ]