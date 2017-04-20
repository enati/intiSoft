# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Recibo, Factura, OT
from django.contrib.contenttypes.models import ContentType


class ReciboTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Factura para OT, es lo mismo para OTML
        OT.objects.create(id=1,
                          codigo="00001")
        ot = OT.objects.get(id=1)
        content_type = ContentType.objects.get(model="ot")
        Factura.objects.create(id=1,
                               numero="00001",
                               content_type=content_type,
                               object_id=ot.id)
        factura = Factura.objects.get(id=1)
        Recibo.objects.create(id=1,
                             factura=factura)

    def test_comprobante_cobro_test(self):
        recibo = Recibo.objects.get(id=1)
        field_label = recibo._meta.get_field("comprobante_cobro").verbose_name
        self.assertEquals(field_label, "Comprobante de Cobro")

    def test_numero_test(self):
        recibo = Recibo.objects.get(id=1)
        field_label = recibo._meta.get_field("numero").verbose_name
        self.assertEquals(field_label, "Número")

    def test_fecha_test(self):
        recibo = Recibo.objects.get(id=1)
        field_label = recibo._meta.get_field("fecha").verbose_name
        self.assertEquals(field_label, "Fecha")

    def test_importe_test(self):
        recibo = Recibo.objects.get(id=1)
        field_label = recibo._meta.get_field("importe").verbose_name
        self.assertEquals(field_label, "Importe")

    def test_factura_test(self):
        recibo = Recibo.objects.get(id=1)
        field_label = recibo._meta.get_field("factura").verbose_name
        self.assertEquals(field_label, "Factura")
