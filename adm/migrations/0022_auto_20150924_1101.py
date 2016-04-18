# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0021_auto_20150924_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='IEM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='presupuesto',
            name='IEM',
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='IEM',
            field=models.ManyToManyField(to='adm.IEM', verbose_name=b'IEM'),
        ),
    ]
