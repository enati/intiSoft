# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import OT


class OTTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        OT.objects.create(id=1,
                          codigo="00001")

    def test_estado_label(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("estado").verbose_name
        self.assertEquals(field_label, "Estado")

    def test_codigo_label(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("codigo").verbose_name
        self.assertEquals(field_label, "Nro. OT")

    def test_factura_set_label(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("factura_set").verbose_name
        self.assertEquals(field_label, "Factura")