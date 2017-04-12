# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adm.models
import audit_log.models.fields
import django.db.models.deletion
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adm', '0109_auto_20161031_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='SOT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('created_with_session_key', audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False)),
                ('modified_with_session_key', audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False)),
                ('importe_neto', models.FloatField(default=0, null=True, verbose_name=b'Importe Neto')),
                ('importe_bruto', models.FloatField(default=0, null=True, verbose_name=b'Importe Bruto')),
                ('descuento', models.FloatField(default=0, null=True, verbose_name=b'Descuento')),
                ('fecha_realizado', models.DateField(null=True, verbose_name=b'Fecha')),
                ('estado', models.CharField(default=b'borrador', max_length=12, verbose_name=b'Estado', choices=[(b'borrador', b'Borrador'), (b'pendiente', b'Pendiente'), (b'cobrada', b'Cobrada'), (b'cancelada', b'Cancelada')])),
                ('codigo', models.CharField(default=adm.models.nextSOTCode, unique=True, max_length=15, verbose_name=b'Nro. SOT', error_messages={b'unique': b'Ya existe una SOT con ese n\xc3\xbamero.'})),
                ('ot', models.CharField(max_length=5, null=True, verbose_name=b'Nro. OT', blank=True)),
                ('expediente', models.CharField(max_length=5, null=True, verbose_name=b'Expediente', blank=True)),
                ('fecha_prevista', models.DateField(null=True, verbose_name=b'Fecha prevista', blank=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(related_name='created_adm_sot_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by')),
                ('deudor', models.ForeignKey(related_name='sot_deudor', on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Usuario', to='adm.Usuario')),
                ('ejecutor', models.ForeignKey(related_name='sot_ejecutor', on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Usuario', to='adm.Usuario')),
                ('modified_by', audit_log.models.fields.LastUserField(related_name='modified_adm_sot_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by')),
                ('presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', to='adm.Presupuesto', null=True)),
                ('usuario_final', models.ForeignKey(related_name='sot_usuario_final', on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Usuario OT', to='adm.Usuario')),
            ],
            options={
                'permissions': (('cancel_sot', 'Can cancel SOT'), ('finish_sot', 'Can finish SOT')),
            },
        ),
    ]
