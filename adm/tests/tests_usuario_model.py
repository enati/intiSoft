# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Usuario


class UsuarioTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Usuario.objects.create(nombre="John Doe")

    def test_nro_usuario_label(self):
        usuario = Usuario.objects.get(nombre="John Doe")
        field_label = usuario._meta.get_field("nro_usuario").verbose_name
        self.assertEquals(field_label, "Nro. Usuario")

    def test_nombre_label(self):
        usuario = Usuario.objects.get(nombre="John Doe")
        field_label = usuario._meta.get_field("nombre").verbose_name
        self.assertEquals(field_label, "Nombre")

    def test_cuit_label(self):
        usuario = Usuario.objects.get(nombre="John Doe")
        field_label = usuario._meta.get_field("cuit").verbose_name
        self.assertEquals(field_label, "Cuit")

    def test_mail_label(self):
        usuario = Usuario.objects.get(nombre="John Doe")
        field_label = usuario._meta.get_field("mail").verbose_name
        self.assertEquals(field_label, "Mail")

    def test_rubro_label(self):
        usuario = Usuario.objects.get(nombre="John Doe")
        field_label = usuario._meta.get_field("rubro").verbose_name
        self.assertEquals(field_label, "Rubro")
