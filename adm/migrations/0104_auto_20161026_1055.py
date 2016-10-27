# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('adm', '0103_auto_20160922_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='content_type',
            field=models.ForeignKey(default=15, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factura',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='factura',
            name='ot',
            field=models.ForeignKey(verbose_name=b'OT', blank=True, to='adm.OT', null=True),
        ),
    ]
