# -*- coding: utf-8 -*-


def check_state(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        if instance.old_fecha_aceptado != instance.fecha_aceptado:
            if instance.fecha_aceptado:
                instance.estado = 'aceptado'
                turnoList = instance.get_turnos_activos()
                for turno in turnoList:
                    turno.estado = 'activo'
                    turno.save()
            else:
                instance.estado = 'borrador'
                turnoList = instance.get_turnos_activos()
                for turno in turnoList:
                    turno.estado = 'en_espera'
                    turno.save()


def remember_fecha_aceptado(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        instance.old_fecha_aceptado = instance.fecha_aceptado
    else:
        instance.old_fecha_aceptado = None


def toState_pendiente(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        if instance.fecha_envio_ut and instance.estado == 'borrador':
            instance.estado = 'pendiente'
