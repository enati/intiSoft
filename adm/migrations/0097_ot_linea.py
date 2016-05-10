# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields
import audit_log.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adm', '0096_auto_20160505_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='OT_Linea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('created_with_session_key', audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False)),
                ('modified_with_session_key', audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False)),
                ('precio', models.FloatField(verbose_name=b'Precio')),
                ('cantidad', models.IntegerField(default=1, verbose_name=b'Cantidad')),
                ('cant_horas', models.FloatField(null=True, verbose_name=b'Horas', blank=True)),
                ('observaciones', models.TextField(max_length=100, blank=True)),
                ('detalle', models.CharField(max_length=350, null=True, verbose_name=b'Detalle', blank=True)),
                ('tipo_servicio', models.CharField(max_length=20, null=True, verbose_name=b'Tipo de Servicio', blank=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(related_name='created_adm_ot_linea_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by')),
                ('modified_by', audit_log.models.fields.LastUserField(related_name='modified_adm_ot_linea_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by')),
                ('ofertatec', models.ForeignKey(verbose_name=b'OfertaTec', to='adm.OfertaTec')),
                ('ot', models.ForeignKey(verbose_name=b'OT', to='adm.OT')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
