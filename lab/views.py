from .forms import TurnoForm, OfertaTec_LineaFormSet
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from .models import Turno, OfertaTec_Linea
from adm.models import OfertaTec, Presupuesto, OT, SI, PDT
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
from reversion.models import Version
from reversion import RegistrationError
import reversion
import re
from django.db.models import Q
import operator

#===========================================
#========== VARIABLES GLOBALES =============
#===========================================

thismonth = str(datetime.now().month)
thisyear = str(datetime.now().year)

back_url_lia = reverse_lazy('lab:LIA-list')
back_url_lim1 = reverse_lazy('lab:LIM1-list')
back_url_lim2 = reverse_lazy('lab:LIM2-list')
back_url_lim3 = reverse_lazy('lab:LIM3-list')
back_url_lim4 = reverse_lazy('lab:LIM4-list')
back_url_lim5 = reverse_lazy('lab:LIM5-list')
back_url_lim6 = reverse_lazy('lab:LIM6-list')
back_url_ext = reverse_lazy('lab:EXT-list')
back_url_sis = reverse_lazy('lab:SIS-list')
back_url_des = reverse_lazy('lab:DES-list')
back_url_cal = reverse_lazy('lab:CAL-list')
back_url_mec = reverse_lazy('lab:MEC-list')
back_url_ml = reverse_lazy('lab:ML-list')


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
        queryset = Turno.objects.all().order_by('-fecha_inicio')
        if self.lab:
            queryset = queryset.filter(area=self.lab)
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    if vals[0] in ['usuario', '-usuario']:
                        queryset = queryset.extra(select={"usuario": "COALESCE('presupuesto__usuario__nombre', 'si__solicitante') as usuario"}, order_by=[vals[0]])
                    else:
                        queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        # Busco solo por fecha de inicio del turno
                        if re.match(r'^\d{2}\/\d{2}\/\d{4}-\d{2}\/\d{2}\/\d{4}$', arg):
                            start_date, end_date = map(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d'), arg.split("-"))
                            QList.append(Q(fecha_inicio__range=['%s' % start_date, '%s' % end_date]))
                            continue
                        QList.append(Q(estado__icontains="%s" % arg) |
                                    Q(presupuesto__usuario__nombre__icontains="%s" % arg) |
                                    Q(presupuesto__codigo__contains="%s" % arg) |
                                    Q(presupuesto__ot__codigo__contains="%s" % arg) |
                                    Q(si__solicitante__icontains="%s" % arg) |
                                    Q(si__codigo__contains="%s" % arg) |
                                    Q(presupuesto__sot__codigo__contains="%s" % arg) |
                                    Q(presupuesto__rut__codigo__contains="%s" % arg))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        self._checkstate(queryset)
        #self._checkrev(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TurnoList, self).get_context_data(**kwargs)
        field_names = ['estado', 'usuario',
                       'fecha_inicio', 'fecha_fin',
                       'presupuesto__instrumento__fecha_llegada',
                       'presupuesto__fecha_aceptado',
                       'presupuesto__codigo', 'presupuesto__ot__codigo', 'presupuesto__sot__codigo',
                       'presupuesto__rut__codigo', 'presupuesto__si__codigo']
        field_labels = ['Estado', 'Usuario',
                        'Inicio', 'Finalizacion', 'Llegada del instrumento',
                        'Aceptacion Presupuesto',
                        'Nro. Presupuesto', 'Nro.  OT', 'Nro. SOT', 'Nro. RUT', 'Nro. SI']
        context['fields'] = list(zip(field_names, field_labels))
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
                obs = request.POST.get('observations', '')
                turno_obj._toState_cancelado(obs)
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('lab.delete_turno_' + self.lab):
                turno_id = request.POST.get('Eliminar')
                turno_obj = Turno.objects.get(pk=turno_id)
                try:
                    turno_obj._delete()
                    response_dict['redirect'] = reverse("lab:%s-list" % self.lab)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
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


class LIM4List(TurnoList):
    template_name = 'lab/LIM4_list.html'
    lab = 'LIM4'


class LIM5List(TurnoList):
    template_name = 'lab/LIM5_list.html'
    lab = 'LIM5'


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


class CALList(TurnoList):
    template_name = 'lab/CAL_list.html'
    lab = 'CAL'


class MECList(TurnoList):
    template_name = 'lab/MEC_list.html'
    lab = 'MEC'


class MLList(TurnoList):
    template_name = 'lab/ML_list.html'
    lab = 'ML'


class TurnoCreate(CreateView):
    model = Turno
    form_class = TurnoForm
    lab = ''

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
    lab = 'LIA'

    @method_decorator(permission_required('lab.add_turno_LIA',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIA-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lia
                back_url_lia = http_referer
        return super(LIACreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIACreate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lia
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIA-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIA'}


class LIM1Create(TurnoCreate):
    template_name = 'lab/LIM1_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM1',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM1-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim1
                back_url_lim1 = http_referer
        return super(LIM1Create, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM1Create, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim1
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM1-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM1'}


class LIM2Create(TurnoCreate):
    template_name = 'lab/LIM2_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM2',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM2-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim2
                back_url_lim2 = http_referer
        return super(LIM2Create, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM2Create, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim2
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM2-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM2'}


class LIM3Create(TurnoCreate):
    template_name = 'lab/LIM3_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM3',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM3-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim3
                back_url_lim3 = http_referer
        return super(LIM3Create, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM3Create, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim3
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM3-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM3'}


class LIM4Create(TurnoCreate):
    template_name = 'lab/LIM4_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM4',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM4-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim4
                back_url_lim4 = http_referer
        return super(LIM4Create, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM4Create, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim4
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM4-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM4'}


class LIM5Create(TurnoCreate):
    template_name = 'lab/LIM5_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM5',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM5-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim5
                back_url_lim5 = http_referer
        return super(LIM5Create, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM5Create, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim5
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM5-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM5'}


class LIM6Create(TurnoCreate):
    template_name = 'lab/LIM6_form.html'

    @method_decorator(permission_required('lab.add_turno_LIM6',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM6-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim6
                back_url_lim6 = http_referer
        return super(LIM6Create, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM6Create, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim6
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM6-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'LIM6'}


class EXTCreate(TurnoCreate):
    template_name = 'lab/EXT_form.html'

    @method_decorator(permission_required('lab.add_turno_EXT',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:EXT-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_ext
                back_url_ext = http_referer
        return super(EXTCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EXTCreate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_ext
        return context

    def get_success_url(self):
        return reverse_lazy('lab:EXT-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'EXT'}


class SISCreate(TurnoCreate):
    template_name = 'lab/SIS_form.html'

    @method_decorator(permission_required('lab.add_turno_SIS',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:SIS-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_sis
                back_url_sis = http_referer
        return super(SISCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SISCreate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_sis
        return context

    def get_success_url(self):
        return reverse_lazy('lab:SIS-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'SIS'}


class DESCreate(TurnoCreate):
    template_name = 'lab/DES_form.html'

    @method_decorator(permission_required('lab.add_turno_DES',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:DES-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_des
                back_url_des = http_referer
        return super(DESCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DESCreate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_des
        return context

    def get_success_url(self):
        return reverse_lazy('lab:DES-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'DES'}


class CALCreate(TurnoCreate):
    template_name = 'lab/CAL_form.html'

    @method_decorator(permission_required('lab.add_turno_CAL',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:CAL-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_cal
                back_url_cal = http_referer
        return super(CALCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CALCreate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_cal
        return context

    def get_success_url(self):
        return reverse_lazy('lab:CAL-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'CAL'}


class MECCreate(TurnoCreate):
    template_name = 'lab/MEC_form.html'

    @method_decorator(permission_required('lab.add_turno_MEC',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:MEC-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_mec
                back_url_mec = http_referer
        return super(MECCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MECCreate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_mec
        return context

    def get_success_url(self):
        return reverse_lazy('lab:MEC-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'MEC'}


class MLCreate(TurnoCreate):
    template_name = 'lab/ML_form.html'

    @method_decorator(permission_required('lab.add_turno_ML',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:ML-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_ml
                back_url_ml = http_referer
        return super(MLCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MLCreate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_ml
        return context

    def get_success_url(self):
        return reverse_lazy('lab:ML-update', kwargs={'pk': self.object.id})

    def get_initial(self):
        return {'area': 'ML'}


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
        if form.isRev:
            ofertatec_linea_form = OfertaTec_LineaFormSet(instance=self.object, revision=True)
        else:
            ofertatec_linea_form = OfertaTec_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ofertatec_linea_form=ofertatec_linea_form))

    def get_form_kwargs(self):
        kwargs = super(TurnoUpdate, self).get_form_kwargs()
        if self.request.GET.get('revision', False):
            kwargs.update({'revision': 1})
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = Turno.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.isRev:
            ofertatec_linea_form = OfertaTec_LineaFormSet(self.request.POST, instance=self.object, revision=True)
        else:
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
        context['revision'] = self.request.GET.get('revision', False)

        # Revisionado
        turnoVers = Version.objects.get_for_object(self.object).exclude(revision__comment__contains='P_')
        presupVersByRevision = []
        usuarioVersByRevision = []
        otLineaVersByRevision = []
        siLineaVersByRevision = []
        if turnoVers:
            for tv in turnoVers:
                revId = tv.revision.id
                # Todos los objetos versionados en la revision revId
                objectsVersiones = Version.objects.filter(revision=revId)
                # Todos los presupuestos versionados en la revision revId
                pv = objectsVersiones.filter(content_type__model='presupuesto')
                presupVersByRevision.append(pv)
                # Todos los usuarios versionados en la revision revId
                uv = objectsVersiones.filter(content_type__model='usuario')
                usuarioVersByRevision.append(uv)
                # Todos las lineas de ot versionados en la revision revId
                ot = objectsVersiones.filter(content_type__model='ofertatec_linea').order_by('object_id')
                otLineaVersByRevision.append(ot)
                # Todass las SI versionadas en la revision revId
                si = objectsVersiones.filter(content_type__model='si').order_by('object_id')
                siLineaVersByRevision.append(si)

        context['turnoVersions'] = zip(turnoVers, presupVersByRevision, usuarioVersByRevision,
                                       otLineaVersByRevision, siLineaVersByRevision)
        return context


def createRevision(request, *args, **kwargs):
    try:
        # Declare a revision block.
        with reversion.create_revision():
            # Save a new model instance.
            obj_pk = kwargs.get('pk')
            obj = Turno.objects.get(pk=obj_pk)
            obj.save()

            actualRevNumber = 'T_REV' + str(obj.nro_revision)

            # Store some meta-information.
            reversion.set_user(request.user)
            reversion.set_comment(actualRevNumber)
        # Actualizo el turno
        obj.nro_revision += 1
        obj.revisionar = False
        obj.save()
        # Aviso al presupuesto que hay que revisionar (si hay)
        if obj.presupuesto:
            obj.presupuesto.revisionar = True
            obj.presupuesto.save()
        obj.write_activity_log("Revision #%d creada" % obj.nro_revision)
        return JsonResponse({'ok': 'ok'})
    except RegistrationError as e:
        raise e


def rollBackRevision(request, *args, **kwargs):
    obj_pk = kwargs.get('pk')
    obj = Turno.objects.get(pk=obj_pk)
    redirect = reverse_lazy('lab:' + obj.area + '-update', kwargs={'pk': kwargs['pk']}).strip()
    try:
        turnoVers = Version.objects.get_for_object(obj)
        if turnoVers:
            ultRev = turnoVers.first()
            ultRev.revision.revert(True)
            ultRev.revision.delete()
        self.write_activity_log("Presupuesto #%s eliminado" % self.codigo)

        obj.write_activity_log("Revision #%d eliminada" % obj.nro_revision)
        return JsonResponse({'ok': 'ok', 'redirect': redirect})
    except:
        return JsonResponse({'err': 'err', 'redirect': redirect})


class LIAUpdate(TurnoUpdate):
    template_name = 'lab/LIA_form.html'

    @method_decorator(permission_required('lab.change_turno_LIA',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIA-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lia
                back_url_lia = http_referer
        return super(LIAUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIAUpdate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lia
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIA-update', kwargs={'pk': self.object.id})


class LIM1Update(TurnoUpdate):
    template_name = 'lab/LIM1_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM1',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM1-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim1
                back_url_lim1 = http_referer
        return super(LIM1Update, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM1Update, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim1
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM1-update', kwargs={'pk': self.object.id})


class LIM2Update(TurnoUpdate):
    template_name = 'lab/LIM2_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM2',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM2-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim2
                back_url_lim2 = http_referer
        return super(LIM2Update, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM2Update, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim2
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM2-update', kwargs={'pk': self.object.id})


class LIM3Update(TurnoUpdate):
    template_name = 'lab/LIM3_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM3',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM3-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim3
                back_url_lim3 = http_referer
        return super(LIM3Update, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM3Update, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim3
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM3-update', kwargs={'pk': self.object.id})


class LIM4Update(TurnoUpdate):
    template_name = 'lab/LIM4_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM4',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM4-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim4
                back_url_lim4 = http_referer
        return super(LIM4Update, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM4Update, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim4
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM4-update', kwargs={'pk': self.object.id})


class LIM5Update(TurnoUpdate):
    template_name = 'lab/LIM5_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM5',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM5-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim5
                back_url_lim5 = http_referer
        return super(LIM5Update, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM5Update, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim5
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM5-update', kwargs={'pk': self.object.id})


class LIM6Update(TurnoUpdate):
    template_name = 'lab/LIM6_form.html'

    @method_decorator(permission_required('lab.change_turno_LIM6',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:LIM6-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_lim6
                back_url_lim6 = http_referer
        return super(LIM6Update, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LIM6Update, self).get_context_data(**kwargs)
        context['back_url'] = back_url_lim6
        return context

    def get_success_url(self):
        return reverse_lazy('lab:LIM6-update', kwargs={'pk': self.object.id})


class EXTUpdate(TurnoUpdate):
    template_name = 'lab/EXT_form.html'

    @method_decorator(permission_required('lab.change_turno_EXT',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:EXT-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_ext
                back_url_ext = http_referer
        return super(EXTUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EXTUpdate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_ext
        return context

    def get_success_url(self):
        return reverse_lazy('lab:EXT-update', kwargs={'pk': self.object.id})


class SISUpdate(TurnoUpdate):
    template_name = 'lab/SIS_form.html'

    @method_decorator(permission_required('lab.change_turno_SIS',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:SIS-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_sis
                back_url_sis = http_referer
        return super(SISUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SISUpdate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_sis
        return context

    def get_success_url(self):
        return reverse_lazy('lab:SIS-update', kwargs={'pk': self.object.id})


class DESUpdate(TurnoUpdate):
    template_name = 'lab/DES_form.html'

    @method_decorator(permission_required('lab.change_turno_DES',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:DES-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_des
                back_url_des = http_referer
        return super(DESUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DESUpdate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_des
        return context

    def get_success_url(self):
        return reverse_lazy('lab:DES-update', kwargs={'pk': self.object.id})


class CALUpdate(TurnoUpdate):
    template_name = 'lab/CAL_form.html'

    @method_decorator(permission_required('lab.change_turno_CAL',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:CAL-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_cal
                back_url_cal = http_referer
        return super(CALUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CALUpdate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_cal
        return context

    def get_success_url(self):
        return reverse_lazy('lab:CAL-update', kwargs={'pk': self.object.id})


class MECUpdate(TurnoUpdate):
    template_name = 'lab/MEC_form.html'

    @method_decorator(permission_required('lab.change_turno_MEC',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:MEC-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_mec
                back_url_mec = http_referer
        return super(MECUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MECUpdate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_mec
        return context

    def get_success_url(self):
        return reverse_lazy('lab:MEC-update', kwargs={'pk': self.object.id})


class MLUpdate(TurnoUpdate):
    template_name = 'lab/ML_form.html'

    @method_decorator(permission_required('lab.change_turno_ML',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('lab:ML-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_ml
                back_url_ml = http_referer
        return super(MLUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MLUpdate, self).get_context_data(**kwargs)
        context['back_url'] = back_url_ml
        return context

    def get_success_url(self):
        return reverse_lazy('lab:ML-update', kwargs={'pk': self.object.id})


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
        data = {'codigo': ot_obj.codigo,
                'precio': ot_obj.precio,
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
        turnos_activos = presup_obj.get_turnos_activos()
        data['pdt'] = presup_obj.pdt.nombre if presup_obj.pdt else '---'
        data['fecha_solicitado'] = presup_obj.fecha_solicitado.strftime("%d/%m/%Y")
        data['fecha_realizado'] = presup_obj.fecha_realizado.strftime("%d/%m/%Y") if presup_obj.fecha_realizado else ''
        data['fecha_aceptado'] = presup_obj.fecha_aceptado.strftime("%d/%m/%Y") if presup_obj.fecha_aceptado else ''
        data['usuario'] = presup_obj.usuario.nombre
        data['mail'] = presup_obj.usuario.mail
        data['rubro'] = presup_obj.usuario.rubro
        data['ofertatec'] = []
        turnos_activos = turnos_activos.order_by('-fecha_fin')
        if turnos_activos:
            data['area'] = '-'.join([t.area for t in turnos_activos])
            data['solicitante'] = turnos_activos[0].area
            if turnos_activos[0].fecha_fin:
                data['fecha_turno'] = turnos_activos[0].fecha_fin.strftime("%d/%m/%Y")
            for turno in turnos_activos:
                for ot in turno.ofertatec_linea_set.all():
                    # Puede ser que la referencia al obj no exista mas
                    ot_object_id = None
                    try:
                        ot_object_id = ot.ofertatec.id
                    except:
                        pass
                    data['ofertatec'].append({'ofertatec': ot_object_id,
                                              'codigo': ot.codigo, 'tipo_servicio': ot.tipo_servicio,
                                              'cantidad': ot.cantidad, 'cant_horas': ot.cant_horas,
                                              'precio': ot.precio, 'precio_total': ot.precio_total,
                                              'detalle': ot.detalle, 'observaciones': ot.observaciones})

    except:
        data = {}
    return HttpResponse(json.dumps(data), content_type="text/json")


def get_si(request, *args, **kwargs):
    data = {}
    try:
        si_id = request.GET['si_id']
        si_obj = SI.objects.get(pk=si_id)
        data['solicitante'] = si_obj.solicitante
        data['fecha_realizado'] = si_obj.fecha_realizado.strftime("%d/%m/%Y") if si_obj.fecha_realizado else ''
        data['fecha_prevista'] = si_obj.fecha_prevista.strftime("%d/%m/%Y") if si_obj.fecha_prevista else ''
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


class LIM4Delete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_LIM4',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM4Delete, self).dispatch(request, *args, **kwargs)


class LIM5Delete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_LIM5',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(LIM5Delete, self).dispatch(request, *args, **kwargs)


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


class CALDelete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_CAL',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(CALDelete, self).dispatch(request, *args, **kwargs)


class MECDelete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_MEC',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(MECDelete, self).dispatch(request, *args, **kwargs)


class MLDelete(TurnoDelete):
    success_url = reverse_lazy('lab:turnos-list')

    @method_decorator(permission_required('lab.delete_turno_ML',
                      raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        return super(MLDelete, self).dispatch(request, *args, **kwargs)


class CalendarView(View):
    template_name = 'lab/calendar.html'
    lab = ''

    def get(self, request, year=thisyear, month=thismonth):
        if len(month) == 1:
            month = '0' + str(month)
        date = year + '-' + month
        turnos = Turno.objects.order_by('fecha_inicio').filter(fecha_inicio__contains=date,
                                                               estado__in=['en_espera', 'activo'],
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


class LIM4CalendarView(CalendarView):
    template_name = 'lab/LIM4_calendar.html'
    lab = 'LIM4'


class LIM5CalendarView(CalendarView):
    template_name = 'lab/LIM5_calendar.html'
    lab = 'LIM5'


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


class CALCalendarView(CalendarView):
    template_name = 'lab/CAL_calendar.html'
    lab = 'CAL'


class MECCalendarView(CalendarView):
    template_name = 'lab/MEC_calendar.html'
    lab = 'MEC'


class MLCalendarView(CalendarView):
    template_name = 'lab/ML_calendar.html'
    lab = 'ML'

