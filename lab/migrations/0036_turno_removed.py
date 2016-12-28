# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0035_ofertatec_linea_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='removed',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
    ]
