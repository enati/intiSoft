# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import SI


class SITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        SI.objects.create(id=1)

    def test_estado_label(self):
        si = SI.objects.get(id=1)
        field_label = si._meta.get_field("estado").verbose_name
        self.assertEquals(field_label, "Estado")

    def test_codigo_label(self):
        si = SI.objects.get(id=1)
        field_label = si._meta.get_field("codigo").verbose_name
        self.assertEquals(field_label, "Nro. SI")

    def test_solicitante_label(self):
        si = SI.objects.get(id=1)
        field_label = si._meta.get_field("solicitante").verbose_name
        self.assertEquals(field_label, "UT Solicitante")

    def test_ejecutor_label(self):
        si = SI.objects.get(id=1)
        field_label = si._meta.get_field("ejecutor").verbose_name
        self.assertEquals(field_label, "UT Ejecutora")

    def test_fecha_fin_real_label(self):
        si = SI.objects.get(id=1)
        field_label = si._meta.get_field("fecha_fin_real").verbose_name
        self.assertEquals(field_label, "Fecha de Finalización")

