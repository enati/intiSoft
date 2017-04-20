# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import RUT, Usuario
from datetime import datetime


class RUTTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create(id=1)
        usuario = Usuario.objects.get(id=1)
        RUT.objects.create(id=1,
                           deudor=usuario,
                           ejecutor=usuario,
                           fecha_prevista=datetime.now().date(),
                           firmada=False,
                           descuento_fijo=False)

    def test_estado_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("estado").verbose_name
        self.assertEquals(field_label, "Estado")

    def test_codigo_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("codigo").verbose_name
        self.assertEquals(field_label, "Nro. RUT")

    def test_deudor_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("deudor").verbose_name
        self.assertEquals(field_label, "UT Deudora")

    def test_ejecutor_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("ejecutor").verbose_name
        self.assertEquals(field_label, "UT Ejecutora")

    def test_solicitante_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("solicitante").verbose_name
        self.assertEquals(field_label, "Area Solicitante")

    def test_fecha_envio_ut_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("fecha_envio_ut").verbose_name
        self.assertEquals(field_label, "Fecha de Envío a la UT")

    def test_firmada_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("firmada").verbose_name
        self.assertEquals(field_label, "Retornó Firmada")

    def test_fecha_envio_cc_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("fecha_envio_cc").verbose_name
        self.assertEquals(field_label, "Fecha de Envío a CC")

    def test_fecha_prevista_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("fecha_prevista").verbose_name
        self.assertEquals(field_label, "Fecha Prevista")

    def test_descuento_fijo_label(self):
        rut = RUT.objects.get(id=1)
        field_label = rut._meta.get_field("descuento_fijo").verbose_name
        self.assertEquals(field_label, "Descuento Fijo")

