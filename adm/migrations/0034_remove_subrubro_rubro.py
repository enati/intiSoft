# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0033_auto_20150928_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subrubro',
            name='rubro',
        ),
    ]
