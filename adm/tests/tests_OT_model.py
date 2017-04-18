# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import OT


class OTTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        OT.objects.create(id=1,
                          codigo="00001")

    # CAMPOS DE CONTRATO

    def test_presupuesto_label(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("presupuesto").verbose_name
        self.assertEquals(field_label, "Presupuesto")

    def test_importe_neto_label(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("importe_neto").verbose_name
        self.assertEquals(field_label, "Importe Neto")

    def test_importe_bruto_label(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("importe_bruto").verbose_name
        self.assertEquals(field_label, "Importe Bruto")

    def test_descuento_label(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("descuento").verbose_name
        self.assertEquals(field_label, "Descuento")

    def test_fecha_realizado_label(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("fecha_realizado").verbose_name
        self.assertEquals(field_label, "Fecha")

    def test_ot_linea_set(self):
        ot = OT.objects.get(id=1)
        field_label = ot._meta.get_field("ot_linea_set").verbose_name
        self.assertEquals(field_label, "Líneas de OT")

    # CAMPOS DE OT

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