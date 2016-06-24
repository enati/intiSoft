# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Presupuesto, OfertaTec, Usuario
from lab.models import OfertaTec_Linea
from .forms import PresupuestoForm, OfertaTecForm, UsuarioForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from .utils import genWord
from django.http import JsonResponse
import json
from intiSoft.exception import StateError
from reversion.models import Version
import reversion

#===========================================
#======== FUNCIONES AUXILIARES =============
#===========================================


def plus_five(orig_date):
    try:
        date = (orig_date + timedelta(days=7)).strftime('%d/%m/%Y')
    except:
        date = orig_date
    return date


def less_five(orig_date):
    try:
        date = (orig_date - timedelta(days=7)).strftime('%d/%m/%Y')
    except:
        date = orig_date
    return date

#===========================================
#======= FUNCIONES ROUTEABLES ==============
#===========================================


def viewWord(request, *args, **kwargs):
    presup_id = kwargs.get('pk')
    presup_obj = Presupuesto.objects.get(id=presup_id)
    vals = {}
    turno_activo = presup_obj.get_turno_activo()
    vals['area'] = turno_activo.area if turno_activo else ''
    vals['codigo'] = presup_obj.codigo + '-R' + str(presup_obj.nro_revision)
    vals['fecha'] = presup_obj.fecha_realizado.strftime('%d/%m/%Y') \
                    if presup_obj.fecha_realizado else ''
    vals['email'] = presup_obj.usuario.mail
    vals['solicitante'] = presup_obj.usuario.nombre
    vals['contacto'] = presup_obj.usuario.nombre
    vals['ofertatec'] = []
    vals['fecha_inicio'] = less_five(turno_activo.fecha_inicio) if turno_activo else ''
    vals['fecha_fin'] = plus_five(turno_activo.fecha_fin) if turno_activo else ''
    vals['plantilla'] = ''

    if presup_obj.asistencia:
        vals['plantilla'] = 'Presupuesto Asistencia.docx'
    elif presup_obj.calibracion:
        vals['plantilla'] = 'Presupuesto Calibracion.docx'
    elif presup_obj.in_situ:
        vals['plantilla'] = 'Presupuesto In Situ.docx'
    elif presup_obj.lia:
        vals['plantilla'] = 'Presupuesto LIA.docx'

    if turno_activo:
        for o in turno_activo.ofertatec_linea_set.get_queryset():
            vals['ofertatec'].append((o.ofertatec.codigo, o.ofertatec.detalle, o.precio))
        #vals['ofertatec'] += turno_activo.ofertatec.codigo if turno_activo else ''
        #vals['detalle'] = turno_activo.ofertatec.detalle if turno_activo else ''
        #vals['precio'] = str(turno_activo.ofertatec.precio) if turno_activo else ''
    # Create the HttpResponse object with the appropriate headers.
    #response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    # Create the Word object
    return genWord(vals)


def get_user(request, *args, **kwargs):
    try:
        user_id = request.GET['user_id']
        user_obj = Usuario.objects.get(pk=user_id)
        data = {'nro_usuario': user_obj.nro_usuario,
                'cuit': user_obj.cuit,
                'rubro': user_obj.rubro,
                }
    except:
        data = {}
    return HttpResponse(json.dumps(data), content_type="text/json")


def createRevision(request, *args, **kwargs):
    try:
        # Declare a revision block.
        with reversion.create_revision():

            # Save a new model instance.
            obj_pk = kwargs.get('pk')
            obj = Presupuesto.objects.get(pk=obj_pk)
            obj.save()

            presupVers = Version.objects.get_for_object(obj)
            actualRevNumber = 'REV0'
            if presupVers:
                ultRev = presupVers.first()
                numUltRev = int(ultRev.revision.comment.split('REV')[1])
                actualRevNumber = 'REV' + str(numUltRev + 1)

            # Store some meta-information.
            reversion.set_user(request.user)
            reversion.set_comment(actualRevNumber)
        # Actualizo el presupuesto
        obj.nro_revision += 1
        obj.revisionar = False
        obj.save()
        return JsonResponse({'ok': 'ok'})
    except:
        return JsonResponse({'err': 'err'})


def rollBackRevision(request, *args, **kwargs):
    obj_pk = kwargs.get('pk')
    obj = Presupuesto.objects.get(pk=obj_pk)
    redirect = reverse_lazy('adm:presup-update', kwargs={'pk': kwargs['pk']}).strip()
    try:
        presupVers = Version.objects.get_for_object(obj)
        if presupVers:
            ultRev = presupVers.first()
            obj.nro_revision -= 1
            if ultRev.field_dict['revisionar']:
                obj.revisionar = True
            obj.save()
            ultRev.delete()
        return JsonResponse({'ok': 'ok', 'redirect': redirect})
    except:
        return JsonResponse({'err': 'err', 'redirect': redirect})


class PresupuestoCreate(CreateView):
    model = Presupuesto
    form_class = PresupuestoForm

    @method_decorator(permission_required('adm.add_presupuesto',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(PresupuestoCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PresupuestoCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('adm:presup-update', kwargs={'pk': self.object.id})


#===========================================
#========== VISTAS PRESUPUESTO =============
#===========================================


class PresupuestoList(ListView):
    model = Presupuesto
    template_name = 'adm/presupuesto_list.html'
    paginate_by = 30

    def _checkstate(self, queryset):
        """
        Chequeo los presupuestos que hay que cancelar.
        Seran cancelados los presupuestos que no hayan sido aceptados pasados 21 dias corridos
        de la fecha de realizacion del mismo.
        """
        for presup in queryset.filter(estado='borrador').exclude(fecha_realizado=None):
            if presup.fecha_realizado + timedelta(days=21) <= datetime.now().date():
                presup._toState_cancelado()

    def get_queryset(self):
        # Por defecto los ordeno por fecha de realizacion (desc)
        queryset = Presupuesto.objects.all().order_by('-codigo')
        kwargs = {}
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                elif key == 'estado':
                    kwargs['%s__in' % key] = [x.split('(')[0] for x in vals]
                elif key == 'fecha_realizado' or key == 'fecha_aceptado' \
                    or key == 'fecha_solicitado' or key == 'fecha_instrumento':
                    kwargs['%s__in' % key] = [datetime.strptime(v, "%d/%m/%Y")
                           for v in vals]
                else:
                    # Este caso lo trato aparte ya que estos campos no forman parte del presupuesto
                    kwargs['%s__in' % key] = vals
                    if key.find('ofertatec__') != -1:
                        ot_queryset = OfertaTec_Linea.objects.all()
                        ofertatec_lineas = ot_queryset.filter(**kwargs)
                        turnos = [ot.turno for ot in ofertatec_lineas]
                        presup = [p.id for p in queryset if p.get_turno_activo() in turnos]
                        p_queryset = queryset.filter(id__in=presup)
                        return p_queryset
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        self._checkstate(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PresupuestoList, self).get_context_data(**kwargs)

        presupuestos = Presupuesto.objects.all()
        turnos = [p.get_turno_activo() for p in presupuestos]

        presupuestos_by_page = context['object_list']
        turnos_by_page = [p.get_turno_activo() for p in presupuestos_by_page]

        context['tuple_paginated_list'] = list(zip(presupuestos_by_page, turnos_by_page))
        context['tuple_all_list'] = list(zip(presupuestos, turnos))

        field_names = ['estado', 'codigo', 'usuario__nombre', 'usuario__nro_usuario',
                        #'fecha_solicitado',
                        #'ofertatec__tipo_servicio',
                       'ofertatec__area',
                       #'usuario__rubro',
                       'fecha_realizado',
                       'fecha_aceptado',
                       'fecha_instrumento',
                       'nro_recepcion']
        field_labels = ['Estado', 'Nro.', 'Usuario', 'Nro Usuario',
                        #'Fecha de Solicitud',
                        #'Tipo de Servicio',
                        'Area',
                        #'Rubro',
                        'Fecha de Realizacion',
                        'Fecha de Aceptacion',
                        'Llegada del Instrumento',
                        'Nro Recepcion']
        # Agregado para mostrar los campos ordenados
        # Presup en borrador
        borrCount = len(presupuestos.filter(estado='borrador'))
        # Presup aceptados
        acepCount = len(presupuestos.filter(estado='aceptado'))
        # Presup finalizados
        finCount = len(presupuestos.filter(estado='finalizado'))
        # Presup cancelados
        canCount = len(presupuestos.filter(estado='cancelado'))
        options = []
        estado_vals = ['borrador('+str(borrCount)+')', 'aceptado('+str(acepCount)+')', 'finalizado('+str(finCount)+')', 'cancelado('+str(canCount)+')']
        options.append(estado_vals)
        cod_vals = sorted(set([p.codigo for p in presupuestos]))
        options.append(cod_vals)
        usuario_vals = sorted(set([p.usuario.nombre for p in presupuestos]))
        options.append(usuario_vals)
        nro_usuario_vals = sorted(set([p.usuario.nro_usuario for p in presupuestos]))
        options.append(nro_usuario_vals)
        #fec1_vals = set([p.fecha_solicitado.strftime("%d/%m/%Y")
               #for p in presupuestos if p.fecha_solicitado if not None])
        #options.append(fec1_vals)
        # ofertatec_linea es un campo many2one
        #ofertatec_list = [t.ofertatec_linea_set for p, t in context['presupuesto_list']
                                           #if t is not None]
        ofertatec_list = [t.ofertatec_linea_set for p, t in context['tuple_all_list']
                                           if t is not None]
        ofertatec_plist = reduce(lambda x, y: x + y,
                                 [[t for t in o.get_queryset()] for o in ofertatec_list], [])
        #serv_vals = set([o.ofertatec.tipo_servicio for o in ofertatec_plist])
        #options.append(serv_vals)
        area_vals = sorted(set([o.ofertatec.area for o in ofertatec_plist]))
        options.append(area_vals)
        #rubro_vals = set([p.usuario.rubro for p in presupuestos])
        #options.append(rubro_vals)
        fec2_vals = sorted(set([p.fecha_realizado.strftime("%d/%m/%Y")
                        for p in presupuestos if p.fecha_realizado is not None]))
        options.append(fec2_vals)
        fec3_vals = sorted(set([p.fecha_aceptado.strftime("%d/%m/%Y")
                        for p in presupuestos if p.fecha_aceptado if not None]))
        options.append(fec3_vals)
        fec4_vals = sorted(set([p.fecha_instrumento.strftime("%d/%m/%Y")
                      for p in presupuestos if p.fecha_instrumento if not None]))
        options.append(fec4_vals)
        nro_recepcion_vals = sorted(set([p.nro_recepcion for p in presupuestos]))
        options.append(nro_recepcion_vals)
        context['fields'] = list(zip(field_names, field_labels, options))
        # Chequeo los filtros seleccionados para conservar el estado de los
        # checkboxes
        checked_fields = []
        for key, vals in self.request.GET.lists():
            if key != 'order_by':
                checked_fields += ["%s_%s" % (v, key) for v in vals]
        context['checked_fields'] = checked_fields
        # Fecha de hoy para coloreo de filas
        context['today'] = datetime.now().strftime("%d/%m/%Y")
        # Para la paginacion
        if self.request.GET.has_key('order_by'):
            context['order_by'] = self.request.GET['order_by']
        return context

    def _actualizar_precios(self, request, presup_id, *args, **kwargs):
        """Retorna True si se actualizaron los precios de las OTs"""
        obj_presup = Presupuesto.objects.get(pk=presup_id)
        if not obj_presup._vigente():
            obj_turno = obj_presup.get_turno_activo()
            if obj_turno:
                kwargs['pk'] = presup_id
                for linea in obj_turno.ofertatec_linea_set.all():
                    obj_ofertatec = OfertaTec.objects.get(pk=linea.ofertatec.id)
                    if linea.precio != obj_ofertatec.precio:
                        linea.precio = obj_ofertatec.precio
                        linea.save()
                        obj_presup.nro_revision += 1
                        obj_presup.save()
            return True
        # Si el presupuesto esta vigente no le hago modificaciones
        else:
            return False
        #return HttpResponseRedirect(reverse_lazy('adm:presup-update', kwargs=kwargs))

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Finalizar' in request.POST:
            if request.user.has_perm('adm.finish_presupuesto'):
                presup_id = request.POST.get('Finalizar')
                presup_obj = Presupuesto.objects.get(pk=presup_id)
                try:
                    presup_obj._toState_finalizado()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Cancelar' in request.POST:
            if request.user.has_perm('adm.cancel_presupuesto'):
                presup_id = request.POST.get('Cancelar')
                presup_obj = Presupuesto.objects.get(pk=presup_id)
                try:
                    presup_obj._toState_cancelado()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_presupuesto'):
                presup_id = request.POST.get('Eliminar')
                presup_obj = Presupuesto.objects.get(pk=presup_id)
                presup_obj._delete()
                response_dict['redirect'] = reverse_lazy('adm:presup-list').strip()
            else:
                raise PermissionDenied
        if 'Actualizar' in request.POST:
            presup_id = request.POST.get('Actualizar')
            #return self._actualizar_precios(request, presup_id, args, kwargs)
            res = self._actualizar_precios(request, presup_id, args, kwargs)
            if not res:
                response_dict['ok'] = False
                response_dict['msg'] = """No se pueden actualizar los precios ya que el presupuesto\
                                          aun esta vigente.\n Para esto deberan pasar al menos 15 dias
                                          habiles desde su realizacion."""
        return JsonResponse(response_dict)


class PresupuestoDelete(DeleteView):
    model = Presupuesto
    success_url = reverse_lazy('adm:presup-list')

    @method_decorator(permission_required('adm.delete_presupuesto',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(PresupuestoCreate, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'cancelar' in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(PresupuestoDelete, self).post(request, *args, **kwargs)


class PresupuestoUpdate(UpdateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name_suffix = '_form'
    success_url = reverse_lazy('adm:presup-list')

    @method_decorator(permission_required('adm.change_presupuesto',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(PresupuestoUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PresupuestoUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['turno_activo'] = (context['object']).get_turno_activo()
        context['revision'] = self.request.GET.get('revision', False)
        # Revisionado
        presupVers = Version.objects.get_for_object(self.object)
        turnoVersByRevision = []
        usuarioVersByRevision = []
        otLineaVersByRevision = []
        #import pdb; pdb.set_trace()
        if presupVers:
            for pv in presupVers:
                revId = pv.revision.id
                # Todos los objetos versionados en la revision revId
                objectsVersiones = Version.objects.filter(revision=revId)
                # Todos los turnos versionados en la revision revId
                tv = objectsVersiones.filter(content_type__model='turno')
                turnoVersByRevision.append(tv)
                # Todos los usuarios versionados en la revision revId
                uv = objectsVersiones.filter(content_type__model='usuario')
                usuarioVersByRevision.append(uv)
                # Todos las lineas de ot versionados en la revision revId
                ot = objectsVersiones.filter(content_type__model='ofertatec_linea').order_by('object_id')
                otLineaVersByRevision.append(ot)

        context['presupVersions'] = zip(presupVers, turnoVersByRevision, usuarioVersByRevision, otLineaVersByRevision)
        return context

    def get_success_url(self):
        #import pdb; pdb.set_trace()
        return reverse_lazy('adm:presup-update', kwargs={'pk': self.object.id})

#=================================================
#========= VISTAS OFERTA TECNOLOGICA =============
#=================================================


class OfertaTecList(ListView):
    model = OfertaTec
    paginate_by = 50

    def get_queryset(self):
        queryset = OfertaTec.objects.all()
        kwargs = {}
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                else:
                    kwargs['%s__in' % key] = vals
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OfertaTecList, self).get_context_data(**kwargs)
        ofertas = OfertaTec.objects.all()
        field_names = ['proveedor', 'codigo', 'rubro', 'subrubro',
                       'tipo_servicio', 'area', 'detalle', 'precio']
        field_labels = ['Proveedor', 'Codigo', 'Rubro', 'Subrubro',
                        'Tipo de Servicio', 'Area', 'Detalle', 'Precio']
        # Agregado para mostrar los campos ordenados
        options = []
        prov_vals = sorted(set([o.proveedor for o in ofertas]))
        options.append(prov_vals)
        cod_vals = sorted(set([o.codigo for o in ofertas]))
        options.append(cod_vals)
        rubro_vals = sorted(set([o.rubro for o in ofertas]))
        options.append(rubro_vals)
        subrubro_vals = sorted(set([o.subrubro for o in ofertas]))
        options.append(subrubro_vals)
        serv_vals = sorted(set([o.tipo_servicio for o in ofertas]))
        options.append(serv_vals)
        area_vals = sorted(set([o.area for o in ofertas]))
        options.append(area_vals)
        detalle_vals = sorted(set([o.detalle for o in ofertas]))
        options.append(detalle_vals)
        precio_vals = sorted(set([o.precio for o in ofertas]))
        options.append(precio_vals)
        context['fields'] = list(zip(field_names, field_labels, options))
        # Chequeo los filtros seleccionados para conservar el estado de los
        # checkboxes
        checked_fields = []
        for key, vals in self.request.GET.lists():
            if key != 'order_by':
                checked_fields += ["%s_%s" % (v, key) for v in vals]
        context['checked_fields'] = checked_fields
        # Para la paginacion
        if self.request.GET.has_key('order_by'):
            context['order_by'] = self.request.GET['order_by']
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_ofertatec'):
                ofertatec_id = request.POST.get('Eliminar')
                ofertatec_obj = OfertaTec.objects.get(pk=ofertatec_id)
                if not ofertatec_obj._delete():
                    response_dict['ok'] = False
                    response_dict['msg'] = 'No se puede borrar la oferta ya que tiene\
                                            turnos asociados'
                else:
                    response_dict['redirect'] = reverse_lazy('adm:ofertatec-list').strip()
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)


class OfertaTecCreate(CreateView):
    model = OfertaTec
    form_class = OfertaTecForm

    @method_decorator(permission_required('adm.add_ofertatec',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OfertaTecCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OfertaTecCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('adm:ofertatec-update', kwargs={'pk': self.object.id})


class OfertaTecDelete(DeleteView):
    model = OfertaTec
    success_url = reverse_lazy('adm:ofertatec-list')

    @method_decorator(permission_required('adm.delete_ofertatec',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OfertaTecDelete, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'cancelar' in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(OfertaTecDelete, self).post(request, *args, **kwargs)


class OfertaTecUpdate(UpdateView):
    model = OfertaTec
    form_class = OfertaTecForm
    template_name_suffix = '_form'

    @method_decorator(permission_required('adm.change_ofertatec',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OfertaTecUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OfertaTecUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:ofertatec-update', kwargs={'pk': self.object.id})


#===========================================
#======== VISTAS USUARIO =============
#===========================================


class UsuarioList(ListView):
    model = Usuario
    paginate_by = 25

    def get_queryset(self):
        queryset = Usuario.objects.all()
        kwargs = {}
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])

                else:
                    kwargs['%s__in' % key] = vals
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UsuarioList, self).get_context_data(**kwargs)
        usuarios = Usuario.objects.all()
        field_names = ['nro_usuario', 'nombre', 'cuit', 'mail', 'rubro']
        field_labels = ['Nro. Usuario', 'Nombre', 'Cuit', 'Mail', 'Rubro']
        # Agregado para mostrar los campos ordenados
        options = []
        nro_vals = sorted(set([u.nro_usuario for u in usuarios]))
        options.append(nro_vals)
        nombre_vals = sorted(set([u.nombre for u in usuarios]))
        options.append(nombre_vals)
        cuit_vals = sorted(set([u.cuit for u in usuarios]))
        options.append(cuit_vals)
        mail_vals = sorted(set([u.mail for u in usuarios if u.mail is not None]))
        options.append(mail_vals)
        rubro_vals = sorted(set([u.rubro for u in usuarios]))
        options.append(rubro_vals)
        context['fields'] = list(zip(field_names, field_labels, options))
        # Chequeo los filtros seleccionados para conservar el estado de los
        # checkboxes
        checked_fields = []
        for key, vals in self.request.GET.lists():
            if key != 'order_by':
                checked_fields += ["%s_%s" % (v, key) for v in vals]
        context['checked_fields'] = checked_fields
        # Para la paginacion
        if self.request.GET.has_key('order_by'):
            context['order_by'] = self.request.GET['order_by']
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_usuario'):
                user_id = request.POST.get('Eliminar')
                user_obj = Usuario.objects.get(pk=user_id)
                if not user_obj._delete():
                    response_dict['ok'] = False
                    response_dict['msg'] = 'No se puede borrar el usuario ya que tiene\
                                            presupuestos asociados'
                response_dict['redirect'] = reverse_lazy('adm:usuarios-list').strip()
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)


class UsuarioCreate(CreateView):
    model = Usuario
    form_class = UsuarioForm

    @method_decorator(permission_required('adm.add_usuario',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsuarioCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('adm:usuarios-update', kwargs={'pk': self.object.id})


class UsuarioDelete(DeleteView):
    model = Usuario
    success_url = reverse_lazy('adm:usuarios-list')

    @method_decorator(permission_required('adm.delete_usuario',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioDelete, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'cancelar' in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(UsuarioDelete, self).post(request, *args, **kwargs)


class UsuarioUpdate(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name_suffix = '_form'

    @method_decorator(permission_required('adm.change_usuario',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsuarioUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:usuarios-update', kwargs={'pk': self.object.id})