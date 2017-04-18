# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0145_auto_20170418_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ot_linea',
            name='ofertatec',
            field=models.ForeignKey(verbose_name=b'Oferta Tecnol\xc3\xb3gica', to='adm.OfertaTec'),
        ),
    ]
