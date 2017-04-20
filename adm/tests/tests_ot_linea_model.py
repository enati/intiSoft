# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import OT_Linea, OT, OfertaTec
from django.contrib.contenttypes.models import ContentType


class OT_LineaTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Linea para OT, es lo mismo para OTML, SOT, RUT y SI
        OT.objects.create(id=1,
                          codigo="00001")
        ot = OT.objects.get(id=1)
        content_type = ContentType.objects.get(model="ot")
        OfertaTec.objects.create(id=1,
                                 codigo="00000000000000",
                                 rubro="RUBRO",
                                 subrubro="SUBRUBRO",
                                 tipo_servicio="TIPO DE SERVICIO",
                                 area="AREA",
                                 detalle="Detalle",
                                 precio="0.00")
        ofertatec = OfertaTec.objects.get(id=1)
        OT_Linea.objects.create(id=1,
                                ofertatec=ofertatec,
                                codigo="00001",
                                precio="0",
                                precio_total="0",
                                content_type=content_type,
                                object_id=ot.id)

    def test_ofertatec_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("ofertatec").verbose_name
        self.assertEquals(field_label, "Oferta Tecnológica")

    def test_codigo_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("codigo").verbose_name
        self.assertEquals(field_label, "Código")

    def test_precio_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("precio").verbose_name
        self.assertEquals(field_label, "Precio Unitario")

    def test_precio_total_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("precio_total").verbose_name
        self.assertEquals(field_label, "Precio Total")

    def test_cantidad_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("cantidad").verbose_name
        self.assertEquals(field_label, "Cantidad")

    def test_cant_horas_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("cant_horas").verbose_name
        self.assertEquals(field_label, "Horas")

    def test_observaciones_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("observaciones").verbose_name
        self.assertEquals(field_label, "Observaciones")

    def test_detalle_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("detalle").verbose_name
        self.assertEquals(field_label, "Detalle")

    def test_tipo_servicio_label(self):
        ot_linea = OT_Linea.objects.get(id=1)
        field_label = ot_linea._meta.get_field("tipo_servicio").verbose_name
        self.assertEquals(field_label, "Tipo de Servicio")
