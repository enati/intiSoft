# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Remito, OT


class RemitoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        OT.objects.create(id=1,
                          codigo="00001")
        ot = OT.objects.get(id=1)
        Remito.objects.create(ot=ot)

    def test_numero_label(self):
        remito = Remito.objects.get(id=1)
        field_label = remito._meta.get_field("numero").verbose_name
        self.assertEquals(field_label, "Número")

    def test_fecha_label(self):
        remito = Remito.objects.get(id=1)
        field_label = remito._meta.get_field("fecha").verbose_name
        self.assertEquals(field_label, "Fecha")

    def test_ot_label(self):
        remito = Remito.objects.get(id=1)
        field_label = remito._meta.get_field("ot").verbose_name
        self.assertEquals(field_label, "OT")
