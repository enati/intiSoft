# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Presupuesto, OfertaTec, Usuario, OT, Factura
from lab.models import OfertaTec_Linea
from .forms import PresupuestoForm, OfertaTecForm, UsuarioForm, OTForm, Factura_LineaFormSet, OT_LineaFormSet
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

            actualRevNumber = 'P_REV' + str(obj.nro_revision)

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
            ultRev.revision.revert(True)
            ultRev.revision.delete()
        return JsonResponse({'ok': 'ok', 'redirect': redirect})
    except:
        return JsonResponse({'err': 'err', 'redirect': redirect})


#===========================================
#========== VISTAS OT =============
#===========================================


class OTCreate(CreateView):
    model = OT
    form_class = OTForm
    success_url = reverse_lazy('adm:ot-list')

    @method_decorator(permission_required('adm.add_ot',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OTCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OTCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('adm:ot-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        factura_form = Factura_LineaFormSet()
        ot_linea_form = OT_LineaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  factura_form=factura_form,
                                  ot_linea_form=ot_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        factura_form = Factura_LineaFormSet(self.request.POST)
        ot_linea_form = OT_LineaFormSet(self.request.POST)
        if (form.is_valid() and factura_form.is_valid() and ot_linea_form.is_valid()):
            return self.form_valid(form, factura_form, ot_linea_form)
        else:
            return self.form_invalid(form, factura_form, ot_linea_form)

    def form_valid(self, form, factura_form, ot_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Factuas and Recibos then redirects to a
        success page.
        """
        self.object = form.save()
        factura_form.instance = self.object
        factura_form.save()
        ot_linea_form.instance = self.object
        ot_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, factura_form, ot_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  factura_form=factura_form,
                                  ot_linea_form=ot_linea_form))


class OTUpdate(UpdateView):
    model = OT
    form_class = OTForm
    template_name_suffix = '_form'
    success_url = reverse_lazy('adm:ot-list')

    @method_decorator(permission_required('adm.change_ot',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OTUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OTUpdate, self).get_context_data(**kwargs)
        turno = (context['object']).presupuesto.get_turno_activo()
        context['turno_activo'] = turno
        context['edit'] = self.request.GET.get('edit', False)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:ot-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates filled versions of the form
        and its inline formsets.
        """
        self.object = OT.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        factura_form = Factura_LineaFormSet(instance=self.object)
        ot_linea_form = OT_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  factura_form=factura_form,
                                  ot_linea_form=ot_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = OT.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        factura_form = Factura_LineaFormSet(self.request.POST, instance=self.object)
        ot_linea_form = OT_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and factura_form.is_valid() and ot_linea_form.is_valid()):
            return self.form_valid(form, factura_form, ot_linea_form)
        else:
            return self.form_invalid(form, factura_form, ot_linea_form)

    def form_valid(self, form, factura_form, ot_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Facturas and then redirects to a
        success page.
        """
        form.save()
        factura_form.save()
        ot_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, factura_form, ot_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  factura_form=factura_form,
                                  ot_linea_form=ot_linea_form))


class OTList(ListView):
    model = Presupuesto
    template_name = 'adm/ot_list.html'
    paginate_by = 30

    def get_queryset(self):
        # Por defecto los ordeno por codigo (desc)
        queryset = OT.objects.all().order_by('-codigo')
        kwargs = {}
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                elif key == 'estado':
                    kwargs['%s__in' % key] = [x.split('(')[0] for x in vals]
                elif key == 'fecha_realizado' or key == 'fecha_aviso':
                    kwargs['%s__in' % key] = [datetime.strptime(v, "%d/%m/%Y")
                           for v in vals]
                elif key == 'area':
                    presup_by_ot = [o.presupuesto for o in queryset]
                    filtered_presup = [p for p in presup_by_ot if p.get_turno_activo().area in vals]
                    kwargs['presupuesto__in'] = filtered_presup
                elif key == 'factura':
                    ots = [o.id for o in queryset if o.factura_set.get_queryset().filter(numero__in=vals)]
                    kwargs['id__in'] = ots
                elif key == 'factura__fecha':
                    factura = Factura.objects.all().filter(fecha__in=[datetime.strptime(v, "%d/%m/%Y")
                                                                         for v in vals])
                    ots = [f.ot.id for f in factura]
                    kwargs['id__in'] = ots
                elif key == 'factura__importe':
                    factura = Factura.objects.filter.all().filter(importe__in=vals)
                    ots = [f.ot.id for f in factura]
                    kwargs['id__in'] = ots
                elif key == 'recibo':
                    factura = Factura.objects.all()
                    ots = [f.ot.id for f in factura if f.recibo_set.get_queryset().filter(numero__in=vals)]
                    kwargs['id__in'] = ots
                elif key == 'recibo__fecha':
                    factura = Factura.objects.all()
                    ots = [f.ot.id for f in factura
                        if f.recibo_set.get_queryset().filter(
                                        fecha__in=[datetime.strptime(v, "%d/%m/%Y")
                                                   for v in vals])]
                    kwargs['id__in'] = ots
                elif key == 'recibo__tipo':
                    factura = Factura.objects.all()
                    ots = [f.ot.id for f in factura
                        if f.recibo_set.get_queryset().filter(
                                        comprobante_cobro__in=vals)]
                    kwargs['id__in'] = ots
                elif key == 'remito':
                    factura = Factura.objects.all()
                    ots = [f.ot.id for f in factura if f.remito_set.get_queryset().filter(numero__in=vals)]
                    kwargs['id__in'] = ots
                else:
                    kwargs['%s__in' % key] = vals
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OTList, self).get_context_data(**kwargs)
        ots = OT.objects.all()

        field_names = ['estado', 'presupuesto__codigo', 'presupuesto__usuario__nombre',
                       'codigo', 'fecha_realizado', 'importe', 'area', 'factura', 'factura__fecha',
                       'factura__importe', 'fecha_aviso',
                       'recibo', 'recibo_tipo', 'recibo__fecha', 'recibo__importe', 'remito']
        field_labels = ['Estado', 'Nro. Presup.', 'Usuario', 'Nro. OT', 'Fecha', 'Imp.',
                        'Area', 'Nro. Factura', 'Fecha', 'Imp.', 'Fecha Aviso',
                        'Recibo', 'Tipo', 'Fecha', 'Imp.', 'Remito']

        # OTs sin facturar
        sfCount = len(ots.filter(estado='sin_facturar'))
        # OTs sin pagar
        npCount = len(ots.filter(estado='no_pago'))
        # OTs pagadas
        pagCount = len(ots.filter(estado='pagado'))
        # OTs canceladas
        canCount = len(ots.filter(estado='cancelado'))
        options = []
        estado_vals = ['sin_facturar(' + str(sfCount) + ')',
                       'no_pago(' + str(npCount) + ')',
                       'pagado(' + str(pagCount) + ')',
                       'cancelado(' + str(canCount) + ')']
        options.append(estado_vals)
        presup_vals = sorted(set([o.presupuesto.codigo for o in ots]))
        options.append(presup_vals)
        usuario_vals = sorted(set([o.presupuesto.usuario.nombre for o in ots]))
        options.append(usuario_vals)
        cod_vals = sorted(set([o.codigo for o in ots]))
        options.append(cod_vals)
        fec1_vals = sorted(set([o.fecha_realizado.strftime("%d/%m/%Y")
                        for o in ots if o.fecha_realizado is not None]))
        options.append(fec1_vals)
        importe_vals = sorted(set([o.importe for o in ots if o.importe]))
        options.append(importe_vals)
        area_vals = sorted(set([o.presupuesto.get_turno_activo().area for o in ots]))
        options.append(area_vals)
        factura_list = [o.factura_set for o in ots]
        factura_plist = reduce(lambda x, y: x + y,
                                 [[t for t in f.get_queryset()] for f in factura_list], [])
        factura_vals = sorted(set([f.numero for f in factura_plist]))
        options.append(factura_vals)
        factura_fecha_vals = sorted(set([f.fecha.strftime("%d/%m/%Y") for f in factura_plist
                                         if f.fecha is not None]))
        options.append(factura_fecha_vals)
        importef_vals = sorted(set([f.importe for f in factura_plist]))
        options.append(importef_vals)
        fec2_vals = sorted(set([o.fecha_aviso.strftime("%d/%m/%Y")
                        for o in ots if o.fecha_aviso is not None]))
        options.append(fec2_vals)
        recibo_list = [f.recibo_set for f in factura_plist]
        recibo_plist = reduce(lambda x, y: x + y,
                                 [[t for t in r.get_queryset()] for r in recibo_list], [])
        recibo_vals = sorted(set([r.numero for r in recibo_plist]))
        options.append(recibo_vals)
        recibo_tipo_vals = sorted(set([r.comprobante_cobro for f in recibo_plist]))
        options.append(recibo_tipo_vals)
        recibo_fecha_vals = sorted(set([r.fecha.strftime("%d/%m/%Y") for f in recibo_plist if r.fecha is not None]))
        options.append(recibo_fecha_vals)
        recibo_importe_vals = sorted(set([r.importe for f in recibo_plist]))
        options.append(recibo_importe_vals)
        remito_list = [f.remito_set for f in factura_plist]
        remito_plist = reduce(lambda x, y: x + y,
                                 [[t for t in r.get_queryset()] for r in remito_list], [])
        remito_vals = sorted(set([r.numero for r in remito_plist]))
        options.append(remito_vals)
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
        if 'order_by' in self.request.GET:
            context['order_by'] = self.request.GET['order_by']
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'CancelarF' in request.POST:
            if request.user.has_perm('adm.cancel_factura'):
                factura_id = request.POST.get('CancelarF')
                factura_obj = Factura.objects.get(pk=factura_id)
                try:
                    factura_obj._toState_cancelado()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Cancelar' in request.POST:
            if request.user.has_perm('adm.cancel_ot'):
                ot_id = request.POST.get('Cancelar')
                ot_obj = OT.objects.get(pk=ot_id)
                try:
                    ot_obj._toState_cancelado()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_ot'):
                ot_id = request.POST.get('Eliminar')
                ot_obj = OT.objects.get(pk=ot_id)
                ot_obj._delete()
                response_dict['redirect'] = reverse_lazy('adm:ot-list').strip()
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)

#===========================================
#========== VISTAS PRESUPUESTO =============
#===========================================


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
        # Presup finalizados
        facCount = len(presupuestos.filter(estado='en_proceso_de_facturacion'))
        # Presup cancelados
        canCount = len(presupuestos.filter(estado='cancelado'))
        options = []
        estado_vals = ['borrador('+str(borrCount)+')', 'aceptado('+str(acepCount)+')', 'en_proceso_de_facturacion('+str(facCount)+')', 'finalizado('+str(finCount)+')', 'cancelado('+str(canCount)+')']
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
                        for p in presupuestos if p.fecha_aceptado is not None]))
        options.append(fec3_vals)
        fec4_vals = sorted(set([p.fecha_instrumento.strftime("%d/%m/%Y")
                      for p in presupuestos if p.fecha_instrumento is not None]))
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
        presupVers = Version.objects.get_for_object(self.object).exclude(revision__comment__contains='T_')
        turnoVersByRevision = []
        usuarioVersByRevision = []
        otLineaVersByRevision = []
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
        #import pdb; pdb.set_trace()
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

