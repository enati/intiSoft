# -*- coding: utf-8 -*-


def check_state(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        if instance.old_fecha_aceptado != instance.fecha_aceptado:
            if instance.fecha_aceptado:
                instance.estado = 'aceptado'
                turno = instance.get_turno_activo()
                if turno:
                    turno.estado = 'activo'
                    turno.save()
            else:
                instance.estado = 'borrador'
                turno = instance.get_turno_activo()
                if turno:
                    turno.estado = 'en_espera'
                    turno.save()


def remember_fecha_aceptado(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        instance.old_fecha_aceptado = instance.fecha_aceptado
    else:
        instance.old_fecha_aceptado = None


