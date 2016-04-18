# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields
import audit_log.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adm', '0058_auto_20151209_1044'),
        ('lab', '0020_auto_20151130_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfertaTec_Linea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('created_with_session_key', audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False)),
                ('modified_with_session_key', audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False)),
                ('precio', models.FloatField(verbose_name=b'Precio')),
                ('cant_horas', models.IntegerField(null=True, verbose_name=b'Horas', blank=True)),
                ('precio_hora', models.IntegerField(null=True, verbose_name=b'Precio por hora', blank=True)),
                ('observaciones', models.TextField(max_length=100, blank=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(related_name='created_lab_ofertatec_linea_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by')),
                ('modified_by', audit_log.models.fields.LastUserField(related_name='modified_lab_ofertatec_linea_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by')),
                ('ofertatec', models.ForeignKey(verbose_name=b'OfertaTec', to='adm.OfertaTec')),
                ('turno', models.ForeignKey(verbose_name=b'Turno', to='lab.Turno')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
