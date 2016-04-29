# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0092_recibo_ot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibo',
            name='ot',
            field=models.ForeignKey(verbose_name=b'OT', blank=True, to='adm.OT', null=True),
        ),
    ]
