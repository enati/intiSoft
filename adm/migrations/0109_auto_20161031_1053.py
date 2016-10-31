# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0108_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='otml',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name=b'Usuario', to='adm.Usuario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='otml',
            name='usuarioRep',
            field=models.ForeignKey(related_name='usuarioRep_set', on_delete=django.db.models.deletion.PROTECT, default=1, verbose_name=b'Usuario Representado', to='adm.Usuario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='otml',
            name='vpe',
            field=models.CharField(max_length=5, null=True, verbose_name=b'VPE', blank=True),
        ),
        migrations.AddField(
            model_name='otml',
            name='vpu',
            field=models.DateField(null=True, verbose_name=b'VPU', blank=True),
        ),
        migrations.AddField(
            model_name='otml',
            name='vpuu',
            field=models.DateField(null=True, verbose_name=b'VPUU', blank=True),
        ),
    ]
