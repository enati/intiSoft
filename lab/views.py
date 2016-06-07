from .forms import TurnoForm, OfertaTec_LineaFormSet
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from .models import Turno, OfertaTec_Linea
from adm.models import OfertaTec, Presupuesto
from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
import json
from intiSoft.exception import StateError
from django.shortcuts import render
from django.utils.safestring import mark_safe
from labCalendar import WorkoutCalendar
from django.views.generic import View

thismonth = str(datetime.now().month)
thisyear = str(datetime.now().year)


class TurnoList(ListView):
    model = Turno
    paginate_by = 15
    lab = ''

    def _checkstate(self, queryset):
        """
        Chequeo los turnos a revisionar
        """
        for turno in queryset.exclude(revisionar=True):
            if turno._revisionar():
                turno.revisionar = True
            turno.save()

    def get_queryset(self):
        queryset = Turno.objects.all()
        if self.lab:
            queryset = queryset.filter(area=self.lab)
        kwargs = {}
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                elif key == 'estado':
                    kwargs['%s__in' % key] = [x.split('(')[0] for x in vals]
                elif key == 'fecha_inicio' or\
                     key == 'fecha_fin' or\
                     key == 'presupuesto__fecha_instrumento' or\
                     key == 'presupuesto__fecha_aceptado':
                    kwargs['%s__in' % key] = [datetime.strptime(v, "%d/%m/%Y")
                                              for v in vals]
                else:
                    kwargs['%s__in' % key] = vals
                    if key.find('ofertatec__') != -1:
                        ot_queryset = OfertaTec_Linea.objects.all()
                        ofertatec_lineas = ot_queryset.filter(**kwargs)
                        turnos = [ot.turno.id for ot in ofertatec_lineas]
                        queryset = queryset.filter(id__in=turnos)
                        return queryset
                if kwargs:
                    queryset = queryset.filter(**kwargs)
        self._checkstate(queryset)
        #self._checkrev(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TurnoList, self).get_context_data(**kwargs)
        turnos = Turno.objects.filter(area=self.lab)
        #turnos_by_page = context['turno_list']
        field_names = ['estado', 'presupuesto__usuario__nombre',
                       'fecha_inicio', 'fecha_fin',
                       'presupuesto__fecha_instrumento',
                       'presupuesto__fecha_aceptado',
                       #'ofertatec__codigo',
                       'presupuesto__codigo']
        field_labels = ['Estado', 'Usuario',
                        'Inicio', 'Finalizacion', 'Llegada del instrumento',
                        'Aceptacion Presupuesto',
                        #'Oferta Tec.',
                        'Nro. Presupuesto']
        # Turnos en espera
        espCount = len(turnos.filter(estado='en_espera'))
        # Turnos activos
        actCount = len(turnos.filter(estado='activo'))
        # Turnos finalizados
        finCount = len(turnos.filter(estado='finalizado'))
        # Turnos cancelados
        canCount = len(turnos.filter(estado='cancelado'))
        # Agregado para mostrar los campos ordenados
        options = []
        estado_vals = ['en_espera(' + str(espCount) + ')', 'activo(' + str(actCount) + ')',
                       'finalizado(' + str(finCount) + ')', 'cancelado(' + str(canCount) + ')']
        options.append(estado_vals)
        usuario_vals = set([t.presupuesto.usuario.nombre
                   for t in turnos if
                   t.presupuesto is not None and
                   t.presupuesto.usuario is not None])
        options.append(usuario_vals)
        finicio_vals = set([t.fecha_inicio.strftime("%d/%m/%Y") for t in turnos
                            if t.fecha_inicio is not None])
        options.append(finicio_vals)
        ffin_vals = set([t.fecha_fin.strftime("%d/%m/%Y") for t in turnos
                         if t.fecha_fin is not None])
        options.append(ffin_vals)
        finst_vals = set([t.presupuesto.fecha_instrumento.strftime("%d/%m/%Y")
                          for t in turnos if
                          t.presupuesto is not None and
                          t.presupuesto.fecha_instrumento is not None])
        options.append(finst_vals)
        facept_vals = set([t.presupuesto.fecha_aceptado.strftime("%d/%m/%Y")
                           for t in turnos if
                           t.presupuesto is not None and
                           t.presupuesto.fecha_aceptado is not None])
        options.append(facept_vals)
        # ofertatec es un campo many2one
        #ofertatec_list = [t.ofertatec_linea_set for t in turnos]
        #ofertatec_plist = reduce(lambda x, y: x + y,
                                 #[[t for t in o.get_queryset()] for o in ofertatec_list], [])
        #ofertatec_vals = set([o.ofertatec.codigo for o in ofertatec_plist])
        #options.append(ofertatec_vals)
        presup_vals = set([t.presupuesto.codigo for t in turnos if t.presupuesto])
        options.append(presup_vals)
        context['fields'] = list(zip(field_names, field_labels, options))
        # Chequeo los filtros seleccionados para conservar el estado de los
        # checkboxes
        checked_fields = []
        for key, vals in self.request.GET.lists():
            if key != 'order_by':
                checked_fields += ["%s_%s" % (v, key) for v in vals]
        context['checked_fields'] = checked_fields
        # Fecha de hoy para coloreo de filas
        context['today'] = datetime.now()
        # Para la paginacion
        if 'order_by' in self.request.GET:
            context['order_by'] = self.request.GET['order_by']
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Finalizar' in request.POST:
            if request.user.has_perm('lab.finish_turno_' + self.lab):
                turno_id = request.POST.get('Finalizar')
                turno_obj = Turno.objects.get(pk=turno_id)
                try:
                    turno_obj._toState_finalizado()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Cancelar' in request.POST:
            if request.user.has_perm('lab.cancel_turno_' + self.lab):
                turno_id = request.POST.get('Cancelar')
                turno_obj = Turno.objects.get(pk=turno_id)
                turno_obj._toState_cancelado()
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('lab.delete_turno_' + self.lab):
                turno_id = request.POST.get('Eliminar')
                turno_obj = Turno.objects.get(pk=turno_id)
                if not turno_obj._delete():
                    response_dict['ok'] = False
                    response_dict['msg'] = 'El turno no se puede eliminar ya que esta asociado a un presupuesto finalizado/cancelado'
                else:
                    response_dict['redirect'] = reverse("lab:%s-list" % self.lab)
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)


class LIAList(TurnoList):
    template_name = 'lab/LIA_list.html'
    lab = 'LIA'


class LIM1List(TurnoList):
    template_name = 'lab/LIM1_list.html'
    lab = 'LIM1'


class LIM2List(TurnoList):
    template_name = 'lab/LIM2_list.html'
    lab = 'LIM2'


class LIM3List(TurnoList):
    template_name = 'lab/LIM3_list.html'
    lab = 'LIM3'


class LIM6List(TurnoList):
    template_name = 'lab/LIM6_list.html'
    lab = 'LIM6'


class EXTList(TurnoList):
    template_name = 'lab/EXT_list.html'
    lab = 'EXT'


class SISList(TurnoList):
    template_name = 'lab/SIS_list.html'
    lab = 'SIS'


class DESList(TurnoList):
    template_name = 'lab/DES_list.html'
    lab = 'DES'


class TurnoCreate(CreateView):
    model = Turno
    form_class = TurnoForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ofertatec_linea_form = OfertaTec_LineaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ofertatec_linea_form=ofertatec_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ofertatec_linea_form = OfertaTec_LineaFormSet(self.request.POST)
        if (form.is_valid() and ofertatec_linea_form.is_valid()):
            return self.form_valid(form, ofertatec_linea_form)
        else:
            return self.form_invalid(form, ofertatec_linea_form)

    def form_valid(self, form, ofertatec_linea_form):
        """
        Called if all forms are valid. Creates a Turno instance along with
        associated OfertaTec_Lineas and then redirects to a
        success page.
        """
        self.object = form.save()
        ofertatec_linea_form.instance = self.object
        ofertatec_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ofertatec_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ofertatec_linea_form=ofertatec_linea_form))

    def get_context_data(self, **kwargs):
        context = super(TurnoCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        return context


class LIACreate(TurnoCreate):
    template_name = 'lab/LIA_form.html'

    @method_decorator(permission_required('lab.add_turno_LIA',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIACreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIA-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIA'}


class LIM1Create(TurnoCreate):
    template_name = 'lab/LIM1_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM1',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM1Create, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIM1-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM1'}


class LIM2Create(TurnoCreate):
    template_name = 'lab/LIM2_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM2',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM2Create, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIM2-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM2'}


class LIM3Create(TurnoCreate):
    template_name = 'lab/LIM3_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM3',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM3Create, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIM3-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM3'}


class LIM6Create(TurnoCreate):
    template_name = 'lab/LIM6_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM6',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM6Create, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIM6-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM6'}


class EXTCreate(TurnoCreate):
    template_name = 'lab/EXT_form.html'

    @method_decorator(permission_required('lab.add_turno_EXT',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(EXTCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:EXT-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'EXT'}


class SISCreate(TurnoCreate):
    template_name = 'lab/SIS_form.html'

    @method_decorator(permission_required('lab.add_turno_SIS',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(SISCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:SIS-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'SIS'}


class DESCreate(TurnoCreate):
    template_name = 'lab/DES_form.html'

    @method_decorator(permission_required('lab.add_turno_DES',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(DESCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:DES-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'DES'}


class TurnoUpdate(UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates filled versions of the form
        and its inline formsets.
        """
        self.object = Turno.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ofertatec_linea_form = OfertaTec_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ofertatec_linea_form=ofertatec_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = Turno.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ofertatec_linea_form = OfertaTec_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and ofertatec_linea_form.is_valid()):
            return self.form_valid(form, ofertatec_linea_form)
        else:
            return self.form_invalid(form, ofertatec_linea_form)

    def form_valid(self, form, ofertatec_linea_form):
        """
        Called if all forms are valid. Creates a Turno instance along with
        associated OfertaTec_Lineas and then redirects to a
        success page.
        """
        form.save()
        ofertatec_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ofertatec_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ofertatec_linea_form=ofertatec_linea_form))

    def get_context_data(self, **kwargs):
        context = super(TurnoUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        return context


class LIAUpdate(TurnoUpdate):
    template_name = 'lab/LIA_form.html'

    @method_decorator(permission_required('lab.change_turno_LIA',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIAUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIA-update', kwargs={'pk': self.object.id})


class LIM1Update(TurnoUpdate):
    template_name = 'lab/LIM1_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM1',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM1Update, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIM1-update', kwargs={'pk': self.object.id})


class LIM2Update(TurnoUpdate):
    template_name = 'lab/LIM2_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM2',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM2Update, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIM2-update', kwargs={'pk': self.object.id})


class LIM3Update(TurnoUpdate):
    template_name = 'lab/LIM3_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM3',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM3Update, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIM3-update', kwargs={'pk': self.object.id})


class LIM6Update(TurnoUpdate):
    template_name = 'lab/LIM6_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM6',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM6Update, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:LIM6-update', kwargs={'pk': self.object.id})


class EXTUpdate(TurnoUpdate):
    template_name = 'lab/EXT_form.html'

    @method_decorator(permission_required('lab.change_turno_EXT',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(EXTUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:EXT-update', kwargs={'pk': self.object.id})


class SISUpdate(TurnoUpdate):
    template_name = 'lab/SIS_form.html'

    @method_decorator(permission_required('lab.change_turno_SIS',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(SISUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:SIS-update', kwargs={'pk': self.object.id})


class DESUpdate(TurnoUpdate):
    template_name = 'lab/DES_form.html'

    @method_decorator(permission_required('lab.change_turno_DES',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(DESUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('lab:DES-update', kwargs={'pk': self.object.id})


class TurnoDelete(DeleteView):
    model = Turno
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(TurnoDelete, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'cancelar' in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(TurnoDelete, self).post(request, *args, **kwargs)


def get_price(request, *args, **kwargs):
    try:
        ot_id = request.GET['ot_id']
        ot_obj = OfertaTec.objects.get(pk=ot_id)
        data = {'precio': ot_obj.precio,
                'precio_total': ot_obj.precio,
                'detalle': ot_obj.detalle,
                'tipo_servicio': ot_obj.tipo_servicio}
    except:
        data = {}
    return HttpResponse(json.dumps(data), content_type="text/json")


def get_presup(request, *args, **kwargs):
    data = {}
    try:
        presup_id = request.GET['presup_id']
        presup_obj = Presupuesto.objects.get(pk=presup_id)
        data['fecha_solicitado'] = presup_obj.fecha_solicitado.strftime("%d/%m/%Y")
        data['fecha_realizado'] = presup_obj.fecha_realizado.strftime("%d/%m/%Y") if presup_obj.fecha_realizado else ''
        data['fecha_aceptado'] = presup_obj.fecha_aceptado.strftime("%d/%m/%Y") if presup_obj.fecha_aceptado else ''
        data['usuario'] = presup_obj.usuario.nombre
        data['mail'] = presup_obj.usuario.mail
        data['rubro'] = presup_obj.usuario.rubro
    except:
        data = {}
    return HttpResponse(json.dumps(data), content_type="text/json")


class LIADelete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_LIA',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIADelete, self).dispatch(request, *args, **kwargs)


class LIM1Delete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_LIM1',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM1Delete, self).dispatch(request, *args, **kwargs)


class LIM2Delete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_LIM2',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM2Delete, self).dispatch(request, *args, **kwargs)


class LIM3Delete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_LIM3',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM3Delete, self).dispatch(request, *args, **kwargs)


class LIM6Delete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_LIM6',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM6Delete, self).dispatch(request, *args, **kwargs)


class EXTDelete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_EXT',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(EXTDelete, self).dispatch(request, *args, **kwargs)


class SISDelete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_SIS',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(SISDelete, self).dispatch(request, *args, **kwargs)


class DESDelete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_DES',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(DESDelete, self).dispatch(request, *args, **kwargs)


class CalendarView(View):
    template_name = 'lab/calendar.html'
    lab = ''

    def get(self, request, year=thisyear, month=thismonth):
        if len(month) == 1:
            month = '0' + str(month)
        date = year + '-' + month
        turnos = Turno.objects.order_by('fecha_inicio').filter(fecha_inicio__contains=date,
                                                               estado__in=['borrador', 'activo'],
                                                               area=self.lab)
        cal = WorkoutCalendar(turnos, self.lab).formatmonth(int(year), int(month))
        return render(request, self.template_name, {'user': request.user, 'calendar': mark_safe(cal)})
        return HttpResponse('result')


class LIACalendarView(CalendarView):
    template_name = 'lab/LIA_calendar.html'
    lab = 'LIA'


class LIM1CalendarView(CalendarView):
    template_name = 'lab/LIM1_calendar.html'
    lab = 'LIM1'


class LIM2CalendarView(CalendarView):
    template_name = 'lab/LIM2_calendar.html'
    lab = 'LIM2'


class LIM3CalendarView(CalendarView):
    template_name = 'lab/LIM3_calendar.html'
    lab = 'LIM3'


class LIM6CalendarView(CalendarView):
    template_name = 'lab/LIM6_calendar.html'
    lab = 'LIM6'


class EXTCalendarView(CalendarView):
    template_name = 'lab/EXT_calendar.html'
    lab = 'EXT'


class SISCalendarView(CalendarView):
    template_name = 'lab/SIS_calendar.html'
    lab = 'SIS'


class DESCalendarView(CalendarView):
    template_name = 'lab/DES_calendar.html'
    lab = 'DES'

