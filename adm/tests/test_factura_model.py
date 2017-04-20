# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Factura, OT
from django.contrib.contenttypes.models import ContentType


class FacutaTest(TestCase):

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

    def test_estado_label(self):
        factura = Factura.objects.get(id=1)
        field_label = factura._meta.get_field("estado").verbose_name
        self.assertEquals(field_label, "Estado")

    def test_numero_label(self):
        factura = Factura.objects.get(id=1)
        field_label = factura._meta.get_field("numero").verbose_name
        self.assertEquals(field_label, "Nro. Factura")

    def test_fecha_label(self):
        factura = Factura.objects.get(id=1)
        field_label = factura._meta.get_field("fecha").verbose_name
        self.assertEquals(field_label, "Fecha")

    def test_importe_label(self):
        factura = Factura.objects.get(id=1)
        field_label = factura._meta.get_field("importe").verbose_name
        self.assertEquals(field_label, "Importe")

    def test_fecha_aviso_label(self):
        factura = Factura.objects.get(id=1)
        field_label = factura._meta.get_field("fecha_aviso").verbose_name
        self.assertEquals(field_label, "Aviso de Trabajo Realizado")
