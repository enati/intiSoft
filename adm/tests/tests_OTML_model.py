# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import OTML, Usuario


class OTMLTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Usuario.objects.create(id=1)
        usuario = Usuario.objects.get(id=1)
        OTML.objects.create(id=1,
                            usuario=usuario,
                            usuarioRep=usuario)

    def test_estado_label(self):
        otml = OTML.objects.get(id=1)
        field_label = otml._meta.get_field("estado").verbose_name
        self.assertEquals(field_label, "Estado")

    def test_codigo_label(self):
        otml = OTML.objects.get(id=1)
        field_label = otml._meta.get_field("codigo").verbose_name
        self.assertEquals(field_label, "Nro. OT")

    def test_vpe_label(self):
        otml = OTML.objects.get(id=1)
        field_label = otml._meta.get_field("vpe").verbose_name
        self.assertEquals(field_label, "VPE")

    def test_vpr_label(self):
        otml = OTML.objects.get(id=1)
        field_label = otml._meta.get_field("vpr").verbose_name
        self.assertEquals(field_label, "VPR")

    def test_vpuu_label(self):
        otml = OTML.objects.get(id=1)
        field_label = otml._meta.get_field("vpuu").verbose_name
        self.assertEquals(field_label, "VPUU")

    def test_usuario_label(self):
        otml = OTML.objects.get(id=1)
        field_label = otml._meta.get_field("usuario").verbose_name
        self.assertEquals(field_label, "Usuario")

    def test_usuarioRep_label(self):
        otml = OTML.objects.get(id=1)
        field_label = otml._meta.get_field("usuarioRep").verbose_name
        self.assertEquals(field_label, "Usuario Representado")

    def test_checkbox_sot_label(self):
        otml = OTML.objects.get(id=1)
        field_label = otml._meta.get_field("checkbox_sot").verbose_name
        self.assertEquals(field_label, "SOT de otro centro")