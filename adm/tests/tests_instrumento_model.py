# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Instrumento, Usuario, Presupuesto
from datetime import datetime


class InstrumentoTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create(id=1)
        usuario = Usuario.objects.get(id=1)
        Presupuesto.objects.create(id=1,
                                   codigo="00001",
                                   fecha_solicitado=datetime.now().date(),
                                   usuario=usuario)
        presupuesto = Presupuesto.objects.get(id=1)
        Instrumento.objects.create(id=1,
                                   fecha_llegada=datetime.now().date(),
                                   presupuesto=presupuesto)

    def test_detalle_label(self):
        instrumento = Instrumento.objects.get(id=1)
        field_label = instrumento._meta.get_field("detalle").verbose_name
        self.assertEquals(field_label, "Detalle")

    def test_fecha_llegada_label(self):
        instrumento = Instrumento.objects.get(id=1)
        field_label = instrumento._meta.get_field("fecha_llegada").verbose_name
        self.assertEquals(field_label, "Fecha de Llegada")

    def test_nro_recepcion_label(self):
        instrumento = Instrumento.objects.get(id=1)
        field_label = instrumento._meta.get_field("nro_recepcion").verbose_name
        self.assertEquals(field_label, "Nro. Recibo de Recepción")

    def test_presupuesto_label(self):
        instrumento = Instrumento.objects.get(id=1)
        field_label = instrumento._meta.get_field("presupuesto").verbose_name
        self.assertEquals(field_label, "Presupuesto")
