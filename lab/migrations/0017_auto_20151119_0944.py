# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0016_auto_20151119_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='ofertatec',
            field=models.ForeignKey(verbose_name=b'Oferta Tec.', blank=True, to='adm.OfertaTec', null=True),
        ),
    ]
