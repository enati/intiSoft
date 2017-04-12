# -*- coding: utf-8 -*-


def check_state(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:
        if instance.si and instance.estado == 'en_espera':
            instance.estado = 'activo'
    return True