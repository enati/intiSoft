# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0110_ot_linea_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertatec',
            name='removed',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
    ]
