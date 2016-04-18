# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0034_remove_subrubro_rubro'),
    ]

    operations = [
        migrations.AddField(
            model_name='subrubro',
            name='rubro',
            field=models.ForeignKey(verbose_name=b'Parent', to='adm.Rubro', null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rubro',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
