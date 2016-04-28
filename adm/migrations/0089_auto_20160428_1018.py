# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0088_auto_20160428_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot',
            name='codigo',
            field=models.CharField(default=b'00000', error_messages={b'unique': b'Ya existe una OT con ese n\xc3\xbamero.'}, max_length=15, validators=[django.core.validators.RegexValidator(b'^\\d{5}\\/\\d{2}$|^\\d{5}$', message=b'El c\xc3\xb3digo debe ser de la forma 00000 \xc3\xb3 00000/00')], unique=True, verbose_name=b'Nro. OT'),
        ),
    ]
