# -*- coding: utf-8 -*-
from django.db import models
from django_extensions.db.models import TimeStampedModel
from audit_log.models import AuthStampedModel
from adm.signals import *
from django.db.models.signals import post_init, pre_save
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from django.db import connection
from intiSoft.exception import StateError
import reversion

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
class OfertaTec(TimeStampedModel, AuthStampedModel):

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
class Presupuesto(TimeStampedModel, AuthStampedModel):

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
            turno = self.turno_set.all().filter(estado__in=['en_espera',
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
        if self.estado != 'en_proceso_de_facturacion':
            raise StateError('El presupuesto debe estar en proceso de facturación antes de poder finalizarlo', '')
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
        """Faltarian las validaciones"""
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


def nextOTCode():
    cursor = connection.cursor()
    cursor.execute("""SELECT (t1.codigo + 1)
                     FROM adm_ot t1
                     WHERE NOT EXISTS
                        (SELECT t2.codigo FROM adm_ot t2 WHERE t2.codigo = t1.codigo + 1)
                     """)
    row = cursor.fetchone()
    if row:
        n = str(int(row[0]))
        zeros = '0' * (5 - len(n))
        return zeros + n
    else:
        return '00001'


class OT(TimeStampedModel, AuthStampedModel):

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
    fecha_realizado = models.DateField(verbose_name='Fecha',
                                       blank=False, null=True)
    importe = models.FloatField(verbose_name='Importe', blank=False, null=True, default=0)
    presupuesto = models.ForeignKey(Presupuesto, verbose_name='Presupuesto',
                                    on_delete=models.PROTECT)
    fecha_aviso = models.DateField(verbose_name='Aviso de Trabajo Realizado',
                                       blank=True, null=True)

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
        # Finalizo el presupuesto asociado
        self.presupuesto.estado = 'finalizado'
        self.presupuesto.save()
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
        """Faltarian las validaciones"""
        self.delete()
        return True

    class Meta:
        permissions = (("cancel_ot", "Can cancel OT"),
                       ("finish_ot", "Can finish OT"),)


class OT_Linea(TimeStampedModel, AuthStampedModel):
    """ Lineas de Oferta Tecnologica de la OT """

    ofertatec = models.ForeignKey(OfertaTec, verbose_name='OfertaTec')
    precio = models.FloatField(verbose_name='Precio')
    precio_total = models.FloatField(verbose_name='Precio Total')
    cantidad = models.IntegerField(verbose_name='Cantidad', default=1)
    cant_horas = models.FloatField(verbose_name='Horas', blank=True, null=True)
    ot = models.ForeignKey(OT, verbose_name='OT')
    observaciones = models.TextField(max_length=100, blank=True)
    detalle = models.CharField(max_length=350, verbose_name='Detalle', blank=True, null=True)
    tipo_servicio = models.CharField(max_length=20, verbose_name='Tipo de Servicio', blank=True, null=True)

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
    ot = models.ForeignKey(OT, verbose_name='OT', on_delete=models.CASCADE)

    def _toState_cancelado(self):
        if self.estado == 'activa':
            self.estado = 'cancelada'
            self.save()
            ot_obj = OT.objects.get(pk=self.ot_id)
            if not(ot_obj.factura_set.exclude(estado__in=['cancelada'])) and ot_obj.estado != 'cancelado':
                ot_obj._toState_sin_facturar()
        return True

    def save(self, *args, **kwargs):
        if not self.pk:
            #This code only happens if the objects is
            #not in the database yet. Otherwise it would
            #have pk
            ot_obj = OT.objects.get(pk=self.ot_id)
            if ot_obj.estado == 'sin_facturar':
                ot_obj._toState_no_pago()
        super(Factura, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        res = super(Factura, self).delete(*args, **kwargs)
        # Si borre la ultima factura asociada a una OT,
        # vuelvo la OT a estado sin_facturar
        ot_obj = OT.objects.get(pk=self.ot_id)
        if not(ot_obj.factura_set.exclude(estado__in=['cancelada'])):
            ot_obj._toState_sin_facturar()
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
    factura = models.ForeignKey(Factura, verbose_name='Factura', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


