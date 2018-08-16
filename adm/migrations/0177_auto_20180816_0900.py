# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-16 12:00
from __future__ import unicode_literals

import audit_log.models.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adm', '0176_presupuesto_contacto'),
    ]

    operations = [
        migrations.CreateModel(
            name='DireccionUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('created_with_session_key', audit_log.models.fields.CreatingSessionKeyField(editable=False, max_length=40, null=True)),
                ('modified_with_session_key', audit_log.models.fields.LastSessionKeyField(editable=False, max_length=40, null=True)),
                ('calle', models.CharField(max_length=50, verbose_name=b'Direcci\xc3\xb3n')),
                ('numero', models.CharField(max_length=10, verbose_name=b'N\xc3\xbamero')),
                ('piso', models.CharField(blank=True, max_length=10, verbose_name=b'Piso/Dpto')),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_adm_direccionusuario_set', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AlterModelOptions(
            name='localidad',
            options={'ordering': ['nombre']},
        ),
        migrations.AlterModelOptions(
            name='provincia',
            options={'ordering': ['nombre']},
        ),
        migrations.AddField(
            model_name='direccionusuario',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm.Localidad', verbose_name=b'Localidad'),
        ),
        migrations.AddField(
            model_name='direccionusuario',
            name='modified_by',
            field=audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_adm_direccionusuario_set', to=settings.AUTH_USER_MODEL, verbose_name='modified by'),
        ),
        migrations.AddField(
            model_name='direccionusuario',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm.Provincia', verbose_name=b'Provincia'),
        ),
        migrations.AddField(
            model_name='direccionusuario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm.Usuario'),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='direccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='adm.DireccionUsuario', verbose_name=b'Direccion'),
        ),
    ]
