# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-16 15:07
from __future__ import unicode_literals

from django.db import migrations

def migrate_foreign_key(apps, schema_editor):
    """
        Data migration to populate the GenericForeignKey fields.
    """
    Remito = apps.get_model('adm', 'Remito')
    ContentType = apps.get_model('contenttypes', 'ContentType')
 
    ot_content_type = ContentType.objects.get(app_label='adm', model='ot')
 
    for remito in Remito.objects.all():
        remito.content_type = ot_content_type
        try:
            remito.object_id = remito.ot.id
            remito.save()
        except:
            print "err: OT - ", remito.id
            pass
 

class Migration(migrations.Migration):

    dependencies = [
        ('adm', '0171_auto_20180713_1428'),
    ]

    operations = [
        migrations.RunPython(migrate_foreign_key),
    ]



