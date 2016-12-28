# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0125_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='rut',
            name='removed',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='si',
            name='removed',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='sot',
            name='removed',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
    ]
