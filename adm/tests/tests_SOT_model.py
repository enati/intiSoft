# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import SOT, Usuario
from datetime import datetime


class SOTTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create(id=1)
        usuario = Usuario.objects.get(id=1)
        SOT.objects.create(id=1,
                           deudor=usuario,
                           ejecutor=usuario,
                           fecha_prevista=datetime.now().date(),
                           firmada=False,
                           descuento_fijo=False
                           )

    def test_estado_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("estado").verbose_name
        self.assertEquals(field_label, "Estado")

    def test_codigo_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("codigo").verbose_name
        self.assertEquals(field_label, "Nro. SOT")

    def test_deudor_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("deudor").verbose_name
        self.assertEquals(field_label, "UT Deudora")

    def test_ejecutor_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("ejecutor").verbose_name
        self.assertEquals(field_label, "UT Ejecutora")

    def test_usuario_final_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("usuario_final").verbose_name
        self.assertEquals(field_label, "Usuario OT")

    def test_ot_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("ot").verbose_name
        self.assertEquals(field_label, "Nro. OT")

    def test_expediente_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("expediente").verbose_name
        self.assertEquals(field_label, "Expediente")

    def test_fecha_envio_ut_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("fecha_envio_ut").verbose_name
        self.assertEquals(field_label, "Fecha de Envío a la UT")

    def test_firmada_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("firmada").verbose_name
        self.assertEquals(field_label, "Retornó Firmada")

    def test_fecha_envio_cc_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("fecha_envio_cc").verbose_name
        self.assertEquals(field_label, "Fecha de Envío a CC")

    def test_fecha_prevista_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("fecha_prevista").verbose_name
        self.assertEquals(field_label, "Fecha Prevista")

    def test_solicitante_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("solicitante").verbose_name
        self.assertEquals(field_label, "Area Solicitante")

    def test_descuento_fijo_label(self):
        sot = SOT.objects.get(id=1)
        field_label = sot._meta.get_field("descuento_fijo").verbose_name
        self.assertEquals(field_label, "Descuento Fijo")

