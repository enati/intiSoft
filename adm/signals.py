# -*- coding: utf-8 -*-
from activity_log.models import ActivityLog
from datetime import datetime
from django.contrib.contenttypes.models import ContentType

def check_state(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        old_status = instance.estado
        if instance.old_fecha_aceptado != instance.fecha_aceptado:
            if instance.fecha_aceptado:
                instance.estado = 'aceptado'
                turnoList = instance.get_turnos_activos()
                for turno in turnoList:
                    turno._toState_activo()
                #Escribo el log de actividades
                instance.write_activity_log("Cambio de estado: %s -> %s" % (old_status, instance.estado))
            else:
                instance.estado = 'borrador'
                turnoList = instance.get_turnos_activos()
                for turno in turnoList:
                    turno._toState_en_espera()
                #Escribo el log de actividades
                instance.write_activity_log("Cambio de estado: %s -> %s" % (old_status, instance.estado))


def remember_fecha_aceptado(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        instance.old_fecha_aceptado = instance.fecha_aceptado
    else:
        instance.old_fecha_aceptado = None


def toState_pendiente(sender, **kwargs):
    instance = kwargs.get('instance')
    old_state = instance.estado
    if instance.pk:
        if instance.fecha_envio_ut and instance.estado == 'borrador':
            instance.estado = 'pendiente'
            instance.write_activity_log("Cambio de estado: %s -> %s" % (old_state, instance.estado))
