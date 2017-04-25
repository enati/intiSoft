# -*- coding: utf-8 -*-
from django.test import TestCase
from adm.models import Usuario, Presupuesto, OTML, SOT, RUT
from datetime import datetime


class UsuarioTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Usuario.objects.create(id=1,
                               nombre="John Doe 1")

    def setUp(self):
        Usuario.objects.create(id=2,
                               nombre="John Doe 2")
        Usuario.objects.create(id=3,
                               nombre="John Doe 3")
        Usuario.objects.create(id=4,
                               nombre="John Doe 4")
        Usuario.objects.create(id=5,
                               nombre="John Doe 5")
        usuario_presup = Usuario.objects.get(id=2)
        Presupuesto.objects.create(id=1,
                                   codigo='00001',
                                   fecha_solicitado=datetime.now().date(),
                                   usuario=usuario_presup)
        usuario_otml = Usuario.objects.get(id=3)
        OTML.objects.create(id=1,
                            usuario=usuario_otml,
                            usuarioRep=usuario_otml)
        usuario_sot = Usuario.objects.get(id=4)
        SOT.objects.create(id=1,
                           deudor=usuario_sot,
                           ejecutor=usuario_sot,
                           fecha_prevista=datetime.now().date(),
                           firmada=False,
                           descuento_fijo=False)
        usuario_rut = Usuario.objects.get(id=4)
        RUT.objects.create(id=1,
                           deudor=usuario_rut,
                           ejecutor=usuario_rut,
                           fecha_prevista=datetime.now().date(),
                           firmada=False,
                           descuento_fijo=False)

    def test_nro_usuario_label(self):
        usuario = Usuario.objects.get(id=1)
        field_label = usuario._meta.get_field("nro_usuario").verbose_name
        self.assertEquals(field_label, "Nro. Usuario")

    def test_nombre_label(self):
        usuario = Usuario.objects.get(id=1)
        field_label = usuario._meta.get_field("nombre").verbose_name
        self.assertEquals(field_label, "Nombre")

    def test_cuit_label(self):
        usuario = Usuario.objects.get(id=1)
        field_label = usuario._meta.get_field("cuit").verbose_name
        self.assertEquals(field_label, "Cuit")

    def test_mail_label(self):
        usuario = Usuario.objects.get(id=1)
        field_label = usuario._meta.get_field("mail").verbose_name
        self.assertEquals(field_label, "Mail")

    def test_rubro_label(self):
        usuario = Usuario.objects.get(id=1)
        field_label = usuario._meta.get_field("rubro").verbose_name
        self.assertEquals(field_label, "Rubro")

    def test_delete_if_has_presupuesto_in_borrador(self):
        usuario = Presupuesto.objects.get(id=1).usuario
        self.assertFalse(usuario._delete())

    def test_delete_if_has_presupuesto_in_activo(self):
        presupuesto = Presupuesto.objects.get(id=1)
        usuario = presupuesto.usuario
        presupuesto._toState_aceptado()
        self.assertEquals(presupuesto.estado, "aceptado")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_presupuesto_in_facturacion(self):
        presupuesto = Presupuesto.objects.get(id=1)
        usuario = presupuesto.usuario
        presupuesto._toState_en_proceso_de_facturacion()
        self.assertEquals(presupuesto.estado, "en_proceso_de_facturacion")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_presupuesto_in_finalizado(self):
        presupuesto = Presupuesto.objects.get(id=1)
        usuario = presupuesto.usuario
        presupuesto._toState_finalizado()
        self.assertEquals(presupuesto.estado, "finalizado")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_presupuesto_in_cancelado(self):
        presupuesto = Presupuesto.objects.get(id=1)
        usuario = presupuesto.usuario
        presupuesto._toState_cancelado()
        self.assertEquals(presupuesto.estado, "cancelado")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_OTML_in_sin_facturar(self):
        otml = OTML.objects.get(id=1)
        usuario = otml.usuario
        self.assertFalse(usuario._delete())

    def test_delete_if_has_OTML_in_no_pago(self):
        otml = OTML.objects.get(id=1)
        usuario = otml.usuario
        otml._toState_no_pago()
        self.assertEquals(otml.estado, "no_pago")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_OTML_in_pagado(self):
        otml = OTML.objects.get(id=1)
        usuario = otml.usuario
        otml._toState_pagado()
        self.assertEquals(otml.estado, "pagado")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_OTML_in_cancelado(self):
        otml = OTML.objects.get(id=1)
        usuario = otml.usuario
        otml._toState_cancelado()
        self.assertEquals(otml.estado, "cancelado")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_SOT_in_borrador(self):
        sot = SOT.objects.get(id=1)
        usuario = sot.deudor
        self.assertFalse(usuario._delete())

    def test_delete_if_has_SOT_in_pendiente(self):
        sot = SOT.objects.get(id=1)
        usuario = sot.deudor
        sot._toState_pendiente()
        self.assertEquals(sot.estado, "pendiente")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_SOT_in_cobrada(self):
        sot = SOT.objects.get(id=1)
        usuario = sot.deudor
        sot._toState_cobrada(False)
        self.assertEquals(sot.estado, "cobrada")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_SOT_in_cancelada(self):
        sot = SOT.objects.get(id=1)
        usuario = sot.deudor
        sot._toState_cancelada()
        self.assertEquals(sot.estado, "cancelada")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_RUT_in_borrador(self):
        rut = RUT.objects.get(id=1)
        usuario = rut.deudor
        self.assertFalse(usuario._delete())

    def test_delete_if_has_RUT_in_pendiente(self):
        rut = RUT.objects.get(id=1)
        usuario = rut.deudor
        rut._toState_pendiente()
        self.assertEquals(rut.estado, "pendiente")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_RUT_in_cobrada(self):
        rut = RUT.objects.get(id=1)
        usuario = rut.deudor
        rut._toState_cobrada(False)
        self.assertEquals(rut.estado, "cobrada")
        self.assertFalse(usuario._delete())

    def test_delete_if_has_RUT_in_cancelada(self):
        rut = RUT.objects.get(id=1)
        usuario = rut.deudor
        rut._toState_cancelada()
        self.assertEquals(rut.estado, "cancelada")
        self.assertFalse(usuario._delete())