# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Presupuesto, Usuario
from datetime import datetime


class PresupuestoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Usuario.objects.create(nombre="John Doe")
        usuario = Usuario.objects.get(nombre="John Doe")
        Presupuesto.objects.create(codigo='00001',
                                   fecha_solicitado=datetime.now().date(),
                                   usuario=usuario)

    def test_estado_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('estado').verbose_name
        self.assertEquals(field_label, 'Estado')

    def test_codigo_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('codigo').verbose_name
        self.assertEquals(field_label, 'Nro. Presupuesto')

    def test_fecha_solicitado_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('fecha_solicitado').verbose_name
        self.assertEquals(field_label, 'Fecha de Solicitud')

    def test_fecha_realizado_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('fecha_realizado').verbose_name
        self.assertEquals(field_label, 'Fecha de Realización')

    def test_fecha_aceptado_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('fecha_aceptado').verbose_name
        self.assertEquals(field_label, 'Fecha de Aceptación')

    def test_usuario_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('usuario').verbose_name
        self.assertEquals(field_label, 'Usuario')

    def test_revisionar_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('revisionar').verbose_name
        self.assertEquals(field_label, 'Revisionar')

    def test_nro_revision_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('nro_revision').verbose_name
        self.assertEquals(field_label, 'Nro. Revisión')

    def test_asistencia_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('asistencia').verbose_name
        self.assertEquals(field_label, 'Asistencia')

    def test_calibracion_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('calibracion').verbose_name
        self.assertEquals(field_label, 'Calibración')

    def test_in_situ_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('in_situ').verbose_name
        self.assertEquals(field_label, 'In Situ')

    def test_lia_label(self):
        presupuesto = Presupuesto.objects.get(id=1)
        field_label = presupuesto._meta.get_field('lia').verbose_name
        self.assertEquals(field_label, 'LIA')