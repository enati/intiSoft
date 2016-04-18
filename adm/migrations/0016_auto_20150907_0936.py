# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0015_presupuesto_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='presupuesto',
            old_name='state',
            new_name='estado',
        ),
    ]
