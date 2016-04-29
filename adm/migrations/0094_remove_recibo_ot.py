# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0093_auto_20160429_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibo',
            name='ot',
        ),
    ]
