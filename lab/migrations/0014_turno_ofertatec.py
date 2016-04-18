# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0047_auto_20151005_1237'),
        ('lab', '0013_auto_20151005_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='ofertatec',
            field=models.ForeignKey(verbose_name=b'Oferta Tec.', to='adm.OfertaTec', null=True),
        ),
    ]
