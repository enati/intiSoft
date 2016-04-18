# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0030_auto_20150928_0903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='rubro',
        ),
    ]
