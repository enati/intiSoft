# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0004_auto_20150826_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='usuario',
            field=models.OneToOneField(default=1, to='adm.Usuario'),
            preserve_default=False,
        ),
    ]
