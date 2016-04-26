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
        ('adm', '0077_auto_20160414_0847'),
    ]

    operations = [
        migrations.CreateModel(
            name='OT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('created_with_session_key', audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False)),
                ('modified_with_session_key', audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False)),
                ('codigo', models.CharField(default=adm.models.nextOTCode, unique=True, max_length=15, verbose_name=b'Nro. OT', error_messages={b'unique': b'Ya existe una OT con ese n\xc3\xbamero.'})),
                ('fecha_realizado', models.DateField(null=True, verbose_name=b'Fecha', blank=True)),
                ('importe', models.FloatField(null=True, verbose_name=b'Importe', blank=True)),
                ('fecha_aviso', models.DateField(null=True, verbose_name=b'Aviso de Trabajo Realizado', blank=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(related_name='created_adm_ot_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by')),
                ('modified_by', audit_log.models.fields.LastUserField(related_name='modified_adm_ot_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by')),
                ('presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', to='adm.Presupuesto')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
