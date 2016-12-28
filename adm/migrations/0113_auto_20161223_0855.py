# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0112_presupuesto_removed'),
    ]

    operations = [
        migrations.AddField(
            model_name='ot',
            name='removed',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='otml',
            name='removed',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
    ]
