# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0028_auto_20150928_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='ofertatec',
            name='rubro',
            field=models.ForeignKey(to='adm.Rubro', null=True),
        ),
    ]
