# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0151_auto_20170518_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='otml',
            name='checkbox_sot',
            field=models.BooleanField(default=False, verbose_name=b'SOT de otro centro'),
        ),
    ]
