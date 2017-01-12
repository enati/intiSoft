# -*- coding: utf-8 -*-
from django.db import models
from django_extensions.db.models import TimeStampedModel
from audit_log.models import AuthStampedModel
from django_permanent.models import PermanentModel
from adm.signals import *
from django.db.models.signals import post_init, pre_save
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from django.db import connection
from intiSoft.exception import StateError
import reversion
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Dias laborales
(LUN, MAR, MIE, JUE, VIE, SAB, DOM) = range(7)


def sumarDiasHabiles(fecha_origen, dias, feriados=(), diasHabiles=(LUN, MAR, MIE, JUE, VIE)):
    """ Suma 'dias' habiles a 'fecha_origen' """
    semanas, dias = divmod(dias, len(diasHabiles))
    res = fecha_origen + timedelta(weeks=semanas)
    lo, hi = min(fecha_origen, res), max(fecha_origen, res)
    count = len([h for h in feriados if h >= lo and h <= hi])
    dias += count * (-1 if dias < 0 else 1)
    for _ in range(dias):
        res += timedelta(days=1)
        while res in feriados or res.weekday() not in diasHabiles:
            res += timedelta(days=1)
    return res


@reversion.register()
class Usuario(TimeStampedModel, AuthStampedModel):
    nro_usuario = models.CharField(validators=[RegexValidator(r'^\d{5}$')],
                                   max_length=5, blank=True,
                                   null=True)
    nombre = models.CharField(max_length=150, blank=False, unique=True,
                            error_messages={'unique': "Ya existe un usuario con ese nombre."})
    cuit = models.CharField(validators=[RegexValidator(r'^\d{11}$')],
                                        max_length=11, blank=True, null=True)
    mail = models.CharField(max_length=50, blank=True, null=True)
    rubro = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre.encode('utf-8')

    def _delete(self):
        """Faltarian las validaciones"""
        # Chequeo que el usuario no este asociado a ningun presupuesto
        if self.presupuesto_set.all():
            return False
        else:
            self.delete()
            return True

    class Meta:
        ordering = ['nombre']


@reversion.register()
class OfertaTec(TimeStampedModel, AuthStampedModel, PermanentModel):

    proveedor = models.IntegerField(default='106', verbose_name='Proveedor')
    codigo = models.CharField(validators=[RegexValidator(r'^\d{14}$')],
                              max_length=14, verbose_name='Codigo')
    rubro = models.CharField(max_length=50, verbose_name='Rubro')
    subrubro = models.CharField(max_length=50, verbose_name='Subrubro')
    tipo_servicio = models.CharField(max_length=20,
                                     verbose_name='Tipo de Servicio')
    area = models.CharField(max_length=15, verbose_name='Area')
    detalle = models.CharField(max_length=350, verbose_name='Detalle')
    precio = models.FloatField(verbose_name='Precio')

    def __str__(self):
        return self.codigo

    def _delete(self):
        """Faltarian las validaciones"""
        # Chequeo que no este asociada a ningun turno
        if self.ofertatec_linea_set.all():
            return False
        else:
            self.delete()
            return True

    class Meta:
        ordering = ['codigo']


# Ultimo codigo disponible (sin tener en cuenta saltos)
#def nextCode():
    #lastCode = Presupuesto.objects.order_by('codigo').last()
    #if lastCode:
        #n = str(int(lastCode.codigo) + 1)
        #zeros = '0' * (5 - len(n))
        #return zeros + n
    #return '00001'

# Ultimo codigo disponible (teniendo en cuenta saltos,
# empezando desde el 05869)
def nextCode():
    cursor = connection.cursor()
    cursor.execute("""SELECT (t1.codigo + 1)
                     FROM adm_presupuesto t1
                     WHERE
                         NOT EXISTS
                            (SELECT t2.codigo FROM adm_presupuesto t2 WHERE t2.codigo = t1.codigo + 1)
                         AND t1.codigo > 5869
                         AND LENGTH(t1.codigo) = 5
                     """)
    row = cursor.fetchone()
    if row:
        n = str(int(row[0]))
        zeros = '0' * (5 - len(n))
        return zeros + n
    else:
        return '00001'

   #cursor.execute("""SELECT (t1.codigo + 1) as gap_starts_at,
                     #(SELECT MIN(t3.codigo) -1 FROM adm_presupuesto t3 WHERE t3.codigo > t1.codigo) as gap_ends_at
                     #FROM adm_presupuesto t1
                     #WHERE NOT EXISTS (SELECT t2.codigo FROM adm_presupuesto t2 WHERE t2.codigo = t1.codigo + 1)
                     #HAVING gap_ends_at IS NOT NULL""")


@reversion.register(follow=["usuario", "turno_set"])
class Presupuesto(TimeStampedModel, AuthStampedModel, PermanentModel):

    old_fecha_aceptado = None

    ESTADOS = (
        ('borrador', 'Borrador'),     # El primer valor es el que se guarda en la DB
        ('aceptado', 'Aceptado'),
        ('en_proceso_de_facturacion', 'En Proceso de Facturacion'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )

    estado = models.CharField(max_length=25, choices=ESTADOS,
                              default='borrador', verbose_name='Estado')
    codigo = models.CharField(max_length=15, verbose_name='Nro. Presupuesto',
                              unique=True, default=nextCode,
                              error_messages={'unique': "Ya existe un presupuesto con ese número."})
    fecha_solicitado = models.DateField('Fecha de Solicitud')
    fecha_realizado = models.DateField(verbose_name='Fecha de Presupuesto',
                                       blank=True, null=True)
    fecha_aceptado = models.DateField(verbose_name='Fecha de Aceptacion',
                                      blank=True, null=True)
    fecha_instrumento = models.DateField('Llegada de instrumento',
                                         blank=True, null=True)
    usuario = models.ForeignKey(Usuario, verbose_name='Usuario',
                                on_delete=models.PROTECT)
    nro_recepcion = models.CharField(max_length=15, verbose_name='Nro. Recibo de Recepcion',
                                     blank=True, null=True)
    revisionar = models.BooleanField(default=False)
    nro_revision = models.IntegerField(default=0)
    asistencia = models.BooleanField('Asistencia')
    calibracion = models.BooleanField('Calibración')
    in_situ = models.BooleanField('In Situ')
    lia = models.BooleanField('LIA')

    def __str__(self):
        return self.codigo

    def get_turno_activo(self):
        if self.estado == 'cancelado':
            turno = self.turno_set.order_by('-created')
        else:
            turno = self.turno_set.select_related().filter(estado__in=['en_espera',
                                                                        'activo',
                                                                        'finalizado'])
        return turno[0] if turno else None

    def _toState_aceptado(self):
        """Faltarian las validaciones"""
        self.estado = 'aceptado'
        self.save()
        turno = self.get_turno_activo()
        if turno:
            turno.estado = 'activo'
            turno.save()
        return True

    def _toState_borrador(self):
        self.estado = 'borrador'
        self.save()
        # Paso a borrador el turno asociado
        turno = self.get_turno_activo()
        if turno:
            turno.estado = 'en_espera'
            turno.save()
        return True

    def _toState_en_proceso_de_facturacion(self):
        self.estado = 'en_proceso_de_facturacion'
        self.save()
        return True

    def _toState_finalizado(self):
        self.estado = 'finalizado'
        self.save()
        return True

    def _toState_cancelado(self):
        if self.estado == 'finalizado':
            raise StateError('No se pueden cancelar los presupuestos finalizados.', '')
        self.estado = 'cancelado'
        self.save()
        # Cancelo el turno activo asociado, de haberlo
        turno = self.get_turno_activo()
        if turno and turno.estado != 'cancelado':
            turno.estado = 'cancelado'
            turno.save()
        return True

    def _delete(self):
        # Dado que el modelo es persistente, hay problemas cuando elimino una instancia y quiero reusar
        # el mismo codigo para uno nuevo ya que no se admiten duplicados.
        # Luego, al eliminar una instancia le agrego un número de 0 a 9 delante del codigo (se permite
        # tener hasta nueva instancias eliminadas del mismo codigo, despues se empiezan a pisar.
        deleted_presupuestos = Presupuesto.deleted_objects.filter(codigo__endswith=self.codigo).order_by('codigo')
        if deleted_presupuestos:
            # Ya elimine un presupuesto con el mismo codigo.
            if int(deleted_presupuestos.last().codigo[0]) < 9:
                # Hay menos de 9 instancias eliminadas con el mismo codigo luego sigo la numeracion.
                new_code = int(deleted_presupuestos.last().codigo) + 100000
                self.codigo = str(new_code)
                self.save()
            else:
                # Hay 9 instancias eliminadas con el mismo codigo luego borro la primera y corro toda
                # la numeracion.
                deleted_presupuestos[0].delete(force=True)
                for rut in deleted_presupuestos[1:]:
                    rut.codigo = str(int(rut.codigo) - 100000)
                    rut.save()
                self.codigo = str(int(self.codigo) + 900000)
                self.save()
        else:
            # Es la primer instancia eliminada con dicho codigo luego le concateno un 1 delante.
            self.codigo = str(int(self.codigo) + 100000)
            self.save()
        self.delete()
        # Borro todos los turnos asociados
        for t in self.turno_set.all():
            t.delete()
        return True

    def _vigente(self):
        """Retorna true si el presupuesto sigue vigente, false en caso contrario
           El presupuesto esta vigente si se encuentra dentro de los 15 dias de realizado."""
        if self.fecha_realizado:
            fecha_caducidad = sumarDiasHabiles(self.fecha_realizado, 15)
            hoy = datetime.now().date()
            return fecha_caducidad > hoy
        else:
            return False

    class Meta:
        permissions = (("finish_presupuesto", "Can finish presupuesto"),
                       ("cancel_presupuesto", "Can cancel presupuesto"))

# Signals
pre_save.connect(check_state, sender=Presupuesto)
post_init.connect(remember_fecha_aceptado, sender=Presupuesto)


class Contrato(TimeStampedModel, AuthStampedModel, PermanentModel):
    presupuesto = models.ForeignKey(Presupuesto, verbose_name='Presupuesto',
                                    null=True, blank=True, on_delete=models.PROTECT)
    importe_neto = models.FloatField(verbose_name='Importe Neto', blank=False, null=True, default=0)
    importe_bruto = models.FloatField(verbose_name='Importe Bruto', blank=False, null=True, default=0)
    descuento = models.FloatField(verbose_name='Descuento', blank=False, null=True, default=0)
    fecha_realizado = models.DateField(verbose_name='Fecha',
                                       blank=False, null=True)
   # Campos para la relacion inversa
    ot_linea_set = GenericRelation('OT_Linea')

    class Meta:
        abstract = True


def nextOTCode():
    cursor = connection.cursor()
    cursor.execute("""SELECT (t1.codigo + 1)
                     FROM adm_ot t1
                     WHERE NOT EXISTS
                        (SELECT t2.codigo FROM adm_ot t2 WHERE t2.codigo = t1.codigo + 1)
                     AND LENGTH(t1.codigo) = 5
                     """)
    row = cursor.fetchone()
    if row:
        n = str(int(row[0]))
        zeros = '0' * (5 - len(n))
        return zeros + n
    else:
        return '00001'


class OT(Contrato):

    ESTADOS = (
        ('sin_facturar', 'Sin Facturar'),     # El primer valor es el que se guarda en la DB
        ('no_pago', 'No Pago'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado')
    )

    estado = models.CharField(max_length=12, choices=ESTADOS,
                              default='sin_facturar', verbose_name='Estado')
    codigo = models.CharField(max_length=15, verbose_name='Nro. OT',
                              unique=True, default='00000',
                              validators=[RegexValidator(r'^\d{5}\/\d{2}$|^\d{5}$',
                                                         message="El código debe ser de la forma 00000 ó 00000/00")],
                              error_messages={'unique': "Ya existe una OT con ese número."})
    # Campos para la relacion inversa
    factura_set = GenericRelation('Factura')

    def _toState_no_pago(self):
        self.estado = 'no_pago'
        self.save()
        return True

    def _toState_sin_facturar(self):
        self.estado = 'sin_facturar'
        self.save()
        return True

    def _toState_pagado(self, flag):
        # Antes de finalizar la OT chequeo que el presupuesto pueda ser finalizado
        if self.presupuesto.estado != 'en_proceso_de_facturacion':
            raise StateError('El presupuesto debe estar en proceso de facturación antes de poder finalizarlo', '')
        self.estado = 'pagado'
        self.save()
        if flag:
            # Finalizo el presupuesto asociado
            self.presupuesto._toState_finalizado()
            return True

    def _toState_cancelado(self):
        if self.estado == 'finalizado':
            raise StateError('No se pueden cancelar las OT pagadas.', '')
        self.estado = 'cancelado'
        self.save()
        ## Cancelo las facturas asociadas, de haberlas
        for factura in self.factura_set.all():
            if factura.estado != 'cancelada':
                factura.estado = 'cancelada'
                factura.save()
        return True

    def _delete(self):
        # Dado que el modelo es persistente, hay problemas cuando elimino una instancia y quiero reusar
        # el mismo codigo para uno nuevo ya que no se admiten duplicados.
        # Luego, al eliminar una instancia le agrego un número de 0 a 9 delante del codigo (se permite
        # tener hasta nueva instancias eliminadas del mismo codigo, despues se empiezan a pisar.
        deleted_ot = OT.deleted_objects.filter(codigo__endswith=self.codigo).order_by('codigo')
        if deleted_ot:
            # Ya elimine un presupuesto con el mismo codigo.
            if int(deleted_ot.last().codigo[0]) < 9:
                # Hay menos de 9 instancias eliminadas con el mismo codigo luego sigo la numeracion.
                new_code = int(deleted_ot.last().codigo) + 100000
                self.codigo = str(new_code)
                self.save()
            else:
                # Hay 9 instancias eliminadas con el mismo codigo luego borro la primera y corro toda
                # la numeracion.
                deleted_ot[0].delete(force=True)
                for rut in deleted_ot[1:]:
                    rut.codigo = str(int(rut.codigo) - 100000)
                    rut.save()
                self.codigo = str(int(self.codigo) + 900000)
                self.save()
        else:
            # Es la primer instancia eliminada con dicho codigo luego le concateno un 1 delante.
            self.codigo = str(int(self.codigo) + 100000)
            self.save()
        self.delete()
        return True

    class Meta:
        permissions = (("cancel_ot", "Can cancel OT"),
                       ("finish_ot", "Can finish OT"),)


class OTML(Contrato):

    ESTADOS = (
        ('sin_facturar', 'Sin Facturar'),     # El primer valor es el que se guarda en la DB
        ('no_pago', 'No Pago'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado')
    )

    estado = models.CharField(max_length=12, choices=ESTADOS,
                              default='sin_facturar', verbose_name='Estado')
    codigo = models.CharField(max_length=15, verbose_name='Nro. OT',
                              unique=True, default='00000',
                              validators=[RegexValidator(r'^\d{5}\/\d{2}$|^\d{5}$',
                                                         message="El código debe ser de la forma 00000 ó 00000/00")],
                              error_messages={'unique': "Ya existe una OT con ese número."})
    vpe = models.CharField(max_length=5, verbose_name='VPE', blank=True, null=True)
    vpu = models.DateField('VPU', blank=True, null=True)
    vpuu = models.DateField('VPUU', blank=True, null=True)
    usuario = models.ForeignKey(Usuario, verbose_name='Usuario', on_delete=models.PROTECT)
    usuarioRep = models.ForeignKey(Usuario, verbose_name='Usuario Representado', on_delete=models.PROTECT,
                                   related_name='usuarioRep_set')
    # Campos para la relacion inversa
    factura_set = GenericRelation('Factura')

    def _toState_no_pago(self):
        self.estado = 'no_pago'
        self.save()
        return True

    def _toState_sin_facturar(self):
        self.estado = 'sin_facturar'
        self.save()
        return True

    def _toState_pagado(self, flag):
        self.estado = 'pagado'
        self.save()

    def _toState_cancelado(self):
        if self.estado == 'finalizado':
            raise StateError('No se pueden cancelar las OT pagadas.', '')
        self.estado = 'cancelado'
        self.save()
        ## Cancelo las facturas asociadas, de haberlas
        for factura in self.factura_set.all():
            if factura.estado != 'cancelada':
                factura.estado = 'cancelada'
                factura.save()
        return True

    def _delete(self):
        # Dado que el modelo es persistente, hay problemas cuando elimino una instancia y quiero reusar
        # el mismo codigo para uno nuevo ya que no se admiten duplicados.
        # Luego, al eliminar una instancia le agrego un número de 0 a 9 delante del codigo (se permite
        # tener hasta nueva instancias eliminadas del mismo codigo, despues se empiezan a pisar.
        deleted_otml = OTML.deleted_objects.filter(codigo__endswith=self.codigo).order_by('codigo')
        if deleted_otml:
            # Ya elimine un presupuesto con el mismo codigo.
            if int(deleted_otml.last().codigo[0]) < 9:
                # Hay menos de 9 instancias eliminadas con el mismo codigo luego sigo la numeracion.
                new_code = int(deleted_otml.last().codigo) + 100000
                self.codigo = str(new_code)
                self.save()
            else:
                # Hay 9 instancias eliminadas con el mismo codigo luego borro la primera y corro toda
                # la numeracion.
                deleted_otml[0].delete(force=True)
                for rut in deleted_otml[1:]:
                    rut.codigo = str(int(rut.codigo) - 100000)
                    rut.save()
                self.codigo = str(int(self.codigo) + 900000)
                self.save()
        else:
            # Es la primer instancia eliminada con dicho codigo luego le concateno un 1 delante.
            self.codigo = str(int(self.codigo) + 100000)
            self.save()
        self.delete()
        return True

    class Meta:
        permissions = (("cancel_otml", "Can cancel OT-ML"),
                       ("finish_otml", "Can finish OT-ML"),)


# Ultimo codigo disponible (teniendo en cuenta saltos,
# empezando desde el 03927)
def nextSOTCode():
    cursor = connection.cursor()
    cursor.execute("""SELECT (t1.codigo + 1)
                     FROM adm_sot t1
                     WHERE
                         NOT EXISTS
                            (SELECT t2.codigo FROM adm_sot t2 WHERE t2.codigo = t1.codigo + 1)
                         AND LENGTH(t1.codigo) = 5
                     """)
    row = cursor.fetchone()
    if row:
        n = str(int(row[0]))
        zeros = '0' * (5 - len(n))
        return zeros + n
    else:
        return '03927'


class SOT(Contrato):

    ESTADOS = (
        ('borrador', 'Borrador'),     # El primer valor es el que se guarda en la DB
        ('pendiente', 'Pendiente'),
        ('cobrada', 'Cobrada'),
        ('cancelada', 'Cancelada')
    )

    AREAS = (
        ('LIA', 'LIA'),
        ('LIM1', 'LIM1'),
        ('LIM2', 'LIM2'),
        ('LIM3', 'LIM3'),
        ('LIM4', 'LIM4'),
        ('LIM5', 'LIM5'),
        ('LIM6', 'LIM6'),
        ('EXT', 'EXT'),
        ('SIS', 'SIS'),
        ('DES', 'DES'),
        ('CAL', 'CAL'),
        ('MEC', 'MEC'),
        ('ML', 'ML'),
    )

    estado = models.CharField(max_length=12, choices=ESTADOS,
                              default='borrador', verbose_name='Estado')
    codigo = models.CharField(max_length=15, verbose_name='Nro. SOT',
                              unique=True, default=nextSOTCode,
                              error_messages={'unique': "Ya existe una SOT con ese número."})
    deudor = models.ForeignKey(Usuario, verbose_name='Usuario',
                               on_delete=models.PROTECT, related_name='sot_deudor')
    ejecutor = models.ForeignKey(Usuario, verbose_name='Usuario', default=1,
                                 on_delete=models.PROTECT, related_name='sot_ejecutor')
    usuario_final = models.ForeignKey(Usuario, verbose_name='Usuario OT', null=True, blank=True,
                                      on_delete=models.PROTECT, related_name='sot_usuario_final')
    ot = models.CharField(max_length=15, verbose_name='Nro. OT', blank=True, null=True)
    expediente = models.CharField(max_length=20, verbose_name='Expediente', blank=True, null=True)
    fecha_envio_ut = models.DateField('Fecha de envio a la UT', blank=True, null=True)
    firmada = models.BooleanField('Retorno firmada')
    fecha_envio_cc = models.DateField('Fecha de envio a CC', blank=True, null=True)
    fecha_prevista = models.DateField('Fecha prevista')
    solicitante = models.CharField(max_length=4, choices=AREAS)
    descuento_fijo = models.BooleanField('Descuento fijo')

    def _toState_pendiente(self):
        self.estado = 'pendiente'
        self.save()
        return True

    def _toState_cobrada(self):
        self.estado = 'cobrada'
        self.save()
        self.presupuesto._toState_finalizado()
        return True

    def _toState_cancelada(self):
        if self.estado == 'cobrada':
            raise StateError('No se pueden cancelar las SOT cobradas.', '')
        self.estado = 'cancelada'
        self.save()
        return True

    def _delete(self):
        # Dado que el modelo es persistente, hay problemas cuando elimino una instancia y quiero reusar
        # el mismo codigo para uno nuevo ya que no se admiten duplicados.
        # Luego, al eliminar una instancia le agrego un número de 0 a 9 delante del codigo (se permite
        # tener hasta nueva instancias eliminadas del mismo codigo, despues se empiezan a pisar.
        deleted_sot = SOT.deleted_objects.filter(codigo__endswith=self.codigo).order_by('codigo')
        if deleted_sot:
            # Ya elimine un presupuesto con el mismo codigo.
            if int(deleted_sot.last().codigo[0]) < 9:
                # Hay menos de 9 instancias eliminadas con el mismo codigo luego sigo la numeracion.
                new_code = int(deleted_sot.last().codigo) + 100000
                self.codigo = str(new_code)
                self.save()
            else:
                # Hay 9 instancias eliminadas con el mismo codigo luego borro la primera y corro toda
                # la numeracion.
                deleted_sot[0].delete(force=True)
                for rut in deleted_sot[1:]:
                    rut.codigo = str(int(rut.codigo) - 100000)
                    rut.save()
                self.codigo = str(int(self.codigo) + 900000)
                self.save()
        else:
            # Es la primer instancia eliminada con dicho codigo luego le concateno un 1 delante.
            self.codigo = str(int(self.codigo) + 100000)
            self.save()
        self.delete()
        return True
    class Meta:
        permissions = (("cancel_sot", "Can cancel SOT"),
                       ("finish_sot", "Can finish SOT"),)

# Signals
pre_save.connect(toState_pendiente, sender=SOT)


# Ultimo codigo disponible (teniendo en cuenta saltos,
# empezando desde el 00454)
def nextRUTCode():
    cursor = connection.cursor()
    cursor.execute("""SELECT (t1.codigo + 1)
                     FROM adm_rut t1
                     WHERE
                         NOT EXISTS
                            (SELECT t2.codigo FROM adm_rut t2 WHERE t2.codigo = t1.codigo + 1)
                            AND LENGTH(t1.codigo) = 5
                     """)
    row = cursor.fetchone()
    if row:
        n = str(int(row[0]))
        zeros = '0' * (5 - len(n))
        return zeros + n
    else:
        return '00454'


class RUT(Contrato):

    ESTADOS = (
        ('borrador', 'Borrador'),     # El primer valor es el que se guarda en la DB
        ('pendiente', 'Pendiente'),
        ('cobrada', 'Cobrada'),
        ('cancelada', 'Cancelada')
    )

    AREAS = (
        ('LIA', 'LIA'),
        ('LIM1', 'LIM1'),
        ('LIM2', 'LIM2'),
        ('LIM3', 'LIM3'),
        ('LIM4', 'LIM4'),
        ('LIM5', 'LIM5'),
        ('LIM6', 'LIM6'),
        ('EXT', 'EXT'),
        ('SIS', 'SIS'),
        ('DES', 'DES'),
        ('CAL', 'CAL'),
        ('MEC', 'MEC'),
        ('ML', 'ML'),
    )

    estado = models.CharField(max_length=12, choices=ESTADOS,
                              default='borrador', verbose_name='Estado')
    codigo = models.CharField(max_length=15, verbose_name='Nro. RUT',
                              unique=True, default=nextRUTCode,
                              error_messages={'unique': "Ya existe una RUT con ese número."})
    deudor = models.ForeignKey(Usuario, verbose_name='Usuario', on_delete=models.PROTECT, related_name='rut_deudor')
    ejecutor = models.ForeignKey(Usuario, verbose_name='Usuario', default=1,
                                 on_delete=models.PROTECT, related_name='rut_ejecutor')
    solicitante = models.CharField(max_length=4, choices=AREAS)
    fecha_envio_ut = models.DateField('Fecha de envio a la UT', blank=True, null=True)
    firmada = models.BooleanField('Retorno firmada')
    fecha_envio_cc = models.DateField('Fecha de envio a CC', blank=True, null=True)
    fecha_prevista = models.DateField('Fecha prevista')
    descuento_fijo = models.BooleanField('Descuento fijo')

    def _toState_pendiente(self):
        self.estado = 'pendiente'
        self.save()
        return True

    def _toState_cobrada(self):
        # Antes de finalizar la RUT chequeo que el presupuesto pueda ser finalizado
        if self.presupuesto.estado != 'en_proceso_de_facturacion':
            raise StateError('El presupuesto debe estar en proceso de facturación antes de poder finalizarlo', '')
        self.estado = 'cobrada'
        self.save()
        self.presupuesto._toState_finalizado()
        return True

    def _toState_cancelada(self):
        if self.estado == 'cobrada':
            raise StateError('No se pueden cancelar las RUT cobradas.', '')
        self.estado = 'cancelada'
        self.save()
        return True

    def _delete(self):
        # Dado que el modelo es persistente, hay problemas cuando elimino una instancia y quiero reusar
        # el mismo codigo para uno nuevo ya que no se admiten duplicados.
        # Luego, al eliminar una instancia le agrego un número de 0 a 9 delante del codigo (se permite
        # tener hasta nueva instancias eliminadas del mismo codigo, despues se empiezan a pisar.
        deleted_ruts = RUT.deleted_objects.filter(codigo__endswith=self.codigo).order_by('codigo')
        if deleted_ruts:
            # Ya elimine un presupuesto con el mismo codigo.
            if int(deleted_ruts.last().codigo[0]) < 9:
                # Hay menos de 9 instancias eliminadas con el mismo codigo luego sigo la numeracion.
                new_code = int(deleted_ruts.last().codigo) + 100000
                self.codigo = str(new_code)
                self.save()
            else:
                # Hay 9 instancias eliminadas con el mismo codigo luego borro la primera y corro toda
                # la numeracion.
                deleted_ruts[0].delete(force=True)
                for rut in deleted_ruts[1:]:
                    rut.codigo = str(int(rut.codigo) - 100000)
                    rut.save()
                self.codigo = str(int(self.codigo) + 900000)
                self.save()
        else:
            # Es la primer instancia eliminada con dicho codigo luego le concateno un 1 delante.
            self.codigo = str(int(self.codigo) + 100000)
            self.save()
        self.delete()
        return True

    class Meta:
        permissions = (("cancel_rut", "Can cancel RUT"),
                       ("finish_rut", "Can finish RUT"),)

# Signals
pre_save.connect(toState_pendiente, sender=RUT)


# Ultimo codigo disponible (teniendo en cuenta saltos,
# empezando desde el 00007)
def nextSICode():
    cursor = connection.cursor()
    cursor.execute("""SELECT (t1.codigo + 1)
                     FROM adm_si t1
                     WHERE NOT EXISTS
                        (SELECT t2.codigo FROM adm_si t2 WHERE t2.codigo = t1.codigo + 1)
                     AND LENGTH(t1.codigo) = 5
                     """)
    row = cursor.fetchone()
    if row:
        n = str(int(row[0]))
        zeros = '0' * (5 - len(n))
        return zeros + n
    else:
        return '00007'


class SI(Contrato):

    ESTADOS = (
        ('borrador', 'Borrador'),     # El primer valor es el que se guarda en la DB
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    )

    AREAS = (
        ('LIA', 'LIA'),
        ('LIM1', 'LIM1'),
        ('LIM2', 'LIM2'),
        ('LIM3', 'LIM3'),
        ('LIM4', 'LIM4'),
        ('LIM5', 'LIM5'),
        ('LIM6', 'LIM6'),
        ('EXT', 'EXT'),
        ('SIS', 'SIS'),
        ('DES', 'DES'),
        ('CAL', 'CAL'),
        ('MEC', 'MEC'),
        ('ML', 'ML'),
    )

    estado = models.CharField(max_length=12, choices=ESTADOS,
                              default='borrador', verbose_name='Estado')
    codigo = models.CharField(max_length=15, verbose_name='Nro. SI',
                              unique=True, default=nextSICode,
                              error_messages={'unique': "Ya existe una SI con ese número."})
    solicitante = models.CharField(max_length=4, choices=AREAS)
    ejecutor = models.CharField(max_length=4, choices=AREAS)
    fecha_prevista = models.DateField('Fecha prevista', blank=True, null=True)
    fecha_fin_real = models.DateField('Finalizacion', blank=True, null=True)
    # Campos para la relacion inversa
    tarea_linea_set = GenericRelation('Tarea_Linea')

    def _toState_finalizada(self):
        self.estado = 'finalizada'
        self.fecha_fin_real = datetime.now().date()
        self.save()
        return True

    def _toState_cancelada(self):
        if self.estado == 'finalizada':
            raise StateError('No se pueden cancelar las SI finalizadas.', '')
        self.estado = 'cancelada'
        self.save()
        return True

    def _delete(self):
        # Dado que el modelo es persistente, hay problemas cuando elimino una instancia y quiero reusar
        # el mismo codigo para uno nuevo ya que no se admiten duplicados.
        # Luego, al eliminar una instancia le agrego un número de 0 a 9 delante del codigo (se permite
        # tener hasta nueva instancias eliminadas del mismo codigo, despues se empiezan a pisar.
        deleted_si = SI.deleted_objects.filter(codigo__endswith=self.codigo).order_by('codigo')
        if deleted_si:
            # Ya elimine un presupuesto con el mismo codigo.
            if int(deleted_si.last().codigo[0]) < 9:
                # Hay menos de 9 instancias eliminadas con el mismo codigo luego sigo la numeracion.
                new_code = int(deleted_si.last().codigo) + 100000
                self.codigo = str(new_code)
                self.save()
            else:
                # Hay 9 instancias eliminadas con el mismo codigo luego borro la primera y corro toda
                # la numeracion.
                deleted_si[0].delete(force=True)
                for rut in deleted_si[1:]:
                    rut.codigo = str(int(rut.codigo) - 100000)
                    rut.save()
                self.codigo = str(int(self.codigo) + 900000)
                self.save()
        else:
            # Es la primer instancia eliminada con dicho codigo luego le concateno un 1 delante.
            self.codigo = str(int(self.codigo) + 100000)
            self.save()
        self.delete()
        return True

    class Meta:
        permissions = (("cancel_si", "Can cancel SOT"),
                       ("finish_si", "Can finish SOT"),)


class Tarea_Linea(TimeStampedModel, AuthStampedModel):

    """ Lineas de tareas de Solicitud Interna """
    tarea = models.CharField(verbose_name='Tarea', max_length=250)
    horas = models.FloatField(verbose_name='Horas')
    arancel = models.FloatField(verbose_name='Arancel', null=True, blank=True)
    # Campos para relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['id']


class OT_Linea(TimeStampedModel, AuthStampedModel):
    """ Lineas de Oferta Tecnologica """

    ofertatec = models.ForeignKey(OfertaTec, verbose_name='OfertaTec')
    codigo = models.CharField(validators=[RegexValidator(r'^\d{14}$')],
                              max_length=14, verbose_name='Codigo')
    precio = models.FloatField(verbose_name='Precio')
    precio_total = models.FloatField(verbose_name='Precio Total')
    cantidad = models.IntegerField(verbose_name='Cantidad', default=1)
    cant_horas = models.FloatField(verbose_name='Horas', blank=True, null=True)
    observaciones = models.TextField(max_length=100, blank=True)
    detalle = models.CharField(max_length=350, verbose_name='Detalle', blank=True, null=True)
    tipo_servicio = models.CharField(max_length=20, verbose_name='Tipo de Servicio', blank=True, null=True)
    # Campos para relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['id']


class Factura(TimeStampedModel, AuthStampedModel):

    ESTADOS = (
        ('activa', 'Activa'),     # El primer valor es el que se guarda en la DB
        ('cancelada', 'Cancelada')
    )

    estado = models.CharField(max_length=12, choices=ESTADOS,
                              default='activa', verbose_name='Estado')
    numero = models.CharField(max_length=15, verbose_name='Nro. Factura')
    fecha = models.DateField(verbose_name='Fecha', blank=False, null=True)
    importe = models.FloatField(verbose_name='Importe', blank=True, null=True, default=0)
    fecha_aviso = models.DateField(verbose_name='Aviso de Trabajo Realizado',
                                       blank=True, null=True)
    # Campos para relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def _toState_cancelado(self):
        if self.estado == 'activa':
            self.estado = 'cancelada'
            self.save()
            contrato_obj = self.content_type.get_object_for_this_type(pk=self.object_id)
            if not(contrato_obj.factura_set.exclude(estado__in=['cancelada'])) and contrato_obj.estado != 'cancelado':
                contrato_obj._toState_sin_facturar()
        return True

    def save(self, *args, **kwargs):
        if not self.pk:
            #This code only happens if the objects is
            #not in the database yet. Otherwise it would
            #have pk
            contrato_obj = self.content_type.get_object_for_this_type(pk=self.object_id)
            if contrato_obj.estado == 'sin_facturar':
                contrato_obj._toState_no_pago()
        super(Factura, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        res = super(Factura, self).delete(*args, **kwargs)
        # Si borre la ultima factura asociada a una OT,
        # vuelvo la OT a estado sin_facturar
        contrato_obj = self.content_type.get_object_for_this_type(pk=self.object_id)
        if not(contrato_obj.factura_set.exclude(estado__in=['cancelada'])):
            contrato_obj._toState_sin_facturar()
        return res

    class Meta:
        ordering = ['id']
        permissions = (("cancel_factura", "Can cancel factura"),)


class Recibo(TimeStampedModel, AuthStampedModel):

    CHOICES = (
        ('recibo', 'Recibo'),     # El primer valor es el que se guarda en la DB
        ('nota_credito', 'Nota De Credito'),
    )

    comprobante_cobro = models.CharField(max_length=20, choices=CHOICES, verbose_name='Comprobante De Cobro')
    numero = models.CharField(max_length=15, verbose_name='Nro.')
    fecha = models.DateField(verbose_name='Fecha', blank=False, null=True)
    importe = models.FloatField(verbose_name='Importe', blank=True, null=True, default=0)
    factura = models.ForeignKey(Factura, verbose_name='Factura', on_delete=models.CASCADE)

    #def save(self, *args, **kwargs):
        #if not self.pk:
            ##This code only happens if the objects is
            ##not in the database yet. Otherwise it would
            ##have pk
            #factura_obj = Factura.objects.get(pk=self.factura_id)
            #ot_obj = OT.objects.get(pk=factura_obj.ot_id)
            #if ot_obj.estado == 'no_pago':
                #ot_obj._toState_pagado()
        #super(Recibo, self).save(*args, **kwargs)

    #def delete(self, *args, **kwargs):
        #res = super(Recibo, self).delete(*args, **kwargs)
        ## Si borre el ultimo recibo asociado a una OT,
        ## vuelvo la OT a estado no_pago
        #factura_obj = Factura.objects.get(pk=self.factura_id)
        #ot_obj = OT.objects.get(pk=factura_obj.ot_id)
        #for factura in ot_obj.factura_set.all():
            #if (factura.recibo_set.all()):
                #return res
        #ot_obj._toState_no_pago()
        #return res

    class Meta:
        ordering = ['id']


class Remito(TimeStampedModel, AuthStampedModel):

    numero = models.CharField(max_length=15, verbose_name='Nro.')
    fecha = models.DateField(verbose_name='Fecha', blank=False, null=True)
    ot = models.ForeignKey(OT, verbose_name='OT', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


