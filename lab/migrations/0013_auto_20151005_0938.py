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
        ('lab', '0012_auto_20151005_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=datetime.datetime(2015, 10, 5, 12, 38, 26, 334969, tzinfo=utc), verbose_name='created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='turno',
            name='created_by',
            field=audit_log.models.fields.CreatingUserField(related_name='created_lab_turno_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='turno',
            name='created_with_session_key',
            field=audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='turno',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=datetime.datetime(2015, 10, 5, 12, 38, 31, 351189, tzinfo=utc), verbose_name='modified', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='turno',
            name='modified_by',
            field=audit_log.models.fields.LastUserField(related_name='modified_lab_turno_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by'),
        ),
        migrations.AddField(
            model_name='turno',
            name='modified_with_session_key',
            field=audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False),
        ),
    ]
