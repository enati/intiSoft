# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Tarea_Linea, SI
from django.contrib.contenttypes.models import ContentType


class Tarea_LineaTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Linea para SI
        SI.objects.create(id=1)
        si = SI.objects.get(id=1)
        content_type = ContentType.objects.get(model="si")
        Tarea_Linea.objects.create(id=1,
                                   tarea="Tarea de SI",
                                   horas=1,
                                   content_type=content_type,
                                   object_id=si.id)

    def test_tarea_label(self):
        tarea_linea = Tarea_Linea.objects.get(id=1)
        field_label = tarea_linea._meta.get_field("tarea").verbose_name
        self.assertEquals(field_label, "Tarea")

    def test_horas_label(self):
        tarea_linea = Tarea_Linea.objects.get(id=1)
        field_label = tarea_linea._meta.get_field("horas").verbose_name
        self.assertEquals(field_label, "Horas")

    def test_arancel_label(self):
        tarea_linea = Tarea_Linea.objects.get(id=1)
        field_label = tarea_linea._meta.get_field("arancel").verbose_name
        self.assertEquals(field_label, "Arancel")
