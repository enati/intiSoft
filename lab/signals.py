# -*- coding: utf-8 -*-
from adm.models import Presupuesto

#def actualizar_lineas(sender, instance, action, reverse, model, pk_set, **kwargs):
    #if instance.presupuesto is not None:
        #obj_presup = instance.presupuesto
        #obj_old_presup = instance._old_presup
        #if action == 'post_clear':
            ## Borro todas las lineas del presupuesto
            #OfertaTec_Linea.objects.filter(presupuesto=obj_old_presup.id).delete()
        #if action == 'post_add':
            ## Por cada nueva oferta tecnologica, creo una linea en el presupuesto
            #m2o_ids = set([x.ofertatec.id for x in obj_presup.ofertatec_linea_set.all()])
            ## Chequeo los m2o agregados
            #for val in pk_set.difference(m2o_ids):
                #obj_ofertatec = OfertaTec.objects.get(pk=val)
                #obj_presup.ofertatec_linea_set.create(ofertatec=obj_ofertatec,
                                                  #precio=obj_ofertatec.precio)
            ## Chequeo los m2o eliminados
            #for val in m2o_ids.difference(pk_set):
                #obj_ofertatec = OfertaTec.objects.get(pk=val)
                #OfertaTec_Linea.objects.filter(presupuesto=obj_presup.id,
                                               #ofertatec=val).delete()


def pre_save_turno(sender, instance, **kwargs):
    if instance.pk:
        # Traigo los datos no modificados de la DB
        obj_old_turno = sender.objects.get(pk=instance.pk)
        #instance._old_m2m = set(list(obj_old_turno.ofertatec.all()))
        instance._old_presup = obj_old_turno.presupuesto
        instance._old_fecha_inicio = obj_old_turno.fecha_inicio
    else:
        #instance._old_m2m = set(list())
        instance._old_presup = None
        instance._old_fecha_inicio = None


def chequear_revisionado(sender, instance, **kwargs):
    if instance.fecha_inicio != instance._old_fecha_inicio:
        # Si el turno debía ser revisionado y se modifico la fecha de inicio, aumento el nro de revision
        if instance.revisionar:
            instance.nro_revision += 1
            instance.revisionar = False
            instance.save()
            presup_obj = Presupuesto.objects.get(turno=instance.id)
            presup_obj.revisionar = True
            presup_obj.save()
