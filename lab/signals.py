# -*- coding: utf-8 -*-


def check_state(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        old_state = instance.estado
        if instance.si and instance.estado == 'en_espera':
            instance.estado = 'activo'
            if instance.si.estado == 'borrador':
                instance.si.estado = 'pendiente'
                instance.si.save()
            instance.write_activity_log("Cambio de estado: %s -> %s" % (old_state, instance.estado))
    return True