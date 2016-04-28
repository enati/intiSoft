# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields
import audit_log.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adm', '0090_auto_20160428_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('created_with_session_key', audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False)),
                ('modified_with_session_key', audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False)),
                ('comprobante_cobro', models.CharField(max_length=20, verbose_name=b'Comprobante De Cobro', choices=[(b'recibo', b'Recibo'), (b'nota_credito', b'Nota De Credito')])),
                ('numero', models.CharField(max_length=15, verbose_name=b'Nro.')),
                ('fecha', models.DateField(null=True, verbose_name=b'Fecha')),
                ('importe', models.FloatField(default=0, null=True, verbose_name=b'Importe', blank=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(related_name='created_adm_recibo_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by')),
                ('factura', models.ForeignKey(verbose_name=b'Factura', to='adm.Factura')),
                ('modified_by', audit_log.models.fields.LastUserField(related_name='modified_adm_recibo_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
