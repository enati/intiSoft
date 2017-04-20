# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import OfertaTec


class OfertaTecTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        OfertaTec.objects.create(codigo="00000000000000",
                                 rubro="RUBRO",
                                 subrubro="SUBRUBRO",
                                 tipo_servicio="TIPO DE SERVICIO",
                                 area="AREA",
                                 detalle="Detalle",
                                 precio="0.00")

    def test_proveedor_label(self):
        ofertatec = OfertaTec.objects.get(codigo="00000000000000")
        field_label = ofertatec._meta.get_field("proveedor").verbose_name
        self.assertEquals(field_label, "Proveedor")

    def test_codigo_label(self):
        ofertatec = OfertaTec.objects.get(codigo="00000000000000")
        field_label = ofertatec._meta.get_field("codigo").verbose_name
        self.assertEquals(field_label, "Código")

    def test_rubro_label(self):
        ofertatec = OfertaTec.objects.get(codigo="00000000000000")
        field_label = ofertatec._meta.get_field("rubro").verbose_name
        self.assertEquals(field_label, "Rubro")

    def test_subrubro_label(self):
        ofertatec = OfertaTec.objects.get(codigo="00000000000000")
        field_label = ofertatec._meta.get_field("subrubro").verbose_name
        self.assertEquals(field_label, "Subrubro")

    def test_tipo_servicio_label(self):
        ofertatec = OfertaTec.objects.get(codigo="00000000000000")
        field_label = ofertatec._meta.get_field("tipo_servicio").verbose_name
        self.assertEquals(field_label, "Tipo de Servicio")

    def test_area_label(self):
        ofertatec = OfertaTec.objects.get(codigo="00000000000000")
        field_label = ofertatec._meta.get_field("area").verbose_name
        self.assertEquals(field_label, "Area")

    def test_detalle_label(self):
        ofertatec = OfertaTec.objects.get(codigo="00000000000000")
        field_label = ofertatec._meta.get_field("detalle").verbose_name
        self.assertEquals(field_label, "Detalle")

    def test_precio_label(self):
        ofertatec = OfertaTec.objects.get(codigo="00000000000000")
        field_label = ofertatec._meta.get_field("precio").verbose_name
        self.assertEquals(field_label, "Precio")