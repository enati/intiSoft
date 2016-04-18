# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0024_auto_20151228_0927'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='turno',
            options={'permissions': (('finish_turno', 'Can finish turno'), ('cancel_turno', 'Can cancel turno'), ('add_turno_LIM1', 'Can add turno LIM1'), ('add_turno_LIM2', 'Can add turno LIM2'), ('add_turno_LIM3', 'Can add turno LIM3'), ('add_turno_LIM6', 'Can add turno LIM6'), ('add_turno_LIA', 'Can add turno LIA'), ('add_turno_EXT', 'Can add turno EXT'), ('add_turno_SIS', 'Can add turno SIS'), ('add_turno_DES', 'Can add turno DES'), ('change_turno_LIM1', 'Can change turno LIM1'), ('change_turno_LIM2', 'Can change turno LIM2'), ('change_turno_LIM3', 'Can change turno LIM3'), ('change_turno_LIM6', 'Can change turno LIM6'), ('change_turno_LIA', 'Can change turno LIA'), ('change_turno_EXT', 'Can change turno EXT'), ('change_turno_SIS', 'Can change turno SIS'), ('change_turno_DES', 'Can change turno DES'), ('delete_turno_LIM1', 'Can delete turno LIM1'), ('delete_turno_LIM2', 'Can delete turno LIM2'), ('delete_turno_LIM3', 'Can delete turno LIM3'), ('delete_turno_LIM6', 'Can delete turno LIM6'), ('delete_turno_LIA', 'Can delete turno LIA'), ('delete_turno_EXT', 'Can delete turno EXT'), ('delete_turno_SIS', 'Can delete turno SIS'), ('delete_turno_DES', 'Can delete turno DES'), ('finish_turno_LIM1', 'Can finish turno LIM1'), ('finish_turno_LIM2', 'Can finish turno LIM2'), ('finish_turno_LIM3', 'Can finish turno LIM3'), ('finish_turno_LIM6', 'Can finish turno LIM6'), ('finish_turno_LIA', 'Can finish turno LIA'), ('finish_turno_EXT', 'Can finish turno EXT'), ('finish_turno_SIS', 'Can finish turno SIS'), ('finish_turno_DES', 'Can finish turno DES'), ('cancel_turno_LIM1', 'Can cancel turno LIM1'), ('cancel_turno_LIM2', 'Can cancel turno LIM2'), ('cancel_turno_LIM3', 'Can cancel turno LIM3'), ('cancel_turno_LIM6', 'Can cancel turno LIM6'), ('cancel_turno_LIA', 'Can cancel turno LIA'), ('cancel_turno_EXT', 'Can cancel turno EXT'), ('cancel_turno_SIS', 'Can cancel turno SIS'), ('cancel_turno_DES', 'Can cancel turno DES'))},
        ),
    ]
