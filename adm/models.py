# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from audit_log.models import AuthStampedModel
from django_permanent.models import PermanentModel
from adm.signals import *
from django.db.models.signals import post_init, pre_save, post_save, post_delete, pre_delete
from django.core.validators import RegexValidator, EmailValidator
from datetime import datetime, timedelta
from django.db import connection
from intiSoft.exception import StateError
import reversion
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from adm.validators import alphabetic

# Dias laborales
(LUN, MAR, MIE, JUE, VIE, SAB, DOM) = range(7)

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
    nro_usuario = models.CharField("Nro. Usuario", validators=[RegexValidator(r'^\d{5}$')],
                                   max_length=5, blank=True,
                                   null=True)
    nombre = models.CharField("Razón Social", max_length=150, blank=False, unique=True,
                            error_messages={'unique': "Ya existe un usuario con ese nombre."})
    cuit = models.CharField("Cuit", validators=[RegexValidator(r'^\d{11}$')],
                                        max_length=11, blank=True, null=True)
    mail = models.CharField("Mail", max_length=50, null=True,
                            validators=[EmailValidator(message="Ingrese un email válido.")])
    rubro = models.CharField("Rubro", max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre.encode('utf-8')

    def _delete(self):
        try:
            self.delete()
        except:
            return False
        return True

    class Meta:
        ordering = ['nombre']


class Provincia(TimeStampedModel, AuthStampedModel):

    abreviatura = models.CharField("Abraviatura", max_length=3)
    nombre = models.CharField("Nombre", max_length=50)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        ordering = ['nombre']


class Localidad(TimeStampedModel, AuthStampedModel):

    nombre = models.CharField("Nombre", max_length=50)
    cp = models.CharField("CP", max_length=4)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)

    def __unicode__(self):
        return unicode(self.nombre)

    class Meta:
        ordering = ['nombre']


@reversion.register()
class DireccionUsuario(TimeStampedModel, AuthStampedModel):

    calle = models.CharField("Dirección", max_length=50)
    numero = models.CharField("Número", max_length=10)
    piso = models.CharField("Piso/Dpto", max_length=10, blank=True)
    localidad = models.ForeignKey(Localidad, verbose_name="Localidad")
    provincia = models.ForeignKey(Provincia, verbose_name="Provincia")
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)

    def __unicode__(self):
        return unicode(self.calle) + " " + unicode(self.numero) + " " + unicode(self.piso) +\
               " (" + unicode(self.provincia) + ", " + unicode(self.localidad) + ")"

    class Meta:
        verbose_name = 'Direccion'
        ordering = ['id']


@reversion.register()
class Contacto(TimeStampedModel, AuthStampedModel):

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre", max_length=100, validators=[alphabetic])
    telefono = models.CharField("Telefono", max_length=20, blank=True)
    mail = models.CharField("Mail", max_length=250, validators=[EmailValidator(message="Ingrese un email válido.")])

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ['id']


@reversion.register()
class OfertaTec(TimeStampedModel, AuthStampedModel, PermanentModel):

    proveedor = models.IntegerField("Proveedor", default='106')
    codigo = models.CharField("Código", validators=[RegexValidator(r'^\d{14}$')],
                              max_length=14)
    rubro = models.CharField("Rubro", max_length=50)
    subrubro = models.CharField("Subrubro", max_length=50)
    tipo_servicio = models.CharField("Tipo de Servicio", max_length=20)
    area = models.CharField("Area", max_length=15)
    detalle = models.CharField("Detalle", max_length=350)
    precio = models.FloatField("Precio")

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


def yearNow():
    return datetime.now().year


@reversion.register()
class PDT(TimeStampedModel, AuthStampedModel):
    """ Planes de Trabajo """
    YEARS = []
    for y in range(2017, datetime.now().year + 3):
        YEARS.append((str(y), str(y)))

    TIPO_PLAN = [('POA', 'POA'), ('PDI', 'PDI')]

    # Indica si el registro es una contribucion de un plan de otro centro
    contribucion = models.BooleanField("Contribución", default=False)
    anio = models.CharField("Año", max_length=4, choices=YEARS, default=yearNow, null=True)
    tipo = models.CharField("Tipo de Plan", max_length=3, choices=TIPO_PLAN, null=True, blank=False)
    nombre = models.CharField("Nombre", max_length=500)
    codigo = models.CharField("Código", max_length=5, unique=True,
                     error_messages={'unique': "Código duplicado."})
    cantidad_servicios = models.PositiveIntegerField("Cantidad de Servicios", default=0, null=True)
    cantidad_contratos = models.PositiveIntegerField("Cantidad de OT/SOT/RUT Anuales", default=0, null=True)
    facturacion_prevista = models.FloatField("Facturación Anual Prevista por OT", default=0, null=True)
    generacion_neta = models.FloatField("Generación Neta", default=0, null=True)
    agentes = models.ManyToManyField(User)

    def __unicode__(self):
        return "%s - %s" % (self.codigo, self.nombre)

    def _delete(self):
        """Faltarian las validaciones"""
        # Chequeo que no este asociada a ningun documento
        if self.ot_set.all() or self.otml_set.all() or self.sot_set.all() or self.rut_set.all() or self.si_set.all():
            return False
        else:
            self.delete()
            return True

    def get_total_servicios(self):
        count = 0
        for ot in self.ot_set.all().exclude(estado='cancelado'):
            count += ot.get_servicios()
        for otml in self.otml_set.all().exclude(estado='cancelado'):
            count += otml.get_servicios()
        for sot in self.sot_set.all().exclude(estado='cancelada'):
            count += sot.get_servicios()
        for rut in self.rut_set.all().exclude(estado='cancelada'):
            count += rut.get_servicios()
        return count

    def get_total_contratos(self):
        count = 0
        count += len(self.ot_set.all().exclude(estado='cancelado'))
        count += len(self.otml_set.all().exclude(estado='cancelado'))
        count += len(self.sot_set.all().exclude(estado='cancelada'))
        count += len(self.rut_set.all().exclude(estado='cancelada'))
        return count

    def get_total_facturacion(self):
        count = 0
        for ot in self.ot_set.all().exclude(estado='cancelado'):
            count += ot.get_facturacion()
        for otml in self.otml_set.all().exclude(estado='cancelado'):
            count += otml.get_facturacion()
        for sot in self.sot_set.all().exclude(estado='cancelada'):
            count += sot.get_facturacion()
        for rut in self.rut_set.all().exclude(estado='cancelada'):
            count += rut.get_facturacion()
        return count

    def get_total_importe_neto(self):
        count = 0
        count += sum(self.ot_set.all().exclude(estado='cancelado').values_list('importe_neto', flat=True))
        count += sum(self.otml_set.all().exclude(estado='cancelado').values_list('importe_neto', flat=True))
        count += sum(self.sot_set.all().exclude(estado='cancelada').values_list('importe_neto', flat=True))
        count += sum(self.rut_set.all().exclude(estado='cancelada').values_list('importe_neto', flat=True))
        return count

    class Meta:
        ordering = ['anio', 'codigo']
        permissions = (("read_pdt", "Can read pdt"),)


@reversion.register(follow=["usuario", "direccion", "contacto", "turno_set", "instrumento_set", "pdt"])
class Presupuesto(TimeStampedModel, AuthStampedModel, PermanentModel):

    ESTADOS = (
        ('borrador', 'Borrador'),     # El primer valor es el que se guarda en la DB
        ('aceptado', 'Aceptado'),
        ('en_proceso_de_facturacion', 'En Proceso de Facturacion'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )

    TIPOS = (
        ('calibracion', 'Calibración'),
        ('asistencia', 'Asistencia'),
        ('in_situ', 'In Situ'),
        ('lia', 'LIA'),
        ('mat_ref', 'Materiales de Referencia'),
    )

    estado = models.CharField('Estado', max_length=25, choices=ESTADOS, default='borrador')
    codigo = models.CharField('Nro. Presupuesto', max_length=15,
                              unique=True, default=nextCode,
                              error_messages={'unique': "Ya existe un presupuesto con ese número."})
    fecha_solicitado = models.DateField('Fecha de Solicitud')
    fecha_realizado = models.DateField('Fecha de Realización',
                                       blank=True, null=True)
    fecha_aceptado = models.DateField('Fecha de Aceptación',
                                      blank=True, null=True)
    usuario = models.ForeignKey(Usuario, verbose_name='Usuario',
                                on_delete=models.PROTECT)
    contacto = models.ForeignKey(Contacto, verbose_name='Contacto',
                                on_delete=models.PROTECT, null=True, blank=True)
    direccion = models.ForeignKey(DireccionUsuario, verbose_name='Direccion',
                                  on_delete=models.PROTECT, null=True, blank=True)
    revisionar = models.BooleanField('Revisionar', default=False)
    nro_revision = models.IntegerField('Nro. Revisión', default=0)
    tipo = models.CharField('Tipo', max_length=11, choices=TIPOS, default='calibracion')
    pdt = models.ForeignKey(PDT, verbose_name="PDT", null=True, blank=False)

    def __str__(self):
        return self.codigo


    def write_activity_log(self, activity, comments="Registro automático"):
        content_type_obj = ContentType.objects.get(model="presupuesto")
        ActivityLog.objects.create(content_type=content_type_obj,
                                   object_id=self.pk,
                                   activity=activity,
                                   comments=comments)
        return True

    def get_area(self):
        areas = []
        for turno in self.get_turnos_activos():
            areas.append(turno.area)
        return areas


    def get_turnos_activos(self):
        if self.estado == 'cancelado':
            return self.turno_set.order_by('-created')
        else:
            return self.turno_set.select_related().filter(estado__in=['en_espera',
                                                                        'activo',
                                                                        'finalizado'])

    def _toState_aceptado(self):
        """Faltarian las validaciones"""
        self.estado = 'aceptado'
        self.save()
        turnoList = self.get_turnos_activos()
        for turno in turnoList:
            turno._toState_activo()
        return True

    def _toState_borrador(self):
        self.estado = 'borrador'
        self.save()
        # Paso a borrador el turno asociado
        turnoList = self.get_turnos_activos()
        for turno in turnoList:
            turno._toState_en_espera()
        return True

    def _toState_en_proceso_de_facturacion(self):
        self.estado = 'en_proceso_de_facturacion'
        self.save()
        return True

    def _toState_finalizado(self):
        self.estado = 'finalizado'
        self.save()
        return True

    def _toState_cancelado(self, obs=''):
        if self.estado == 'finalizado':
            raise StateError('No se pueden cancelar los presupuestos finalizados.', '')
        self.estado = 'cancelado'
        self._obs = obs
        self.save()
        # Cancelo el turno activo asociado, de haberlo
        turnoList = self.get_turnos_activos()
        for turno in turnoList:
                turno._toState_cancelado(obs='Registro automático: Presupuesto cancelado')
        return True

    def _delete(self):
        # Solo se pueden borrar los presupuestos en estado borrador
        if self.estado != 'borrador':
            raise StateError('Solo se pueden borrar presupuestos en estado Borrador', '')
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
        ordering = ["-codigo"]
        permissions = (("finish_presupuesto", "Can finish presupuesto"),
                       ("cancel_presupuesto", "Can cancel presupuesto"),
                       ("read_presupuesto", "Can read presupuesto"))

# Signals
pre_save.connect(check_state, sender=Presupuesto, dispatch_uid="presupuesto.check_state")
pre_save.connect(log_state_change, sender=Presupuesto, dispatch_uid="presupuesto.log_state_change")
post_save.connect(log_create, sender=Presupuesto, dispatch_uid="presupuesto.log_create")
post_delete.connect(on_delete_presupuesto, sender=Presupuesto, dispatch_uid="presupuesto.on_delete_presupuesto")


@reversion.register()
class Instrumento(TimeStampedModel, AuthStampedModel):

    detalle = models.CharField("Detalle", max_length=150, blank=True, null=True)
    fecha_llegada = models.DateField("Fecha de Llegada")
    nro_recepcion = models.CharField("Nro. Recibo de Recepción", max_length=15)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, verbose_name="Presupuesto")

    class Meta:
        ordering = ["fecha_llegada"]


def user_unicode(self):
    return  u'%s %s' % (self.first_name, self.last_name)

User.__unicode__ = user_unicode


class Contrato(TimeStampedModel, AuthStampedModel, PermanentModel):
    presupuesto = models.ForeignKey(Presupuesto, verbose_name="Presupuesto",
                                    null=True, blank=True, on_delete=models.PROTECT)
    importe_neto = models.FloatField("Importe Neto", blank=False, null=True, default=0)
    importe_bruto = models.FloatField("Importe Bruto", blank=False, null=True, default=0)
    descuento = models.FloatField("Descuento", blank=False, null=True, default=0)
    fecha_realizado = models.DateField("Fecha de Realización", blank=False, null=True)
    pdt = models.ForeignKey(PDT, verbose_name="PDT", null=True, blank=False)

    def write_activity_log(self, activity, comments="Registro automático"):
        content_type_obj = ContentType.objects.get(model=self.__class__.__name__)
        ActivityLog.objects.create(content_type=content_type_obj,
                                   object_id=self.pk,
                                   activity=activity,
                                   comments=comments)

    def get_servicios(self):
        count = 0
        for ot_linea in self.ot_linea_set.all():
            count += ot_linea.cantidad
        return count

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

    estado = models.CharField("Estado", max_length=12, choices=ESTADOS, default="sin_facturar")
    codigo = models.CharField("Nro. OT", max_length=15, unique=True, default='00000',
                              validators=[RegexValidator(r'^\d{5}\/\d{2}$|^\d{5}$',
                                                         message="El código debe ser de la forma 00000 ó 00000/00")],
                              error_messages={'unique': "Ya existe una OT con ese número."})
    # Campos para la relacion inversa
    factura_set = GenericRelation("Factura", verbose_name="Factura")
    ot_linea_set = GenericRelation("OT_Linea", verbose_name="Líneas de OT")
    remito_set = GenericRelation("Remito", verbose_name="Remito")


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

    def _toState_cancelado(self, obs=''):
        if self.estado == 'finalizado':
            raise StateError('No se pueden cancelar las OT pagadas.', '')
        self.estado = 'cancelado'
        self._obs = obs
        self.save()
        ## Cancelo las facturas asociadas, de haberlas
        for factura in self.factura_set.all():
            if factura.estado != 'cancelada':
                factura.estado = 'cancelada'
                factura.save()
        return True

    def _delete(self):
        if self.estado != 'sin_facturar':
            raise StateError('Solo se pueden borrar OTs que estén sin facturar', '')
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

    def get_facturacion(self):
        count = 0
        if self.estado in ['no_pago', 'pagado']:
            for factura in self.factura_set.all():
                count += factura.importe
        return count

    class Meta:
        permissions = (("cancel_ot", "Can cancel OT"),
                       ("finish_ot", "Can finish OT"),
                       ("read_ot", "Can read OT"))

# Signals
pre_save.connect(log_state_change, sender=OT, dispatch_uid="ot.log_state_change")
post_save.connect(log_create, sender=OT, dispatch_uid="ot.log_create")
post_delete.connect(on_delete_ot, sender=OT, dispatch_uid="ot.on_delete_ot")


class OTML(Contrato):

    ESTADOS = (
        ('sin_facturar', 'Sin Facturar'),     # El primer valor es el que se guarda en la DB
        ('no_pago', 'No Pago'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado')
    )

    estado = models.CharField("Estado", max_length=12, choices=ESTADOS, default='sin_facturar')
    codigo = models.CharField("Nro. OT", max_length=15, unique=True, default='00000',
                              validators=[RegexValidator(r'^\d{5}\/\d{2}$|^\d{5}$',
                                                         message="El código debe ser de la forma 00000 ó 00000/00")],
                              error_messages={'unique': "Ya existe una OT con ese número."})
    vpe = models.CharField("VPE", max_length=5, blank=True, null=True)
    vpr = models.CharField("VPR", max_length=8, blank=True, null=True)
    vpuu = models.CharField("VPUU", max_length=8, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, verbose_name="Usuario", on_delete=models.PROTECT)
    usuarioRep = models.ForeignKey(Usuario, verbose_name="Usuario Representado", on_delete=models.PROTECT,
                                   related_name='usuarioRep_set')
    checkbox_sot = models.BooleanField("SOT de otro centro", default=False)
    # Campos para la relacion inversa
    factura_set = GenericRelation("Factura")
    ot_linea_set = GenericRelation("OT_Linea", verbose_name="Líneas de OT")

    def _toState_no_pago(self):
        self.estado = 'no_pago'
        self.save()
        return True

    def _toState_sin_facturar(self):
        self.estado = 'sin_facturar'
        self.save()
        return True

    def _toState_pagado(self):
        self.estado = 'pagado'
        self.save()
        return True

    def _toState_cancelado(self, obs=''):
        if self.estado == 'finalizado':
            raise StateError('No se pueden cancelar las OT pagadas.', '')
        self.estado = 'cancelado'
        self._obs = obs
        self.save()
        ## Cancelo las facturas asociadas, de haberlas
        for factura in self.factura_set.all():
            if factura.estado != 'cancelada':
                factura.estado = 'cancelada'
                factura.save()
        return True

    def _delete(self):
        if self.estado != 'sin_facturar':
            raise StateError('Solo se pueden borrar OTs que estén sin facturar', '')
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

    def get_facturacion(self):
        count = 0
        if self.estado in ['no_pago', 'pagado']:
            for factura in self.factura_set.all():
                count += factura.importe
        return count

    class Meta:
        permissions = (("cancel_otml", "Can cancel OT-ML"),
                       ("finish_otml", "Can finish OT-ML"),
                       ("read_otml", "Can read OT-ML"))

# Signals
pre_save.connect(log_state_change, sender=OTML, dispatch_uid="otml.log_state_change")
post_save.connect(log_create, sender=OTML, dispatch_uid="otml.log_create")
post_delete.connect(on_delete_otml, sender=OTML, dispatch_uid="otml.on_delete_otml")


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


MODO_ENVIO = (
    ('correo_postal', 'Correo Postal'),  # El primer valor es el que se guarda en la DB
    ('email', 'Email'),
    ('GDE', 'GDE'),
    ('recibo', 'Recibo')
)

class SOT(Contrato):

    ESTADOS = (
        ('borrador', 'Borrador'),     # El primer valor es el que se guarda en la DB
        ('pendiente', 'Pendiente'),
        ('cobrada', 'Cobrada'),
        ('cancelada', 'Cancelada')
    )

    estado = models.CharField("Estado", max_length=12, choices=ESTADOS, default='borrador')
    codigo = models.CharField("Nro. SOT", max_length=15, unique=True, default=nextSOTCode,
                              error_messages={'unique': "Ya existe una SOT con ese número."})
    deudor = models.ForeignKey(Usuario, verbose_name="UT Deudora",
                               on_delete=models.PROTECT, related_name='sot_deudor')
    ejecutor = models.ForeignKey(Usuario, verbose_name="UT Ejecutora", default=1,
                                 on_delete=models.PROTECT, related_name='sot_ejecutor')
    usuario_final = models.ForeignKey(Usuario, verbose_name="Usuario OT", null=True, blank=True,
                                      on_delete=models.PROTECT, related_name='sot_usuario_final')
    ot = models.CharField("Nro. OT", max_length=200, blank=True, null=True)
    expediente = models.CharField("Expediente", max_length=20, blank=True, null=True)
    fecha_envio_ut = models.DateField("Fecha de Envío a la UT", blank=True, null=True)
    firmada = models.BooleanField("Retornó Firmada")
    fecha_envio_cc = models.DateField("Fecha de Envío a CC", blank=True, null=True)
    fecha_prevista = models.DateField("Fecha Prevista")
    solicitante = models.CharField("Area Solicitante", max_length=4, choices=AREAS)
    descuento_fijo = models.BooleanField("Descuento Fijo")
    # Campos para la relacion inversa
    ot_linea_set = GenericRelation("OT_Linea", verbose_name="Líneas de OT")
    modo_envio = models

    def get_area(self):
        return self.solicitante

    def _toState_pendiente(self):
        self.estado = 'pendiente'
        self.save()
        return True

    def _toState_cobrada(self, flag):
        if flag:
            # Antes de finalizar la SOT chequeo que el presupuesto pueda ser finalizado
            if self.presupuesto.estado != 'en_proceso_de_facturacion':
                raise StateError('El presupuesto debe estar en proceso de facturación antes de poder finalizarlo', '')
            self.presupuesto._toState_finalizado()
        self.estado = 'cobrada'
        self.save()
        return True

    def _toState_cancelada(self, obs=''):
        if self.estado == 'cobrada':
            raise StateError('No se pueden cancelar las SOT cobradas.', '')
        self.estado = 'cancelada'
        self._obs = obs
        self.save()
        return True

    def _delete(self):
        if self.estado != 'borrador':
            raise StateError('Solo se pueden borrar SOTs en estado Borrador', '')
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

    def get_facturacion(self):
        count = 0
        if self.estado in ['pendiente', 'cobrada']:
            count = self.importe_neto
        return count

    class Meta:
        permissions = (("cancel_sot", "Can cancel SOT"),
                       ("finish_sot", "Can finish SOT"),
                       ("read_sot", "Can read SOT"))

# Signals
pre_save.connect(toState_pendiente, sender=SOT, dispatch_uid="sot.toState_pendiente")
pre_save.connect(log_state_change, sender=SOT, dispatch_uid="sot.log_state_change")
post_save.connect(log_create, sender=SOT, dispatch_uid="sot.log_create")
post_delete.connect(on_delete_sot, sender=SOT, dispatch_uid="sot.on_delete_sot")


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

    estado = models.CharField("Estado", max_length=12, choices=ESTADOS, default='borrador')
    codigo = models.CharField("Nro. RUT", max_length=15, unique=True, default=nextRUTCode,
                              error_messages={'unique': "Ya existe una RUT con ese número."})
    deudor = models.ForeignKey(Usuario, verbose_name="UT Deudora", on_delete=models.PROTECT, related_name='rut_deudor')
    ejecutor = models.ForeignKey(Usuario, verbose_name="UT Ejecutora", default=1,
                                 on_delete=models.PROTECT, related_name='rut_ejecutor')
    solicitante = models.CharField("Area Solicitante", max_length=4, choices=AREAS)
    fecha_envio_ut = models.DateField("Fecha de Envío a la UT", blank=True, null=True)
    firmada = models.BooleanField("Retornó Firmada")
    fecha_envio_cc = models.DateField("Fecha de Envío a CC", blank=True, null=True)
    fecha_prevista = models.DateField("Fecha Prevista")
    descuento_fijo = models.BooleanField("Descuento Fijo")
   # Campos para la relacion inversa
    ot_linea_set = GenericRelation("OT_Linea", verbose_name="Líneas de OT")

    def get_area(self):
        return self.solicitante

    def _toState_pendiente(self):
        self.estado = 'pendiente'
        self.save()
        return True

    def _toState_cobrada(self, flag):
        if flag:
            # Antes de finalizar la RUT chequeo que el presupuesto pueda ser finalizado
            if self.presupuesto.estado != 'en_proceso_de_facturacion':
                raise StateError('El presupuesto debe estar en proceso de facturación antes de poder finalizarlo', '')
            self.presupuesto._toState_finalizado()
        self.estado = 'cobrada'
        self.save()
        return True

    def _toState_cancelada(self, obs=''):
        if self.estado == 'cobrada':
            raise StateError('No se pueden cancelar las RUT cobradas.', '')
        self.estado = 'cancelada'
        self._obs = obs
        self.save()
        return True

    def _delete(self):
        if self.estado != 'borrador':
            raise StateError('Solo se pueden borrar RUTs en estado Borrador', '')
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

    def get_facturacion(self):
        count = 0
        if self.estado in ['pendiente', 'cobrada']:
            count = self.importe_neto
        return count

    class Meta:
        permissions = (("cancel_rut", "Can cancel RUT"),
                       ("finish_rut", "Can finish RUT"),
                       ("read_rut", "Can read RUT"))

# Signals
pre_save.connect(toState_pendiente, sender=RUT, dispatch_uid="rut.toState_pendiente")
pre_save.connect(log_state_change, sender=RUT, dispatch_uid="rut.log_state_change")
post_save.connect(log_create, sender=RUT, dispatch_uid="rut.log_create")
post_delete.connect(on_delete_rut, sender=RUT, dispatch_uid="rut.on_delete_rut")


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


@reversion.register()
class SI(Contrato):

    ESTADOS = (
        ('borrador', 'Borrador'),     # El primer valor es el que se guarda en la DB
        ('pendiente', 'Pendiente'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    )

    estado = models.CharField("Estado", max_length=12, choices=ESTADOS, default='borrador')
    codigo = models.CharField("Nro. SI", max_length=15, unique=True, default=nextSICode,
                              error_messages={'unique': "Ya existe una SI con ese número."})
    solicitante = models.CharField("UT Solicitante", max_length=4, choices=AREAS)
    ejecutor = models.CharField("UT Ejecutora", max_length=4, choices=AREAS)
    fecha_fin_real = models.DateField("Fecha de Finalización", blank=True, null=True)
    # Campos para la relacion inversa
    tarea_linea_set = GenericRelation("Tarea_Linea")

    def __str__(self):
        return self.codigo

    def get_area(self):
        return self.ejecutor

    def get_turnos_activos(self):
        if self.estado == 'cancelado':
            return self.turno_set.order_by('-created')
        else:
            return self.turno_set.select_related().filter(estado__in=['en_espera',
                                                                      'activo',
                                                                      'finalizado'])

    def _toState_borrador(self):
        self.estado = 'borrador'
        self.save()
        return True

    def _toState_pendiente(self):
        self.estado = 'pendiente'
        self.save()
        return True

    def _toState_finalizada(self):
        # Si la SI esta asociada a un turno, se finaliza automaticamente al finalizar el turno.
        # Puede darse el caso en que tenga mas de un turno, uno se finaliza y el resto no y luego
        # se borran todos menos el finalizado. En ese caso se finaliza a mano.
        if self.turno_set.filter(estado__in=['borrador', 'activo']):
            raise StateError('La SI tiene turnos asociados. Se finalizara automaticamente al finalizar dichos turnos.', '')
        self.estado = 'finalizada'
        self.fecha_fin_real = datetime.now().date()
        self.save()
        return True

    def _toState_cancelada(self, obs=''):
        if self.estado == 'finalizada':
            raise StateError('No se pueden cancelar las SI finalizadas.', '')
        # Cancelo los turnos asociados
        for turno in self.turno_set.all():
            turno._toState_cancelado("Registro automático: SI cancelada")
        self.estado = 'cancelada'
        self._obs = obs
        self.save()
        return True

    def _delete(self):
        if self.estado != 'borrador':
            raise StateError('Solo se pueden borrar SIs en estado Borrador', '')
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
                       ("finish_si", "Can finish SOT"),
                       ("read_si", "Can read SI"))

# Signals
pre_save.connect(log_state_change, sender=SI, dispatch_uid="si.log_state_change")
post_save.connect(log_create, sender=SI, dispatch_uid="si.post_save")
post_delete.connect(on_delete_si, sender=SI, dispatch_uid="si.on_delete_si")


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

    ofertatec = models.ForeignKey(OfertaTec, verbose_name="Oferta Tecnológica")
    codigo = models.CharField("Código", validators=[RegexValidator(r'^\d{14}$')], max_length=14)
    precio = models.FloatField("Precio Unitario")
    precio_total = models.FloatField("Precio Total")
    cantidad = models.PositiveIntegerField("Cantidad", default=1)
    cant_horas = models.PositiveIntegerField("Horas", blank=True, null=True)
    observaciones = models.TextField("Observaciones", max_length=100, blank=True)
    detalle = models.CharField("Detalle", max_length=350, blank=True, null=True)
    tipo_servicio = models.CharField("Tipo de Servicio", max_length=20, blank=True, null=True)
    # Campos para relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ['id']


class Factura(TimeStampedModel, AuthStampedModel):

    ESTADOS = (
        ('activa', 'Activa'),     # El primer valor es el que se guarda en la DB
        ('cancelada', 'Cancelada')
    )

    estado = models.CharField("Estado", max_length=12, choices=ESTADOS, default='activa')
    numero = models.CharField("Nro. Factura", max_length=15)
    fecha = models.DateField("Fecha", blank=False, null=True)
    importe = models.FloatField("Importe", blank=True, null=True, default=0)
    fecha_aviso = models.DateField("Aviso de Trabajo Realizado", blank=True, null=True)
    # Campos para relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

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

    comprobante_cobro = models.CharField("Comprobante de Cobro", max_length=20, choices=CHOICES)
    numero = models.CharField("Número", max_length=15)
    fecha = models.DateField("Fecha", blank=False, null=True)
    importe = models.FloatField("Importe", blank=True, null=True, default=0)
    factura = models.ForeignKey(Factura, verbose_name="Factura", on_delete=models.CASCADE)
    observaciones = models.TextField("Observaciones", max_length=500, blank=True, null=True)

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

    numero = models.CharField("Número", max_length=15)
    fecha = models.DateField("Fecha", blank=False, null=True)
    informe = models.BooleanField(default=False)         # Indica que el remito se realizo por un informe
    instrumento = models.BooleanField(default=False)     # Indica que el remito se realizo por un instrumento
    # Campos para relacion generica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ['id']


#class ReciboIngreso(TimeStampedModel, AuthStampedModel):
#
#    instrumento = models.BooleanField(default=False)
#    muestra = models.BooleanField(default=False)
#    cantidad = models.PositiveIntegerField("Cantidad")
#    descripcion = models.CharField("Descripción", max_length=250)
#    fecha = models.DateField("Fecha de Ingreso")
