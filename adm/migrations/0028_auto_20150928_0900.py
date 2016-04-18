# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0027_auto_20150925_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subrubro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('rubro', models.ForeignKey(verbose_name=b'Rubro', to='adm.Rubro', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='ofertatec',
            name='rubro',
        ),
        migrations.AlterField(
            model_name='ofertatec',
            name='tipo_servicio',
            field=models.CharField(max_length=20, verbose_name=b'Tipo de Servicio', choices=[(b'ASIST. TECNICA', b'ASIST. TECNICA'), (b'DESARROLLO', b'DESARROLLO'), (b'CAPACITACION', b'CAPACITACION'), (b'LOGISTICA', b'LOGISTICA'), (b'ENSAYOS', b'ENSAYOS'), (b'AUDITORIA', b'AUDITORIA'), (b'CALIBRACION', b'CALIBRACION'), (b'CERT. OBLIGATORIA', b'CERT. OBLIGATORIA')]),
        ),
    ]
