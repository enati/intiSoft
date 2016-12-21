# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Presupuesto, OfertaTec, Usuario, OT, OTML, SOT, RUT, Factura
from lab.models import OfertaTec_Linea
from .forms import PresupuestoForm, OfertaTecForm, UsuarioForm, OTForm, OTMLForm,\
                   Factura_LineaFormSet, OT_LineaFormSet, Remito_LineaFormSet, SOTForm, RUTForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from .utils import genWord, genSOT, genRUT
from django.http import JsonResponse
import json
from intiSoft.exception import StateError
from reversion.models import Version
import reversion
from time import time

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
            vals['ofertatec'].append((o.ofertatec.codigo, o.ofertatec.detalle, o.precio_total))
    return genWord(vals)


def viewSOT(request, *args, **kwargs):
    sot_id = kwargs.get('pk')
    sot_obj = SOT.objects.get(id=sot_id)
    vals = {}
    vals['nro_ejecutor'] = sot_obj.ejecutor.nro_usuario
    vals['ejecutor'] = sot_obj.ejecutor.nombre
    vals['nro_deudor'] = sot_obj.deudor.nro_usuario
    vals['deudor'] = sot_obj.deudor.nombre
    vals['fecha_apertura'] = sot_obj.fecha_realizado.strftime('%d/%m/%Y')
    vals['ot'] = sot_obj.ot
    vals['expediente'] = sot_obj.expediente
    vals['codigo'] = sot_obj.codigo
    vals['fecha_prevista'] = sot_obj.fecha_prevista.strftime('%d/%m/%Y')
    vals['usuario_final'] = sot_obj.usuario_final.nombre if sot_obj.usuario_final else ''
    vals['importe_neto'] = sot_obj.importe_neto
    vals['importe_bruto'] = sot_obj.importe_bruto
    vals['descuento'] = sot_obj.descuento
    vals['ofertatec'] = []
    acc = 0
    for o in sot_obj.ot_linea_set.get_queryset():
        vals['ofertatec'].append((o.ofertatec.codigo, o.detalle, o.tipo_servicio, o.cantidad, o.precio, o.precio_total))
        acc += o.precio_total
    vals['arancel_previsto'] = acc
    vals['plantilla'] = 'SOT.docx'
    return genSOT(vals)


def viewRUT(request, *args, **kwargs):
    rut_id = kwargs.get('pk')
    rut_obj = RUT.objects.get(id=rut_id)
    vals = {}
    vals['nro_ejecutor'] = rut_obj.ejecutor.nro_usuario
    vals['ejecutor'] = rut_obj.ejecutor.nombre
    vals['nro_deudor'] = rut_obj.deudor.nro_usuario
    vals['deudor'] = rut_obj.deudor.nombre
    vals['codigo'] = rut_obj.codigo
    vals['fecha_apertura'] = rut_obj.fecha_realizado.strftime('%d/%m/%Y')
    vals['fecha_prevista'] = rut_obj.fecha_prevista.strftime('%d/%m/%Y')
    vals['importe_neto'] = rut_obj.importe_neto
    vals['importe_bruto'] = rut_obj.importe_bruto
    vals['descuento'] = rut_obj.descuento
    vals['ofertatec'] = []
    acc = 0
    for o in rut_obj.ot_linea_set.get_queryset():
        vals['ofertatec'].append((o.ofertatec.codigo, o.detalle, o.tipo_servicio, o.cantidad, o.precio, o.precio_total))
        acc += o.precio_total
    vals['arancel_previsto'] = acc
    vals['plantilla'] = 'RUT.docx'
    return genRUT(vals)


def get_user(request, *args, **kwargs):
    try:
        user_id = request.GET['user_id']
        user_obj = Usuario.objects.get(pk=user_id)
        data = {'nro_usuario': user_obj.nro_usuario,
                'cuit': user_obj.cuit,
                'rubro': user_obj.rubro,
                'mail': user_obj.mail,
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
        remito_form = Remito_LineaFormSet()
        ot_linea_form = OT_LineaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  factura_form=factura_form,
                                  remito_form=remito_form,
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
        remito_form = Remito_LineaFormSet(self.request.POST)
        ot_linea_form = OT_LineaFormSet(self.request.POST)
        if (form.is_valid() and factura_form.is_valid()
            and ot_linea_form.is_valid() and remito_form.is_valid()):
            return self.form_valid(form, factura_form, remito_form, ot_linea_form)
        else:
            return self.form_invalid(form, factura_form, remito_form, ot_linea_form)

    def form_valid(self, form, factura_form, remito_form, ot_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Factuas and Recibos then redirects to a
        success page.
        """
        self.object = form.save()
        factura_form.instance = self.object
        factura_form.save()
        remito_form.instance = self.object
        remito_form.save()
        ot_linea_form.instance = self.object
        ot_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, factura_form, remito_form, ot_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  factura_form=factura_form,
                                  remito_form=remito_form,
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
        remito_form = Remito_LineaFormSet(instance=self.object)
        ot_linea_form = OT_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  factura_form=factura_form,
                                  remito_form=remito_form,
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
        remito_form = Remito_LineaFormSet(self.request.POST, instance=self.object)
        ot_linea_form = OT_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and factura_form.is_valid()
           and ot_linea_form.is_valid() and remito_form.is_valid()):
            return self.form_valid(form, factura_form, remito_form, ot_linea_form)
        else:
            return self.form_invalid(form, factura_form, remito_form, ot_linea_form)

    def form_valid(self, form, factura_form, remito_form, ot_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Facturas and then redirects to a
        success page.
        """
        form.save()
        factura_form.save()
        remito_form.save()
        ot_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, factura_form, remito_form, ot_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  factura_form=factura_form,
                                  remito_form=remito_form,
                                  ot_linea_form=ot_linea_form))


class OTList(ListView):
    model = OT
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
                    ots = [f.object_id for f in factura if f.content_type.model == 'ot']
                    kwargs['id__in'] = ots
                elif key == 'factura__importe':
                    factura = Factura.objects.all().filter(importe__in=vals)
                    ots = [f.object_id for f in factura if f.content_type.model == 'ot']
                    kwargs['id__in'] = ots
                elif key == 'factura__fecha_aviso':
                    factura = Factura.objects.all().filter(fecha_aviso__in=[datetime.strptime(v, "%d/%m/%Y")
                                                                         for v in vals])
                    ots = [f.object_id for f in factura if f.content_type.model == 'ot']
                    kwargs['id__in'] = ots
                elif key == 'recibo':
                    factura = Factura.objects.all()
                    ots = [f.object_id for f in factura
                            if f.recibo_set.get_queryset().filter(numero__in=vals)
                                and f.content_type.model == 'ot']
                    kwargs['id__in'] = ots
                elif key == 'recibo__fecha':
                    factura = Factura.objects.all()
                    ots = [f.object_id for f in factura
                            if f.recibo_set.get_queryset().filter(
                                            fecha__in=[datetime.strptime(v, "%d/%m/%Y")
                                                   for v in vals])
                                and f.content_type.model == 'ot']
                    kwargs['id__in'] = ots
                elif key == 'recibo__tipo':
                    factura = Factura.objects.all()
                    ots = [f.object_id for f in factura
                            if f.recibo_set.get_queryset().filter(
                                            comprobante_cobro__in=vals)
                                and f.content_type.model == 'ot']
                    kwargs['id__in'] = ots
                elif key == 'recibo__importe':
                    factura = Factura.objects.all()
                    ots = [f.object_id for f in factura
                            if f.recibo_set.get_queryset().filter(
                                            importe__in=vals)
                                and f.content_type.model == 'ot']
                    kwargs['id__in'] = ots
                elif key == 'remito':
                    factura = Factura.objects.all()
                    ots = [o.id for o in queryset if o.remito_set.get_queryset().filter(numero__in=vals)]
                    kwargs['id__in'] = ots
                else:
                    kwargs['%s__in' % key] = vals
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(OTList, self).get_context_data(**kwargs)
        ots = OT.objects.select_related()

        field_names = ['estado', 'presupuesto__codigo', 'presupuesto__usuario__nombre',
                       'codigo', 'fecha_realizado', 'importe_bruto', 'area', 'factura', 'factura__fecha',
                       'factura__importe', 'factura__fecha_aviso',
                       'recibo', 'recibo__tipo', 'recibo__fecha', 'recibo__importe', 'remito']
        field_labels = ['Estado', 'Nro. Presup.', 'Usuario', 'Nro. OT', 'Fecha', 'Imp. Bruto',
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
        importe_bruto_vals = sorted(set([o.importe_bruto for o in ots if o.importe_bruto]))
        options.append(importe_bruto_vals)
        area_vals = sorted(set([o.presupuesto.get_turno_activo().area for o in ots
                                if o.presupuesto.get_turno_activo() is not None]))
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
        fec2_vals = sorted(set([f.fecha_aviso.strftime("%d/%m/%Y") for f in factura_plist
                                         if f.fecha_aviso is not None]))
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
        recibo_importe_vals = sorted(set([r.importe for r in recibo_plist]))
        options.append(recibo_importe_vals)
        remito_list = [o.remito_set for o in ots]
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
        print "TIEMPO get_context_data: ", time() - t_inicial
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
        #Finalizo solo la OT
        if 'Finalizar1' in request.POST:
            if request.user.has_perm('adm.finish_ot'):
                ot_id = request.POST.get('Finalizar1')
                ot_obj = OT.objects.get(pk=ot_id)
                try:
                    num_recibos_factura = [f.recibo_set.count() for f in ot_obj.factura_set.all()]
                    num_recibos_total = reduce(lambda x, y: x + y, num_recibos_factura, 0)
                    if not num_recibos_total:
                        response_dict['ok'] = False
                        response_dict['msg'] = "La OT no tiene recibos registrados.\
                                                Para poder finalizarla debe estar pagada."
                    else:
                        ot_obj._toState_pagado(False)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        #Finalizo la OT y el Presupuesto asociado
        if 'Finalizar2' in request.POST:
            if request.user.has_perm('adm.finish_ot'):
                ot_id = request.POST.get('Finalizar2')
                ot_obj = OT.objects.get(pk=ot_id)
                presup_obj = ot_obj.presupuesto
                try:
                    num_recibos_factura = [f.recibo_set.count() for f in ot_obj.factura_set.all()]
                    num_recibos_total = reduce(lambda x, y: x + y, num_recibos_factura, 0)
                    if not num_recibos_total:
                        response_dict['ok'] = False
                        response_dict['msg'] = "La OT no tiene recibos registrados.\
                                                Para poder finalizarla debe estar pagada."
                    elif presup_obj.ot_set.exclude(id=ot_id).exclude(estado='pagado'):
                        response_dict['ok'] = False
                        response_dict['msg'] = "El Presupuesto no se puede finalizar ya que tiene\
                                                OTs no finalizadas."
                    else:
                        ot_obj._toState_pagado(True)
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
#================ OT ML ====================
#===========================================


class OTMLCreate(CreateView):
    model = OTML
    form_class = OTMLForm
    success_url = reverse_lazy('adm:otml-list')

    @method_decorator(permission_required('adm.add_otml',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OTMLCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OTMLCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('adm:otml-update', kwargs={'pk': self.object.id})

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
        if (form.is_valid() and factura_form.is_valid()
            and ot_linea_form.is_valid()):
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


class OTMLUpdate(UpdateView):
    model = OTML
    form_class = OTMLForm
    template_name_suffix = '_form'
    success_url = reverse_lazy('adm:otml-list')

    @method_decorator(permission_required('adm.change_ot',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OTMLUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OTMLUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:otml-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates filled versions of the form
        and its inline formsets.
        """
        self.object = OTML.objects.get(pk=kwargs['pk'])
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
        self.object = OTML.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        factura_form = Factura_LineaFormSet(self.request.POST, instance=self.object)
        ot_linea_form = OT_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and factura_form.is_valid()
           and ot_linea_form.is_valid()):
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


class OTMLList(ListView):
    model = OTML
    template_name = 'adm/otml_list.html'
    paginate_by = 30

    def get_queryset(self):
        # Por defecto los ordeno por codigo (desc)
        queryset = OTML.objects.all().order_by('-codigo')
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
                elif key == 'factura':
                    ots = [o.id for o in queryset if o.factura_set.get_queryset().filter(numero__in=vals)]
                    kwargs['id__in'] = ots
                elif key == 'factura__fecha':
                    factura = Factura.objects.all().filter(fecha__in=[datetime.strptime(v, "%d/%m/%Y")
                                                                         for v in vals])
                    ots = [f.object_id for f in factura if f.content_type.model == 'otml']
                    kwargs['id__in'] = ots
                elif key == 'factura__importe':
                    factura = Factura.objects.all().filter(importe__in=vals)
                    ots = [f.object_id for f in factura if f.content_type.model == 'otml']
                    kwargs['id__in'] = ots
                elif key == 'factura__fecha_aviso':
                    factura = Factura.objects.all().filter(fecha_aviso__in=[datetime.strptime(v, "%d/%m/%Y")
                                                                         for v in vals])
                    ots = [f.object_id for f in factura if f.content_type.model == 'otml']
                    kwargs['id__in'] = ots
                elif key == 'recibo':
                    factura = Factura.objects.all()
                    ots = [f.object_id for f in factura
                        if f.recibo_set.get_queryset().filter(numero__in=vals)
                            and f.content_type.model == 'otml']
                    kwargs['id__in'] = ots
                elif key == 'recibo__fecha':
                    factura = Factura.objects.all()
                    ots = [f.object_id for f in factura
                        if f.recibo_set.get_queryset().filter(
                                        fecha__in=[datetime.strptime(v, "%d/%m/%Y")
                                                   for v in vals])
                            and f.content_type.model == 'otml']
                    kwargs['id__in'] = ots
                elif key == 'recibo__tipo':
                    factura = Factura.objects.all()
                    ots = [f.object_id for f in factura
                        if f.recibo_set.get_queryset().filter(
                                        comprobante_cobro__in=vals)
                            and f.content_type.model == 'otml']
                    kwargs['id__in'] = ots
                elif key == 'recibo__importe':
                    factura = Factura.objects.all()
                    ots = [f.object_id for f in factura
                        if f.recibo_set.get_queryset().filter(
                                        importe__in=vals)
                            and f.content_type.model == 'otml']
                    kwargs['id__in'] = ots
                else:
                    kwargs['%s__in' % key] = vals
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(OTMLList, self).get_context_data(**kwargs)
        ots = OTML.objects.select_related()

        field_names = ['estado', 'codigo', 'fecha_realizado', 'importe_bruto', 'factura', 'factura__fecha',
                       'factura__importe', 'factura__fecha_aviso',
                       'recibo', 'recibo__tipo', 'recibo__fecha', 'recibo__importe']
        field_labels = ['Estado', 'Nro. OT', 'Fecha', 'Imp. Bruto',
                        'Nro. Factura', 'Fecha', 'Imp.', 'Fecha Aviso',
                        'Recibo', 'Tipo', 'Fecha', 'Imp.']

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
        cod_vals = sorted(set([o.codigo for o in ots]))
        options.append(cod_vals)
        fec1_vals = sorted(set([o.fecha_realizado.strftime("%d/%m/%Y")
                        for o in ots if o.fecha_realizado is not None]))
        options.append(fec1_vals)
        importe_bruto_vals = sorted(set([o.importe_bruto for o in ots if o.importe_bruto]))
        options.append(importe_bruto_vals)
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
        fec2_vals = sorted(set([f.fecha_aviso.strftime("%d/%m/%Y") for f in factura_plist
                                         if f.fecha_aviso is not None]))
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
        print "TIEMPO get_context_data: ", time() - t_inicial
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
            if request.user.has_perm('adm.cancel_otml'):
                otml_id = request.POST.get('Cancelar')
                otml_obj = OTML.objects.get(pk=otml_id)
                try:
                    otml_obj._toState_cancelado()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Finalizar' in request.POST:
            if request.user.has_perm('adm.finish_otml'):
                otml_id = request.POST.get('Finalizar')
                otml_obj = OTML.objects.get(pk=otml_id)
                try:
                    num_recibos_factura = [f.recibo_set.count() for f in otml_obj.factura_set.all()]
                    num_recibos_total = reduce(lambda x, y: x + y, num_recibos_factura, 0)
                    if not num_recibos_total:
                        response_dict['ok'] = False
                        response_dict['msg'] = "La OT no tiene recibos registrados.\
                                                Para poder finalizarla debe estar pagada."
                    else:
                        otml_obj._toState_pagado(False)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_otml'):
                otml_id = request.POST.get('Eliminar')
                otml_obj = OTML.objects.get(pk=otml_id)
                otml_obj._delete()
                response_dict['redirect'] = reverse_lazy('adm:otml-list').strip()
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)


#===========================================
#================ SOT ====================
#===========================================


class SOTCreate(CreateView):
    model = SOT
    form_class = SOTForm

    @method_decorator(permission_required('adm.add_sot',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(SOTCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SOTCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('adm:sot-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ot_linea_form = OT_LineaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
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
        ot_linea_form = OT_LineaFormSet(self.request.POST)
        if (form.is_valid() and ot_linea_form.is_valid()):
            return self.form_valid(form, ot_linea_form)
        else:
            return self.form_invalid(form, ot_linea_form)

    def form_valid(self, form, ot_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Factuas and Recibos then redirects to a
        success page.
        """
        self.object = form.save()
        ot_linea_form.instance = self.object
        ot_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ot_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ot_linea_form=ot_linea_form))


class SOTUpdate(UpdateView):
    model = SOT
    form_class = SOTForm
    template_name_suffix = '_form'

    @method_decorator(permission_required('adm.change_sot',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(SOTUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SOTUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:sot-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates filled versions of the form
        and its inline formsets.
        """
        self.object = SOT.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ot_linea_form = OT_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ot_linea_form=ot_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = SOT.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ot_linea_form = OT_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and ot_linea_form.is_valid()):
            return self.form_valid(form, ot_linea_form)
        else:
            return self.form_invalid(form, ot_linea_form)

    def form_valid(self, form, ot_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Facturas and then redirects to a
        success page.
        """
        form.save()
        ot_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ot_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ot_linea_form=ot_linea_form))


class SOTList(ListView):
    model = SOT
    template_name = 'adm/sot_list.html'
    paginate_by = 30

    def get_queryset(self):
        # Por defecto los ordeno por codigo (desc)
        queryset = SOT.objects.all().order_by('-codigo')
        kwargs = {}
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                elif key == 'estado':
                    kwargs['%s__in' % key] = [x.split('(')[0] for x in vals]
                elif key == 'fecha_realizado':
                    kwargs['%s__in' % key] = [datetime.strptime(v, "%d/%m/%Y")
                           for v in vals]
                else:
                    kwargs['%s__in' % key] = vals
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(SOTList, self).get_context_data(**kwargs)
        sots = SOT.objects.select_related()

        field_names = ['estado', 'codigo', 'fecha_realizado', 'deudor', 'solicitante',
                       'importe_bruto', 'importe_neto', 'fecha_envio_ut', 'fecha_envio_cc',
                       'firmada']
        field_labels = ['Estado', 'Nro. SOT', 'Fecha Realizada', 'UT Deudora', 'Area Solic.',
                        'Imp. Bruto', 'Imp. Neto',  'Fecha Envio UT', 'Retorno Firmada',
                        'Fecha Envio CC']

        # SOT en borrador
        borrCount = len(sots.filter(estado='borrador'))
        # SOT pendientes
        penCount = len(sots.filter(estado='pendiente'))
        # SOT cobradas
        cobCount = len(sots.filter(estado='cobrada'))
        # SOT canceladas
        canCount = len(sots.filter(estado='cancelada'))
        options = []
        estado_vals = ['borrador(' + str(borrCount) + ')',
                       'pendiente(' + str(penCount) + ')',
                       'cobrada(' + str(cobCount) + ')',
                       'cancelada(' + str(canCount) + ')']
        options.append(estado_vals)
        cod_vals = sorted(set([s.codigo for s in sots]))
        options.append(cod_vals)
        fec1_vals = sorted(set([s.fecha_realizado.strftime("%d/%m/%Y")
                        for s in sots if s.fecha_realizado is not None]))
        options.append(fec1_vals)
        deudor_vals = sorted(set([s.deudor for s in sots if s.deudor]))
        options.append(deudor_vals)
        solicitante_vals = sorted(set([s.solicitante for s in sots if s.solicitante]))
        options.append(solicitante_vals)
        importe_bruto_vals = sorted(set([s.importe_bruto for s in sots if s.importe_bruto]))
        options.append(importe_bruto_vals)
        importe_neto_vals = sorted(set([s.importe_neto for s in sots if s.importe_neto]))
        options.append(importe_neto_vals)
        fec2_vals = sorted(set([s.fecha_envio_ut.strftime("%d/%m/%Y")
                        for s in sots if s.fecha_envio_ut is not None]))
        options.append(fec2_vals)
        fec3_vals = sorted(set([s.fecha_envio_cc.strftime("%d/%m/%Y")
                        for s in sots if s.fecha_envio_cc is not None]))
        options.append(fec3_vals)
        firmada_vals = sorted(set([s.firmada for s in sots if s.firmada]))
        options.append(firmada_vals)
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
        print "TIEMPO get_context_data: ", time() - t_inicial
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Cancelar' in request.POST:
            if request.user.has_perm('adm.cancel_sot'):
                sot_id = request.POST.get('Cancelar')
                sot_obj = SOT.objects.get(pk=sot_id)
                try:
                    sot_obj._toState_cancelada()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Finalizar' in request.POST:
            if request.user.has_perm('adm.finish_sot'):
                sot_id = request.POST.get('Finalizar')
                sot_obj = SOT.objects.get(pk=sot_id)
                try:
                    sot_obj._toState_cobrada()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_sot'):
                sot_id = request.POST.get('Eliminar')
                sot_obj = SOT.objects.get(pk=sot_id)
                sot_obj._delete()
                response_dict['redirect'] = reverse_lazy('adm:sot-list').strip()
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)

#===========================================
#================ RUT ====================
#===========================================


class RUTCreate(CreateView):
    model = RUT
    form_class = RUTForm

    @method_decorator(permission_required('adm.add_rut',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(RUTCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RUTCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('adm:rut-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ot_linea_form = OT_LineaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
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
        ot_linea_form = OT_LineaFormSet(self.request.POST)
        if (form.is_valid() and ot_linea_form.is_valid()):
            return self.form_valid(form, ot_linea_form)
        else:
            return self.form_invalid(form, ot_linea_form)

    def form_valid(self, form, ot_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Factuas and Recibos then redirects to a
        success page.
        """
        self.object = form.save()
        ot_linea_form.instance = self.object
        ot_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ot_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ot_linea_form=ot_linea_form))


class RUTUpdate(UpdateView):
    model = RUT
    form_class = RUTForm
    template_name_suffix = '_form'

    @method_decorator(permission_required('adm.change_rut',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(RUTUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RUTUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:rut-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates filled versions of the form
        and its inline formsets.
        """
        self.object = RUT.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ot_linea_form = OT_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ot_linea_form=ot_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = RUT.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ot_linea_form = OT_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and ot_linea_form.is_valid()):
            return self.form_valid(form, ot_linea_form)
        else:
            return self.form_invalid(form, ot_linea_form)

    def form_valid(self, form, ot_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Facturas and then redirects to a
        success page.
        """
        form.save()
        ot_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ot_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ot_linea_form=ot_linea_form))


class RUTList(ListView):
    model = RUT
    template_name = 'adm/rut_list.html'
    paginate_by = 30

    def get_queryset(self):
        # Por defecto los ordeno por codigo (desc)
        queryset = RUT.objects.all().order_by('-codigo')
        kwargs = {}
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                elif key == 'estado':
                    kwargs['%s__in' % key] = [x.split('(')[0] for x in vals]
                elif key == 'fecha_realizado':
                    kwargs['%s__in' % key] = [datetime.strptime(v, "%d/%m/%Y")
                           for v in vals]
                else:
                    kwargs['%s__in' % key] = vals
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(RUTList, self).get_context_data(**kwargs)
        ruts = RUT.objects.select_related()

        field_names = ['estado', 'codigo', 'fecha_realizado', 'deudor', 'solicitante',
                       'importe_bruto', 'importe_neto', 'fecha_envio_ut', 'firmada',
                       'fecha_envio_cc']
        field_labels = ['Estado', 'Nro. RUT', 'Fecha', 'UT Deudora', 'Area Solic.', 'Imp. Bruto',
                        'Imp. Neto', 'Fecha Envio a UT', 'Retorno Firmada', 'Fecha Envio a CC']

        # RUTs en borrador
        borrCount = len(ruts.filter(estado='borrador'))
        # RUTs pendientes
        penCount = len(ruts.filter(estado='pendiente'))
        # RUTs cobradas
        cobCount = len(ruts.filter(estado='cobrada'))
        # RUTs canceladas
        canCount = len(ruts.filter(estado='cancelada'))
        options = []
        estado_vals = ['borrador(' + str(borrCount) + ')',
                       'pendiente(' + str(penCount) + ')',
                       'cobrada(' + str(cobCount) + ')',
                       'cancelada(' + str(canCount) + ')']
        options.append(estado_vals)
        cod_vals = sorted(set([r.codigo for r in ruts]))
        options.append(cod_vals)
        fec1_vals = sorted(set([r.fecha_realizado.strftime("%d/%m/%Y")
                        for r in ruts if r.fecha_realizado is not None]))
        options.append(fec1_vals)
        deudor_vals = sorted(set([r.deudor for r in ruts if r.deudor]))
        options.append(deudor_vals)
        solicitante_vals = sorted(set([r.solicitante for r in ruts if r.solicitante]))
        options.append(solicitante_vals)
        importe_bruto_vals = sorted(set([r.importe_bruto for r in ruts if r.importe_bruto]))
        options.append(importe_bruto_vals)
        importe_neto_vals = sorted(set([r.importe_neto for r in ruts if r.importe_neto]))
        options.append(importe_neto_vals)
        fec2_vals = sorted(set([r.fecha_envio_ut.strftime("%d/%m/%Y")
                        for r in ruts if r.fecha_envio_ut is not None]))
        options.append(fec2_vals)
        fec3_vals = sorted(set([r.fecha_envio_cc.strftime("%d/%m/%Y")
                        for r in ruts if r.fecha_envio_cc is not None]))
        options.append(fec3_vals)
        firmada_vals = sorted(set([r.firmada for r in ruts if r.firmada]))
        options.append(firmada_vals)
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
        print "TIEMPO get_context_data: ", time() - t_inicial
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Cancelar' in request.POST:
            if request.user.has_perm('adm.cancel_rut'):
                rut_id = request.POST.get('Cancelar')
                rut_obj = RUT.objects.get(pk=rut_id)
                try:
                    rut_obj._toState_cancelada()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Finalizar' in request.POST:
            if request.user.has_perm('adm.finish_rut'):
                rut_id = request.POST.get('Finalizar')
                rut_obj = RUT.objects.get(pk=rut_id)
                try:
                    rut_obj._toState_cobrada()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_rut'):
                rut_id = request.POST.get('Eliminar')
                rut_obj = RUT.objects.get(pk=rut_id)
                rut_obj._delete()
                response_dict['redirect'] = reverse_lazy('adm:rut-list').strip()
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
            if presup.fecha_realizado + timedelta(days=21) < datetime.now().date():
                presup._toState_cancelado()

    def get_queryset(self):
        queryset = Presupuesto.objects.select_related().order_by('-codigo')
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

        presupuestos = Presupuesto.objects.select_related()
        turnos = [p.get_turno_activo() for p in presupuestos]

        presupuestos_by_page = context['object_list']
        turnos_by_page = [p.get_turno_activo() for p in presupuestos_by_page]

        context['tuple_paginated_list'] = list(zip(presupuestos_by_page, turnos_by_page))

        field_names = ['estado', 'codigo', 'usuario__nombre', 'usuario__nro_usuario',
                       'ofertatec__area',
                       'fecha_realizado',
                       'fecha_aceptado',
                       'fecha_instrumento',
                       'nro_recepcion']
        field_labels = ['Estado', 'Nro.', 'Usuario', 'Nro Usuario',
                        'Area',
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
        area_vals = sorted(set([t.area for t in turnos if t is not None]))
        options.append(area_vals)
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

