# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0043_auto_20150929_1118'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IEM',
        ),
        migrations.RemoveField(
            model_name='subrubro',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Rubro',
        ),
        migrations.DeleteModel(
            name='Subrubro',
        ),
    ]
