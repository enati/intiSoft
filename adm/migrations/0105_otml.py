# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import audit_log.models.fields
import django.db.models.deletion
from django.conf import settings
import django.core.validators
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adm', '0104_auto_20161020_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTML',
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
                ('estado', models.CharField(default=b'sin_facturar', max_length=12, verbose_name=b'Estado', choices=[(b'sin_facturar', b'Sin Facturar'), (b'no_pago', b'No Pago'), (b'pagado', b'Pagado'), (b'cancelado', b'Cancelado')])),
                ('codigo', models.CharField(default=b'00000', error_messages={b'unique': b'Ya existe una OT con ese n\xc3\xbamero.'}, max_length=15, validators=[django.core.validators.RegexValidator(b'^\\d{5}\\/\\d{2}$|^\\d{5}$', message=b'El c\xc3\xb3digo debe ser de la forma 00000 \xc3\xb3 00000/00')], unique=True, verbose_name=b'Nro. OT')),
                ('created_by', audit_log.models.fields.CreatingUserField(related_name='created_adm_otml_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by')),
                ('modified_by', audit_log.models.fields.LastUserField(related_name='modified_adm_otml_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by')),
                ('presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Presupuesto', to='adm.Presupuesto')),
            ],
            options={
                'permissions': (('cancel_otml', 'Can cancel OT-ML'), ('finish_otml', 'Can finish OT-ML')),
            },
        ),
    ]
