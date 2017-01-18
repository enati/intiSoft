from django.db import models
from django.core.urlresolvers import reverse
from adm.models import Presupuesto, Usuario, OfertaTec, SI
from django_extensions.db.models import TimeStampedModel
from audit_log.models import AuthStampedModel
from django_permanent.models import PermanentModel
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from lab.signals import *
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
        ('SIS', 'SIS'),
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

    def _revisionar(self):
        """ Chequeo si es necesario hacer una revision del turno. Solo se revisionan
            los turnos en_espera o activos tales que:
                * El instrumento haya llegado pasados 2 dias habiles a la fecha de inicio.
                * El instrumento no haya llegado pasados 2 dias habiles a la fecha de inicio (a menos que sea in situ).
                * Haya pasado la fecha de finalizacion y el turno siga en estado en espera/activo.
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
                    if not (self.presupuesto.in_situ or self.presupuesto.asistencia):
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
                    and not (self.presupuesto.in_situ)\
                    and not (self.presupuesto.asistencia):
                        return True
            return False
        except:
            return False

    def _toState_finalizado(self):
        """Faltarian las validaciones"""
        if self.estado != 'activo':
            raise StateError('El turno debe estar activo antes de poder finalizarlo.', '')
        self.estado = 'finalizado'
        self.fecha_fin_real = datetime.now().date()
        self.save()
        # Cambio de estado el presupuesto o la si asociado, segun corresponda.
        if self.presupuesto:
            self.presupuesto.estado = 'en_proceso_de_facturacion'
            self.presupuesto.save()
        elif self.si:
            # Si todavia quedan turnos pendientes no finalizo la SI
            turnos_pendientes = Turno.objects.filter(si_id=self.si.id, estado__in=['en_espera', 'activo'])
            if not turnos_pendientes:
                self.si.estado = 'finalizada'
                self.si.save()
        return True

    def _toState_cancelado(self):
        """Faltarian las validaciones"""
        self.estado = 'cancelado'
        self.save()
        return True

    def _delete(self):
        """Faltarian las validaciones"""
        # Si tiene un presupuesto asociado en estado en proceso de facturacion,
        # finalizado o cancelado, no lo elimino. Lo mismo con SI.
        if self.presupuesto and self.presupuesto.estado in ['en_proceso_de_facturacion', 'finalizado', 'cancelado']:
            return False
        elif self.si and self.si.estado in ['finalizada', 'cancelada']:
            return False
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
                       ("add_turno_SIS", "Can add turno SIS"),
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
                       ("change_turno_SIS", "Can change turno SIS"),
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
                       ("delete_turno_SIS", "Can delete turno SIS"),
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
                       ("finish_turno_SIS", "Can finish turno SIS"),
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
                       ("cancel_turno_SIS", "Can cancel turno SIS"),
                       ("cancel_turno_DES", "Can cancel turno DES"),
                       ("cancel_turno_CAL", "Can cancel turno CAL"),
                       ("cancel_turno_MEC", "Can cancel turno MEC"),
                       ("cancel_turno_ML", "Can cancel turno ML"),
                       )

# Signals
pre_save.connect(check_state, sender=Turno)


@reversion.register(follow=["ofertatec"])
class OfertaTec_Linea(TimeStampedModel, AuthStampedModel):
    """ Lineas de Oferta Tecnologica del Presupuesto """

    ofertatec = models.ForeignKey(OfertaTec, verbose_name='OfertaTec')
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


