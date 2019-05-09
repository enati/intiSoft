# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from adm.models import Presupuesto, Usuario, OfertaTec, SI, OfertaTec_Descripcion
from django_extensions.db.models import TimeStampedModel
from audit_log.models import AuthStampedModel
from django_permanent.models import PermanentModel
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from django.db.models.signals import pre_save, post_save, m2m_changed, post_init, post_delete
from django.dispatch import receiver
from lab.signals import *
from intiSoft.exception import StateError
import reversion
from django.contrib.contenttypes.models import ContentType
from activity_log.models import ActivityLog

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


@reversion.register(follow=["ofertatec_linea_set", "presupuesto", "si"])
class Turno(TimeStampedModel, AuthStampedModel, PermanentModel):

    #_fecha_inicio_orig = None
    #_presupuesto_orig = None
    ESTADOS = (
        ('en_espera', 'En Espera'),
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
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
        ('TICS', 'TICS'),
        ('DES', 'DES'),
        ('CAL', 'CAL'),
        ('MEC', 'MEC'),
        ('ML', 'ML'),
    )

    estado = models.CharField(max_length=10, choices=ESTADOS,
                              default='en_espera')
    presupuesto = models.ForeignKey(Presupuesto,
                                  #limit_choices_to=dict(estado__in=['borrador',
                                  #                                'aceptado']),
                                                         blank=True,
                                                         null=True)
    si = models.ForeignKey(SI, blank=True, null=True)
    fecha_inicio = models.DateField('Inicio estimado', blank=True, null=True)
    fecha_fin = models.DateField('Finalizacion estimada', blank=True, null=True)
    fecha_fin_real = models.DateField('Finalizacion', blank=True, null=True)
    nro_revision = models.IntegerField(default=0)
    revisionar = models.BooleanField(default=False)
    area = models.CharField(max_length=10, choices=AREAS)

    def write_activity_log(self, activity, comments="Registro automático"):
        content_type_obj = ContentType.objects.get(model="turno")
        ActivityLog.objects.create(content_type=content_type_obj,
                                   object_id=self.pk,
                                   activity=activity,
                                   comments=comments)

    def _revisionar(self):
        """ Chequeo si es necesario hacer una revision del turno. Solo se revisionan
            los turnos en_espera o activos tales que:
                * El instrumento haya llegado pasados 2 dias habiles a la fecha de inicio.
                * El instrumento no haya llegado pasados 2 dias habiles a la fecha de inicio (a menos que sea in situ).
                * Haya pasado la fecha de finalizacion y el turno siga en estado en espera/activo.
                * El turno no este asociado a una SI
        """
        try:
            hoy = datetime.now().date()
            fecha_limite = sumarDiasHabiles(self.fecha_inicio, 2)
            if self.presupuesto:
                if self.presupuesto.instrumento_set.all():
                    if self.presupuesto.instrumento_set.last().fecha_instrumento > fecha_limite:
                        # El instrumento llego pasados 2 dias habiles a la fecha de inicio
                        return True
                elif (hoy > fecha_limite):
                    # El instrumento no llego pasados 2 dias habiles a la fecha de inicio
                    # y no es in_situ ni asistencia
                    if (self.presupuesto.tipo not in ('in_situ', 'asistencia')):
                        return True
            return False
        except:
            return False

    def alertar(self):
        """ Chequeo si es necesario generar una alerta por fecha proxima de inicio y presupuesto
            no aceptado o instrumento faltante
        """
        pasado_manana = sumarDiasHabiles(datetime.now().date(), 2)
        try:
            if self.estado in ['en_espera', 'activo']:
                if self.presupuesto and\
                    (not (self.presupuesto.instrumento_set.last().fecha_instrumento and self.presupuesto.fecha_aceptado)
                    and pasado_manana >= self.fecha_inicio)\
                    and (self.presupuesto.tipo not in ('in_situ', 'asistencia')):
                        return True
            return False
        except:
            return False

    def _toState_activo(self):
        self.estado = 'activo'
        self.save()
        return True

    def _toState_en_espera(self):
        self.estado = 'en_espera'
        self.save()
        return True

    def _toState_finalizado(self):
        """Faltarian las validaciones"""
        if self.estado != 'activo':
            raise StateError('El turno debe estar activo antes de poder finalizarlo.', '')
        self.estado = 'finalizado'
        self.fecha_fin_real = datetime.now().date()
        self.save()
        # Cambio de estado el presupuesto o la si asociado, segun corresponda.
        if self.presupuesto:
            # Si todava quedan turnos pendientes no cambio de estado el presupuesto
            turnos_pendientes = Turno.objects.filter(presupuesto_id=self.presupuesto.id, estado__in=['en_espera', 'activo'])
            if not turnos_pendientes:
                self.presupuesto._toState_en_proceso_de_facturacion()
        elif self.si:
            # Si todavia quedan turnos pendientes no finalizo la SI
            turnos_pendientes = Turno.objects.filter(si_id=self.si.id, estado__in=['en_espera', 'activo'])
            if not turnos_pendientes:
                self.si._toState_finalizada()
        return True

    def _toState_cancelado(self, obs=''):
        """
        Si el turno esta asociado a una SI, la SI esta en estado Pendiente.
        Luego, si el turno que se quiere cancelar es el unico turno activo de la SI,
        hay que volverla a estado Borrador.
        """
        self.estado = 'cancelado'
        self._obs = obs
        self.save()
        if self.si:
            turnosAsociados = self.si.get_turnos_activos()
            if not turnosAsociados:
                self.si._toState_borrador()
        return True

    def _delete(self):
        """Faltarian las validaciones"""
        if self.estado != 'en_espera':
            raise StateError('Solo se pueden borrar turnos que esten en espera', '')
        # Si tiene un presupuesto asociado en estado en proceso de facturacion,
        # finalizado o cancelado, no lo elimino. Lo mismo con SI.
        if self.presupuesto and self.presupuesto.estado in ['en_proceso_de_facturacion', 'finalizado', 'cancelado']:
            raise StateError('El turno no se puede borrar ya que esta asociado a un presupuesto que no se encuentra en estado Borrador', '')
        elif self.si and self.si.estado in ['finalizada', 'cancelada']:
            raise StateError('El turno no se puede borrar ya que esta asociado a una SI que se encuentra finalizada/cancelada', '')
        else:
            self.delete()
            return True

    class Meta:
        permissions = (("finish_turno", "Can finish turno"),
                       ("cancel_turno", "Can cancel turno"),
                       ("add_turno_LIM1", "Can add turno LIM1"),
                       ("add_turno_LIM2", "Can add turno LIM2"),
                       ("add_turno_LIM3", "Can add turno LIM3"),
                       ("add_turno_LIM4", "Can add turno LIM4"),
                       ("add_turno_LIM5", "Can add turno LIM5"),
                       ("add_turno_LIM6", "Can add turno LIM6"),
                       ("add_turno_LIA", "Can add turno LIA"),
                       ("add_turno_EXT", "Can add turno EXT"),
                       ("add_turno_TICS", "Can add turno TICS"),
                       ("add_turno_DES", "Can add turno DES"),
                       ("add_turno_CAL", "Can add turno CAL"),
                       ("add_turno_MEC", "Can add turno MEC"),
                       ("add_turno_ML", "Can add turno ML"),
                       ("change_turno_LIM1", "Can change turno LIM1"),
                       ("change_turno_LIM2", "Can change turno LIM2"),
                       ("change_turno_LIM3", "Can change turno LIM3"),
                       ("change_turno_LIM4", "Can change turno LIM4"),
                       ("change_turno_LIM5", "Can change turno LIM5"),
                       ("change_turno_LIM6", "Can change turno LIM6"),
                       ("change_turno_LIA", "Can change turno LIA"),
                       ("change_turno_EXT", "Can change turno EXT"),
                       ("change_turno_TICS", "Can change turno TICS"),
                       ("change_turno_DES", "Can change turno DES"),
                       ("change_turno_CAL", "Can change turno CAL"),
                       ("change_turno_MEC", "Can change turno MEC"),
                       ("change_turno_ML", "Can change turno ML"),
                       ("delete_turno_LIM1", "Can delete turno LIM1"),
                       ("delete_turno_LIM2", "Can delete turno LIM2"),
                       ("delete_turno_LIM3", "Can delete turno LIM3"),
                       ("delete_turno_LIM4", "Can delete turno LIM4"),
                       ("delete_turno_LIM5", "Can delete turno LIM5"),
                       ("delete_turno_LIM6", "Can delete turno LIM6"),
                       ("delete_turno_LIA", "Can delete turno LIA"),
                       ("delete_turno_EXT", "Can delete turno EXT"),
                       ("delete_turno_TICS", "Can delete turno TICS"),
                       ("delete_turno_DES", "Can delete turno DES"),
                       ("delete_turno_CAL", "Can delete turno CAL"),
                       ("delete_turno_MEC", "Can delete turno MEC"),
                       ("delete_turno_ML", "Can delete turno ML"),
                       ("finish_turno_LIM1", "Can finish turno LIM1"),
                       ("finish_turno_LIM2", "Can finish turno LIM2"),
                       ("finish_turno_LIM3", "Can finish turno LIM3"),
                       ("finish_turno_LIM4", "Can finish turno LIM4"),
                       ("finish_turno_LIM5", "Can finish turno LIM5"),
                       ("finish_turno_LIM6", "Can finish turno LIM6"),
                       ("finish_turno_LIA", "Can finish turno LIA"),
                       ("finish_turno_EXT", "Can finish turno EXT"),
                       ("finish_turno_TICS", "Can finish turno TICS"),
                       ("finish_turno_DES", "Can finish turno DES"),
                       ("finish_turno_CAL", "Can finish turno CAL"),
                       ("finish_turno_MEC", "Can finish turno MEC"),
                       ("finish_turno_ML", "Can finish turno ML"),
                       ("cancel_turno_LIM1", "Can cancel turno LIM1"),
                       ("cancel_turno_LIM2", "Can cancel turno LIM2"),
                       ("cancel_turno_LIM3", "Can cancel turno LIM3"),
                       ("cancel_turno_LIM4", "Can cancel turno LIM4"),
                       ("cancel_turno_LIM5", "Can cancel turno LIM5"),
                       ("cancel_turno_LIM6", "Can cancel turno LIM6"),
                       ("cancel_turno_LIA", "Can cancel turno LIA"),
                       ("cancel_turno_EXT", "Can cancel turno EXT"),
                       ("cancel_turno_TICS", "Can cancel turno TICS"),
                       ("cancel_turno_DES", "Can cancel turno DES"),
                       ("cancel_turno_CAL", "Can cancel turno CAL"),
                       ("cancel_turno_MEC", "Can cancel turno MEC"),
                       ("cancel_turno_ML", "Can cancel turno ML"),
                       )

# Signals
pre_save.connect(check_state, sender=Turno, dispatch_uid="turno.check_state")
pre_save.connect(log_state_change, sender=Turno, dispatch_uid="turno.log_state_change")
post_save.connect(log_create, sender=Turno, dispatch_uid="turno.log_create")
post_delete.connect(log_delete, sender=Turno, dispatch_uid="turno.log_delete")


@reversion.register(follow=["ofertatec", "ofertatec_old"])
class OfertaTec_Linea(TimeStampedModel, AuthStampedModel):
    """ Lineas de Oferta Tecnologica del Presupuesto """

    ofertatec = models.ForeignKey(OfertaTec, verbose_name='OfertaTec')
    # Oferta tecnologica vieja del centro, para llevar un control ya que la oferta nueva
    # es demasiado generica.
    ofertatec_old = models.ForeignKey(OfertaTec_Descripcion, verbose_name='OfertaTec Centro', blank=True, null=True)
    codigo = models.CharField(validators=[RegexValidator(r'^\d{14}$')],
                              max_length=14, verbose_name='Codigo')
    precio = models.FloatField(verbose_name='Precio')
    precio_total = models.FloatField(verbose_name='Precio Total')
    cantidad = models.IntegerField(verbose_name='Cantidad', default=1)
    cant_horas = models.FloatField(verbose_name='Horas', blank=True, null=True)
    turno = models.ForeignKey(Turno, verbose_name='Turno')
    observaciones = models.TextField(max_length=100, blank=True)
    detalle = models.CharField(max_length=350, verbose_name='Detalle', blank=True, null=True)
    tipo_servicio = models.CharField(max_length=20, verbose_name='Tipo de Servicio', blank=True, null=True)

    class Meta:
        ordering = ['id']


