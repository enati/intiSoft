# -*- coding: utf-8 -*-


def pre_save_presup(sender, instance, **kwargs):
    if instance.pk:
        # Traigo los datos no modificados de la DB
        obj_old_presup = sender.objects.get(pk=instance.pk)
        instance._old_fecha_instr = obj_old_presup.fecha_instrumento
        instance._old_fecha_realizado = obj_old_presup.fecha_realizado
    else:
        instance._old_fecha_instr = None
        instance._old_fecha_realizado = None


def chequear_revisionado(sender, instance, **kwargs):
    if instance.fecha_realizado != instance._old_fecha_realizado:
        # Si el presup debía ser revisionado y se modifico la fecha de realizado, aumento el nro de revision
        if instance.revisionar:
            instance.nro_revision += 1
            instance.revisionar = False
            instance.fecha_aceptado = None
            instance.estado = 'borrador'
            instance.save()
            # Vuelvo el turno a estado 'en_espera'
            turno = instance.get_turno_activo()
            if turno:
                turno.estado = 'en_espera'
                turno.save()
    #if instance.fecha_instrumento != instance._old_fecha_instr:
        ## Chequeo si hay que revisionar el turno o no
            #turno = instance.get_turno_activo()
            #if turno and turno._revisionar():
                #turno.nro_revision += 1
                #turno.revisionar = True
                #turno.save()