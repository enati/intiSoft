# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Presupuesto, Usuario
from datetime import datetime


class PresupuestoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Usuario.objects.create(nro_usuario='00001',
                               cuit='00000000000')
        usuario = Usuario.objects.get(id=1)
        Presupuesto.objects.create(codigo='00001',
                                   fecha_solicitado=datetime.now().date(),
                                   usuario=usuario)

    def test_codigo_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('codigo').verbose_name
        self.assertEquals(field_label, 'Codigo')