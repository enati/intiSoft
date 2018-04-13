# -*- coding: utf-8 -*-


# post_save
def log_create(sender, instance, created, **kwargs):
    if created:
        instance.write_activity_log("Turno #%d creado" % instance.id)


# pre_save
def log_state_change(sender, instance, **kwargs):
    if instance.pk:
        estado_orig = sender.objects.get(pk=instance.pk).estado
        if estado_orig != instance.estado:
            try:
                if instance._obs:
                    instance.write_activity_log("Cambio de estado: %s -> %s" % (estado_orig, instance.estado), instance._obs)
                else:
                    instance.write_activity_log("Cambio de estado: %s -> %s" % (estado_orig, instance.estado))
            except:
                instance.write_activity_log("Cambio de estado: %s -> %s" % (estado_orig, instance.estado))


# post_delete
def log_delete(sender, instance, **kwargs):
    instance.write_activity_log("Turno #%d eliminado" % instance.id)


# pre_save
def check_state(sender, instance, **kwargs):
    if instance.pk:
        if instance.si and instance.estado == 'en_espera':
            instance.estado = 'activo'
            if instance.si.estado == 'borrador':
                instance.si._toState_pendiente()