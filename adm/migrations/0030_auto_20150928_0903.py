# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0029_ofertatec_rubro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subrubro',
            name='rubro',
        ),
        migrations.AddField(
            model_name='subrubro',
            name='parent',
            field=models.ForeignKey(verbose_name=b'Parent', to='adm.Rubro', null=True),
        ),
    ]
