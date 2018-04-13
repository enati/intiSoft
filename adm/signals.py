# -*- coding: utf-8 -*-
from activity_log.models import ActivityLog
from datetime import datetime
from django.contrib.contenttypes.models import ContentType

# Comentario: los post_save se llaman 2 veces en la creacion de objetos:
#             en __init__ y en save(). Las llamadas se diferencian
#             con la flag 'created'

CREATION_MSG = {
    "Presupuesto": "Presupuesto #%s creado",
    "OT": "OT #%s creada",
    "OTML": "OTML #%s creada",
    "SOT": "SOT #%s creada",
    "RUT": "RUT #%s creada",
    "SI": "SI #%s creada"
}

# =============================================
# ============== GENERAL SIGNALS ==============
# =============================================


# post_save
def log_create(sender, instance, created, **kwargs):
    if created:
        instance.write_activity_log(CREATION_MSG[sender.__name__] % instance.codigo)


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


# =============================================
# ============ PRESUPUESTO SIGNALS ============
# =============================================

# pre_save
def check_state(sender, instance, **kwargs):
    if instance.pk:
        if instance.fecha_aceptado and instance.estado == 'borrador':
            instance.estado = 'aceptado'
            turnoList = instance.get_turnos_activos()
            for turno in turnoList:
                turno._toState_activo()
        elif not instance.fecha_aceptado and instance.estado == 'aceptado':
            instance.estado = 'borrador'
            turnoList = instance.get_turnos_activos()
            for turno in turnoList:
                turno._toState_en_espera()


# post_delete
def on_delete_presupuesto(sender, instance, **kwargs):
    instance.write_activity_log("Presupuesto #%s eliminado" % instance.codigo[1:])

# ============================================
# ================ OT SIGNALS ================
# ============================================


# post_delete
def on_delete_ot(sender, instance, **kwargs):
    instance.write_activity_log("OT #%s eliminada" % instance.codigo[1:])

# ==============================================
# ================ OTML SIGNALS ================
# ==============================================


# post_delete
def on_delete_otml(sender, instance, **kwargs):
    instance.write_activity_log("OTML #%s eliminada" % instance.codigo[1:])

# =============================================
# ================ SOT SIGNALS ================
# =============================================


# post_delete
def on_delete_sot(sender, instance, **kwargs):
    instance.write_activity_log("SOT #%s eliminada" % instance.codigo[1:])

# =============================================
# ================ RUT SIGNALS ================
# =============================================


# pre_save
def toState_pendiente(sender, instance, **kwargs):
    if instance.pk:
        if instance.fecha_envio_ut and instance.estado == 'borrador':
            instance.estado = 'pendiente'


# post_delete
def on_delete_rut(sender, instance, **kwargs):
    instance.write_activity_log("RUT #%s eliminada" % instance.codigo[1:])

# ============================================
# ================ SI SIGNALS ================
# ============================================


# post_delete
def on_delete_si(sender, instance, **kwargs):
    instance.write_activity_log("SI #%s eliminada" % instance.codigo[1:])



