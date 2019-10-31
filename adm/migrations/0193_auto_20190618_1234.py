# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-06-18 15:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0192_auto_20190618_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='otml',
            name='area_tematica',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm.AreaTematica', verbose_name=b'Area Tem\xc3\xa1tica'),
        ),
        migrations.AddField(
            model_name='otml',
            name='centro_costos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm.CentroDeCostos', verbose_name=b'Centro de Costos'),
        ),
        migrations.AddField(
            model_name='otml',
            name='horizonte',
            field=models.CharField(choices=[(b'Industria - H1', b'Industria - H1'), (b'Industria - H2', b'Industria - H2'), (b'Industria - H3', b'Industria - H3'), (b'Ecosistema - H1', b'Ecosistema - H1'), (b'Ecosistema - H2', b'Ecosistema - H2'), (b'Ecosistema - H3', b'Ecosistema - H3'), (b'Resto - H1', b'Resto - H1')], max_length=15, null=True),
        ),
    ]