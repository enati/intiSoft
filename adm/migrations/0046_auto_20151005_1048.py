# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import audit_log.models.fields
from django.utils.timezone import utc
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adm', '0045_auto_20151002_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ofertatec',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AddField(
            model_name='ofertatec',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 10, 5, 13, 47, 16, 993909, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ofertatec',
            name='created_by',
            field=audit_log.models.fields.CreatingUserField(related_name='created_adm_ofertatec_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='ofertatec',
            name='created_with_session_key',
            field=audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='ofertatec',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 10, 5, 13, 47, 21, 296727, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ofertatec',
            name='modified_by',
            field=audit_log.models.fields.LastUserField(related_name='modified_adm_ofertatec_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by'),
        ),
        migrations.AddField(
            model_name='ofertatec',
            name='modified_with_session_key',
            field=audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 10, 5, 13, 47, 45, 623593, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='created_by',
            field=audit_log.models.fields.CreatingUserField(related_name='created_adm_presupuesto_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='created_with_session_key',
            field=audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 10, 5, 13, 47, 53, 124363, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='modified_by',
            field=audit_log.models.fields.LastUserField(related_name='modified_adm_presupuesto_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by'),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='modified_with_session_key',
            field=audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='usuario',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 10, 5, 13, 48, 2, 15607, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='created_by',
            field=audit_log.models.fields.CreatingUserField(related_name='created_adm_usuario_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='created_with_session_key',
            field=audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='usuario',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 10, 5, 13, 48, 5, 433703, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='modified_by',
            field=audit_log.models.fields.LastUserField(related_name='modified_adm_usuario_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='modified_with_session_key',
            field=audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False),
        ),
    ]
