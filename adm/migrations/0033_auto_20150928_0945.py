# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0032_usuario_rubro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subrubro',
            old_name='parent',
            new_name='rubro',
        ),
    ]
