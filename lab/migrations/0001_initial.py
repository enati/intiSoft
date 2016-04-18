# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('fecha_solicitud', models.DateField(verbose_name=b'Solicitud')),
                ('fecha_presupuesto', models.DateField(verbose_name=b'Envio del presupuesto')),
                ('fecha_aceptacion', models.DateField(verbose_name=b'Aceptacion del presupuesto')),
                ('validez', models.IntegerField(default=0)),
                ('fecha_inicio', models.DateField(verbose_name=b'Inicio estimado')),
                ('fecha_instrumento', models.DateField(verbose_name=b'Llegada de instrumento')),
                ('fecha_fin', models.DateField(verbose_name=b'Finalizacion estimada')),
                ('observaciones', models.CharField(max_length=150)),
                ('oferta_tec', models.ForeignKey(related_name='ot_id', blank=True, to='adm.OfertaTec', null=True)),
                ('presupuesto', models.ForeignKey(to='adm.Presupuesto')),
            ],
        ),
    ]
