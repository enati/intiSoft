# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
import lab
from .models import Presupuesto, OfertaTec, Usuario, OT, OTML, SOT, RUT, SI, Factura, Recibo, Remito, PDT, Contacto
from lab.models import OfertaTec_Linea
from .forms import PresupuestoForm, OfertaTecForm, UsuarioForm, OTForm, OTMLForm, SIForm, \
    Factura_LineaFormSet, OT_LineaFormSet, Remito_LineaFormSet, SOTForm, RUTForm, \
    Tarea_LineaFormSet, Instrumento_LineaFormSet, PDTForm, Contacto_LineaFormSet, ContactoForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from .utils import genWord, genSOT, genRUT, genSI
from django.http import JsonResponse
import json
from intiSoft.exception import StateError
from reversion.models import Version
import reversion
from time import time
import re
from django.db.models import Q
import operator
from django.core import serializers
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import xlwt
from django.utils.html import escape, escapejs

#===========================================
#========== VARIABLES GLOBALES =============
#===========================================
back_url_presupuesto = reverse_lazy('adm:presup-list')
back_url_ot = reverse_lazy('adm:ot-list')
back_url_otml = reverse_lazy('adm:otml-list')
back_url_usuario = reverse_lazy('adm:usuarios-list')
back_url_ofertatec = reverse_lazy('adm:ofertatec-list')
back_url_sot = reverse_lazy('adm:sot-list')
back_url_rut = reverse_lazy('adm:rut-list')
back_url_si = reverse_lazy('adm:si-list')
back_url_pdt = reverse_lazy('adm:pdt-list')

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


def load_contactos(request):
    usuario_id = int(request.GET.get('usuario'))
    contactos = Contacto.objects.filter(usuario=usuario_id)
    return render(request, 'adm/contacto_select.html', {'contactos': contactos})


def pdtToXls(request, *args, **kwargs):
    pdt_id = kwargs.get('pk')
    pdt_obj = PDT.objects.get(id=pdt_id)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PDT_%s.xls"' % pdt_obj.codigo

    wb = xlwt.Workbook(encoding='utf-8')

    # Estilos
    styleH1 = xlwt.XFStyle()
    styleH1.font.height = 12 * 20
    styleH1.alignment.wrap = 1
    styleH1.aligment = xlwt.Alignment()
    styleH1.alignment.horz = styleH1.alignment.HORZ_CENTER
    styleH1.alignment.vert = styleH1.alignment.VERT_CENTER
    styleH1.font.bold = 1

    styleH2 = xlwt.XFStyle()
    styleH2.font.height = 10 * 20
    styleH2.alignment.wrap = 1
    styleH2.aligment = xlwt.Alignment()
    styleH2.alignment.horz = styleH2.alignment.HORZ_CENTER
    styleH2.alignment.vert = styleH2.alignment.VERT_CENTER
    styleH2.font.bold = 1

    tableStyle1 = xlwt.easyxf('font: bold 1; borders: left medium, top medium, right medium, bottom medium; alignment: horiz centre')
    tableStyle2 = xlwt.easyxf('borders: left thin, top thin, right thin, bottom thin; alignment: horiz centre')

    ws_ot = wb.add_sheet('OT')
    row_num = 0

    ws_ot.write_merge(row_num, row_num + 1, 0, 4, pdt_obj.nombre, styleH1)
    row_num += 3

    columns = ['Número', 'Servicios', 'Importe Bruto', 'Importe Neto', 'Facturado']

    ws_ot.write_merge(row_num, row_num, 0, 4, 'Resumen de OTs', styleH2)
    row_num += 2
    for col_num in range(len(columns)):
        ws_ot.write(row_num, col_num, columns[col_num], tableStyle1)

    row_num += 1
    for i, ot in enumerate(pdt_obj.ot_set.all()):
        ws_ot.write(row_num, 0, ot.codigo, tableStyle2)
        ws_ot.write(row_num, 1, ot.get_servicios(), tableStyle2)
        ws_ot.write(row_num, 2, "$" + str(ot.importe_bruto), tableStyle2)
        ws_ot.write(row_num, 3, "$" + str(ot.importe_neto), tableStyle2)
        ws_ot.write(row_num, 4, "$" + str(ot.get_facturacion()), tableStyle2)
        row_num += 1

    ws_otml = wb.add_sheet('OTML')
    row_num = 0

    ws_otml.write_merge(row_num, row_num + 1, 0, 4, pdt_obj.nombre, styleH1)
    row_num += 3

    ws_otml.write_merge(row_num, row_num, 0, 4, 'Resumen de OTMLs', styleH2)
    row_num += 2
    for col_num in range(len(columns)):
        ws_otml.write(row_num, col_num, columns[col_num], tableStyle1)

    row_num += 1
    for otml in pdt_obj.otml_set.all():
        ws_otml.write(row_num, 0, otml.codigo, tableStyle2)
        ws_otml.write(row_num, 1, otml.get_servicios(), tableStyle2)
        ws_otml.write(row_num, 2, otml.importe_bruto, tableStyle2)
        ws_otml.write(row_num, 3, otml.importe_neto, tableStyle2)
        ws_otml.write(row_num, 4, otml.get_facturacion(), tableStyle2)
        row_num += 1

    ws_sot = wb.add_sheet('SOT')
    row_num = 0

    ws_sot.write_merge(row_num, row_num + 1, 0, 4, pdt_obj.nombre, styleH1)
    row_num += 3

    ws_sot.write_merge(row_num, row_num, 0, 4, 'Resumen de SOTs', styleH2)
    row_num += 2
    for col_num in range(len(columns)):
        ws_sot.write(row_num, col_num, columns[col_num], tableStyle1)

    row_num += 1
    for sot in pdt_obj.sot_set.all():
        ws_sot.write(row_num, 0, sot.codigo, tableStyle2)
        ws_sot.write(row_num, 1, sot.get_servicios(), tableStyle2)
        ws_sot.write(row_num, 2, sot.importe_bruto, tableStyle2)
        ws_sot.write(row_num, 3, sot.importe_neto, tableStyle2)
        ws_sot.write(row_num, 4, sot.get_facturacion(), tableStyle2)
        row_num += 1

    ws_rut = wb.add_sheet('RUT')
    row_num = 0

    ws_rut.write_merge(row_num, row_num + 1, 0, 4, pdt_obj.nombre, styleH1)
    row_num += 3

    ws_rut.write_merge(row_num, row_num, 0, 4, 'Resumen de RUTs', styleH2)
    row_num += 2
    for col_num in range(len(columns)):
        ws_rut.write(row_num, col_num, columns[col_num], tableStyle1)

    row_num += 1
    for rut in pdt_obj.rut_set.all():
        ws_rut.write(row_num, 0, rut.codigo, tableStyle2)
        ws_rut.write(row_num, 1, rut.get_servicios(), tableStyle2)
        ws_rut.write(row_num, 2, rut.importe_bruto, tableStyle2)
        ws_rut.write(row_num, 3, rut.importe_neto, tableStyle2)
        ws_rut.write(row_num, 4, rut.get_facturacion(), tableStyle2)
        row_num += 1

    wb.save(response)
    return response


def pdtToPdf(request, *args, **kwargs):
    pdt_id = kwargs.get('pk')
    pdt_obj = PDT.objects.get(id=pdt_id)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PDT_%s.pdf"' % pdt_obj.codigo

    width, height = A4
    styleH = ParagraphStyle(name='Normal',
                            alignment=TA_CENTER,
                            spaceAfter=20,
                            fontSize=20)
    styleN = ParagraphStyle(name='Normal',
                            alignment=TA_CENTER)
    headerStyle = ParagraphStyle(name='Normal',
                                 fontSize=6)
    tableStyle = TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                              ('BOX', (0, 0), (-1, -1), 1, colors.black),
                              ('LINEABOVE', (0, 1), (4, 1), 1, colors.black)])
    story = []

    # Create the PDF object, using the response object as its "file."
    canvas = Canvas(response, pagesize=A4)

    frame = Frame(0, 0, width, height, leftPadding=10, bottomPadding=50,
                  rightPadding=10, topPadding=50, id=1, showBoundary=0)

    # Header
    now = datetime.now().strftime('%d/%m/%y %H:%M')
    print "==========================="
    print now
    print "==========================="
    header = Paragraph(now, headerStyle)
    header.wrap(width, 20)

    header.drawOn(canvas, width - 45, height - 15)

    # Elementos a dibujar
    story.append(Paragraph(pdt_obj.nombre, styleH))

    # OTs
    story.append(Paragraph('Resumen de OTs', styleN))

    ot_data = [['Número', 'Servicios', 'Importe Bruto', 'Importe Neto', 'Facturado']]
    for ot in pdt_obj.ot_set.all():
        ot_data.append([ot.codigo, ot.get_servicios(), '$' + str(ot.importe_bruto), '$' + str(ot.importe_neto), '$' + str(ot.get_facturacion())])

    ot_table = Table(ot_data, splitByRow=1, style=tableStyle, spaceBefore=10, spaceAfter=30)
    story.append(ot_table)

    # OTMLs
    story.append(Paragraph('Resumen de OTMLs', styleN))

    otml_data = [['Número', 'Servicios', 'Importe Bruto', 'Importe Neto', 'Facturado']]
    for otml in pdt_obj.otml_set.all():
        otml_data.append([otml.codigo, otml.get_servicios(), '$' + str(otml.importe_bruto), '$' + str(otml.importe_neto),
                        '$' + str(otml.get_facturacion())])

    otml_table = Table(otml_data, splitByRow=1, style=tableStyle, spaceBefore=10, spaceAfter=30)
    story.append(otml_table)

    # SOTs
    story.append(Paragraph('Resumen de SOTs', styleN))

    sot_data = [['Número', 'Servicios', 'Importe Bruto', 'Importe Neto', 'Facturado']]
    for sot in pdt_obj.sot_set.all():
        sot_data.append([sot.codigo, sot.get_servicios(), '$' + str(sot.importe_bruto), '$' + str(sot.importe_neto), '$' + str(sot.get_facturacion())])

    sot_table = Table(sot_data, splitByRow=1, style=tableStyle, spaceBefore=10, spaceAfter=30)
    story.append(sot_table)

    # RUTs
    story.append(Paragraph('Resumen de RUTs', styleN))

    rut_data = [['Número', 'Servicios', 'Importe Bruto', 'Importe Neto', 'Facturado']]
    for rut in pdt_obj.rut_set.all():
        rut_data.append(
            [rut.codigo, rut.get_servicios(), '$' + str(rut.importe_bruto), '$' + str(rut.importe_neto),
             '$' + str(rut.get_facturacion())])

    rut_table = Table(rut_data, splitByRow=1, style=tableStyle, spaceBefore=10, spaceAfter=30)
    story.append(rut_table)

    for s in story:
        while frame.add(s, canvas) == 0:
            splited_parts = frame.split(s, canvas)
            if len(splited_parts) > 1:
                frame.add(splited_parts[0], canvas)
                s = splited_parts[1]
            canvas.showPage()
            frame = Frame(0, 0, width, height, leftPadding=10, bottomPadding=50,
                          rightPadding=10, topPadding=50, id=2, showBoundary=0)

    canvas.save()

    return response


def filterOT(request, area):
    ofertatec = OfertaTec.objects.all().filter(area__in=[area, 'TODAS'])
    json_ofertatec = serializers.serialize("json", ofertatec)
    return HttpResponse(json_ofertatec, content_type="text/json")


def viewWord(request, *args, **kwargs):
    presup_id = kwargs.get('pk')
    presup_template = kwargs.get('template')
    presup_obj = Presupuesto.objects.get(id=presup_id)
    vals = {}
    turnos_activos = presup_obj.get_turnos_activos()
    vals['area'] = '-'.join([t.area for t in turnos_activos])
    vals['codigo'] = presup_obj.codigo + '-R' + str(presup_obj.nro_revision)
    vals['fecha'] = presup_obj.fecha_realizado.strftime('%d/%m/%Y') \
                    if presup_obj.fecha_realizado else ''
    vals['email'] = presup_obj.usuario.mail
    vals['solicitante'] = presup_obj.usuario.nombre
    vals['contacto'] = presup_obj.usuario.nombre
    vals['ofertatec'] = []
    vals['fecha_inicio'] = ''
    vals['fecha_fin'] = ''
    # Chequeo que al restarle 5 dias la fecha no quede anterior a la fecha de emision del primer turno
    if turnos_activos:
        # Si todavia no esta completa la fecha_realizado del presupuesto pongo la fecha de hoy
        fecha_realizado = presup_obj.fecha_realizado or datetime.now().date()
        turnos_activos = turnos_activos.order_by('fecha_inicio')
        turnoFechaInicioAnterior = turnos_activos[0]
        turnos_activos = turnos_activos.order_by('-fecha_fin')
        turnoFechaFinPosterior = turnos_activos[0]
        if turnoFechaInicioAnterior.fecha_inicio:
            date_less_five = turnoFechaInicioAnterior.fecha_inicio - timedelta(days=7)
            if date_less_five <= fecha_realizado:
                vals['fecha_inicio'] = turnoFechaInicioAnterior.fecha_inicio.strftime('%d/%m/%Y')
            else:
                vals['fecha_inicio'] = less_five(turnoFechaInicioAnterior.fecha_inicio)
        vals['fecha_fin'] = plus_five(turnoFechaFinPosterior.fecha_fin)

    vals['plantilla'] = ''

    if presup_template == 'asistencia':
        vals['plantilla'] = 'Presupuesto Asistencia.docx'
    elif presup_template == 'calibracion':
        vals['plantilla'] = 'Presupuesto Calibracion.docx'
    elif presup_template == 'in_situ':
        vals['plantilla'] = 'Presupuesto In Situ.docx'
    elif presup_template == 'lia':
        vals['plantilla'] = 'Presupuesto LIA.docx'
    elif presup_template == 'mat_ref':
        vals['plantilla'] = 'Materiales de Referencia.docx'

    for turno in turnos_activos:
        for o in turno.ofertatec_linea_set.get_queryset():
            vals['ofertatec'].append((o.ofertatec.codigo, o.ofertatec.detalle,
                                      o.cant_horas, o.precio, o.precio_total))
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


def viewSI(request, *args, **kwargs):
    si_id = kwargs.get('pk')
    si_obj = SI.objects.get(id=si_id)
    vals = {}
    vals['ejecutor'] = si_obj.ejecutor
    vals['solicitante'] = si_obj.solicitante
    vals['codigo'] = si_obj.codigo

    turnos_activos = si_obj.get_turnos_activos()
    if turnos_activos:
        turnos_activos = turnos_activos.order_by('fecha_inicio')
        turnoFechaInicioAnterior = turnos_activos[0].fecha_inicio
        turnos_activos = turnos_activos.order_by('-fecha_fin')
        turnoFechaFinPosterior = turnos_activos[0].fecha_fin

        vals['fecha_inicio'] = turnoFechaInicioAnterior.strftime('%d/%m/%Y') if turnoFechaInicioAnterior else ''
        vals['fecha_fin'] = turnoFechaFinPosterior.strftime('%d/%m/%Y') if turnoFechaFinPosterior else ''

    vals['fecha_apertura'] = si_obj.fecha_realizado.strftime('%d/%m/%Y')
    vals['ofertatec'] = []
    vals['tarea'] = []
    for t in si_obj.get_turnos_activos():
        for o in t.ofertatec_linea_set.all():
            vals['ofertatec'].append((o.ofertatec.codigo, o.detalle, o.tipo_servicio, o.cantidad, o.precio, o.precio_total))
    for t in si_obj.tarea_linea_set.get_queryset():
        vals['tarea'].append((t.tarea, t.horas))
    vals['plantilla'] = 'SI.docx'
    return genSI(vals)


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

        obj.write_activity_log("Revision #%d creada" % obj.nro_revision)
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

        obj.write_activity_log("Revision #%d eliminada" % obj.nro_revision)
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
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:ot-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_ot
                back_url_ot = http_referer
        return super(OTCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OTCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_ot
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

    @method_decorator(permission_required('adm.read_ot',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:ot-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_ot
                back_url_ot = http_referer
        return super(OTUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OTUpdate, self).get_context_data(**kwargs)
        turnoList = (context['object']).presupuesto.get_turnos_activos()
        context['turnos_activos'] = turnoList
        context['edit'] = self.request.GET.get('edit', False)
        context['back_url'] = back_url_ot
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
        t_inicial = time()
        # Por defecto los ordeno por codigo (desc)
        queryset = OT.objects.all().order_by('-codigo')
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        # Busco solo por fecha de realizacion de la OT
                        if re.match(r'^\d{2}\/\d{2}\/\d{4}-\d{2}\/\d{2}\/\d{4}$', arg):
                            start_date, end_date = map(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d'), arg.split("-"))
                            #recibosFilteredByDate = Recibo.objects.filter(Q(fecha__range=['%s' % start_date, '%s' % end_date]))
                            QList.append(Q(fecha_realizado__range=['%s' % start_date, '%s' % end_date]))# |
                                         #Q(factura_set__fecha__range=['%s' % start_date, '%s' % end_date]) |
                                         #Q(factura_set__fecha_aviso__range=['%s' % start_date, '%s' % end_date]) |
                                         #Q(factura_set__recibo__in=recibosFilteredByDate))
                            continue
                        recibosFiltered = Recibo.objects.filter(Q(numero__contains="%s" % arg) |
                                                       Q(comprobante_cobro__contains="%s" % arg) |
                                                       Q(importe__contains="%s" % arg))
                        QList.append(Q(estado__icontains="%s" % arg) |
                                    Q(presupuesto__codigo__contains="%s" % arg) |
                                    Q(presupuesto__usuario__nombre__icontains="%s" % arg) |
                                    Q(codigo__contains="%s" % arg) |
                                    Q(presupuesto__turno__area__icontains="%s" % arg) |
                                    Q(importe_bruto__contains="%s" % arg) |
                                    Q(factura_set__numero__contains="%s" % arg) |
                                    Q(factura_set__importe__contains="%s" % arg) |
                                    Q(factura_set__recibo__in=recibosFiltered) |
                                    Q(remito_set__numero__contains="%s" % arg))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        print "TIEMPO get_queryset: ", time() - t_inicial
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(OTList, self).get_context_data(**kwargs)
        field_names = ['estado', 'presupuesto__codigo', 'presupuesto__usuario__nombre',
                       'codigo', 'fecha_realizado', 'importe_bruto', 'presupuesto__turno__area',
                       'factura_set__numero', 'factura_set__fecha',
                       'factura_set__importe', 'factura_set__fecha_aviso',
                       'factura_set__recibo__numero', 'factura_set__recibo__comprobante_cobro', 'factura_set__recibo__fecha',
                       'factura_set__recibo__importe', 'remito_set__numero']
        field_labels = ['Estado', 'Nro. Presup.', 'Usuario', 'Nro. OT', 'Fecha', 'Imp. Bruto',
                        'Area', 'Nro. Factura', 'Fecha', 'Imp.', 'Fecha Aviso',
                        'Recibo', 'Tipo', 'Fecha', 'Imp.', 'Remito']

        context['fields'] = list(zip(field_names, field_labels))
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
                obs = request.POST.get('observations', '')
                try:
                    ot_obj._toState_cancelado(obs)
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
                try:
                    ot_obj._delete()
                    response_dict['redirect'] = reverse_lazy('adm:ot-list').strip()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
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
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:otml-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_otml
                back_url_otml = http_referer
        return super(OTMLCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OTMLCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_otml
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

    @method_decorator(permission_required('adm.read_otml',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:otml-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_otml
                back_url_otml = http_referer
        return super(OTMLUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OTMLUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['back_url'] = back_url_otml
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
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        # Busco solo por fecha de realizacion del presupuesto
                        if re.match(r'^\d{2}\/\d{2}\/\d{4}-\d{2}\/\d{2}\/\d{4}$', arg):
                            start_date, end_date = map(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d'), arg.split("-"))
                            QList.append(Q(fecha_realizado__range=['%s' % start_date, '%s' % end_date]))
                            continue
                        recibosFiltered = Recibo.objects.filter(Q(numero__contains="%s" % arg) |
                                                                Q(comprobante_cobro__contains="%s" % arg) |
                                                                Q(importe__contains="%s" % arg))
                        QList.append(Q(estado__icontains="%s" % arg) |
                                     Q(vpe__contains="%s" % arg) |
                                     Q(vpr__contains="%s" % arg) |
                                     Q(vpuu__contains="%s" % arg) |
                                     Q(usuario__nombre__icontains="%s" % arg) |
                                     Q(usuarioRep__nombre__icontains="%s" % arg) |
                                     Q(codigo__contains="%s" % arg) |
                                     Q(importe_bruto__contains="%s" % arg) |
                                     Q(factura_set__numero__icontains="%s" % arg) |
                                     Q(factura_set__importe__contains="%s" % arg) |
                                     Q(factura_set__recibo__in=recibosFiltered))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(OTMLList, self).get_context_data(**kwargs)

        field_names = ['estado', 'vpe', 'vpr', 'vpuu', 'usuario', 'usuarioRep', 'codigo', 'fecha_realizado',
                       'importe_bruto', 'factura_set__numero', 'factura_set__fecha', 'factura_set__importe',
                       'factura_set__recibo__comprobante_cobro', 'factura_set__recibo__numero',
                       'factura_set__recibo__fecha', 'factura_set__recibo__importe']
        field_labels = ['Estado', 'VPE', 'VPR', 'VPUU', 'Usuario', 'Usuario Representado', 'Nro. OT', 'Fecha',
                        'Imp. Bruto', 'Nro. Factura', 'Fecha', 'Imp.',
                        'Comprobante', 'Nro.', 'Fecha', 'Imp.']

        context['fields'] = list(zip(field_names, field_labels))
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
                obs = request.POST.get('observations', '')
                try:
                    otml_obj._toState_cancelado(obs)
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
                        otml_obj._toState_pagado()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_otml'):
                otml_id = request.POST.get('Eliminar')
                otml_obj = OTML.objects.get(pk=otml_id)
                try:
                    otml_obj._delete()
                    response_dict['redirect'] = reverse_lazy('adm:otml-list').strip()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
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
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:sot-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_sot
                back_url_sot = http_referer
        return super(SOTCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SOTCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_sot
        return context

    def get_success_url(self):
        return reverse_lazy('adm:sot-update', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        kwargs = super(SOTCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

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

    @method_decorator(permission_required('adm.read_sot',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:sot-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_sot
                back_url_sot = http_referer
        return super(SOTUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SOTUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['back_url'] = back_url_sot
        context['userGroups'] = self.request.user.groups.values_list('name', flat=True)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:sot-update', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        kwargs = super(SOTUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

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
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        # Busco solo por fecha de realizacion de la SOT
                        if re.match(r'^\d{2}\/\d{2}\/\d{4}-\d{2}\/\d{2}\/\d{4}$', arg):
                            start_date, end_date = map(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d'), arg.split("-"))
                            QList.append(Q(fecha_realizado__range=['%s' % start_date, '%s' % end_date]))
                            continue
                        QList.append(Q(estado__icontains="%s" % arg) |
                                    Q(codigo__contains="%s" % arg) |
                                    Q(deudor__nombre__icontains="%s" % arg) |
                                    Q(solicitante__icontains="%s" % arg) |
                                    Q(importe_bruto__contains="%s" % arg) |
                                    Q(importe_neto__contains="%s" % arg))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(SOTList, self).get_context_data(**kwargs)

        field_names = ['estado', 'codigo', 'fecha_realizado', 'deudor', 'solicitante',
                       'importe_bruto', 'importe_neto', 'fecha_envio_ut', 'fecha_envio_cc',
                       'firmada']
        field_labels = ['Estado', 'Nro. SOT', 'Fecha Realizada', 'UT Deudora', 'Area Solic.',
                        'Imp. Bruto', 'Imp. Neto',  'Fecha Envio UT', 'Retorno Firmada',
                        'Fecha Envio CC']

        context['fields'] = list(zip(field_names, field_labels))
        # Fecha de hoy para coloreo de filas
        context['today'] = datetime.now().strftime("%d/%m/%Y")
        # Para la paginacion
        if 'order_by' in self.request.GET:
            context['order_by'] = self.request.GET['order_by']
        print "TIEMPO get_context_data: ", time() - t_inicial
        context['userGroups'] = self.request.user.groups.values_list('name', flat=True)
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Cancelar' in request.POST:
            if request.user.has_perm('adm.cancel_sot'):
                sot_id = request.POST.get('Cancelar')
                sot_obj = SOT.objects.get(pk=sot_id)
                obs = request.POST.get('observations', '')
                try:
                    sot_obj._toState_cancelada(obs)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        #Finalizo solo la SOT
        if 'Finalizar1' in request.POST:
            if request.user.has_perm('adm.finish_sot'):
                sot_id = request.POST.get('Finalizar1')
                sot_obj = SOT.objects.get(pk=sot_id)
                try:
                    sot_obj._toState_cobrada(False)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        #Finalizo la SOT y el Presupuesto asociado
        if 'Finalizar2' in request.POST:
            if request.user.has_perm('adm.finish_sot'):
                sot_id = request.POST.get('Finalizar2')
                sot_obj = SOT.objects.get(pk=sot_id)
                try:
                    sot_obj._toState_cobrada(True)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_sot'):
                sot_id = request.POST.get('Eliminar')
                sot_obj = SOT.objects.get(pk=sot_id)
                try:
                    sot_obj._delete()
                    response_dict['redirect'] = reverse_lazy('adm:sot-list').strip()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)

#===========================================
#================== RUT ====================
#===========================================


class RUTCreate(CreateView):
    model = RUT
    form_class = RUTForm

    @method_decorator(permission_required('adm.add_rut',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:rut-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_rut
                back_url_rut = http_referer
        return super(RUTCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RUTCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_rut
        return context

    def get_success_url(self):
        return reverse_lazy('adm:rut-update', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        kwargs = super(RUTCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

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

    @method_decorator(permission_required('adm.read_rut',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:rut-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_rut
                back_url_rut = http_referer
        return super(RUTUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RUTUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['back_url'] = back_url_rut
        context['userGroups'] = self.request.user.groups.values_list('name', flat=True)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:rut-update', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        kwargs = super(RUTUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

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
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        # Busco solo por fecha de realizacion de la RUT
                        if re.match(r'^\d{2}\/\d{2}\/\d{4}-\d{2}\/\d{2}\/\d{4}$', arg):
                            start_date, end_date = map(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d'), arg.split("-"))
                            QList.append(Q(fecha_realizado__range=['%s' % start_date, '%s' % end_date]))
                            continue
                        QList.append(Q(estado__icontains="%s" % arg) |
                                    Q(codigo__contains="%s" % arg) |
                                    Q(deudor__nombre__icontains="%s" % arg) |
                                    Q(ejecutor__nombre__icontains="%s" % arg) |
                                    Q(solicitante__icontains="%s" % arg) |
                                    Q(importe_bruto__contains="%s" % arg) |
                                    Q(importe_neto__contains="%s" % arg))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(RUTList, self).get_context_data(**kwargs)

        field_names = ['estado', 'codigo', 'fecha_realizado', 'deudor', 'solicitante',
                       'importe_bruto', 'importe_neto', 'fecha_envio_ut', 'firmada',
                       'fecha_envio_cc']
        field_labels = ['Estado', 'Nro. RUT', 'Fecha', 'UT Deudora', 'Area Solic.', 'Imp. Bruto',
                        'Imp. Neto', 'Fecha Envio a UT', 'Retorno Firmada', 'Fecha Envio a CC']

        context['fields'] = list(zip(field_names, field_labels))
        # Fecha de hoy para coloreo de filas
        context['today'] = datetime.now().strftime("%d/%m/%Y")
        # Para la paginacion
        if 'order_by' in self.request.GET:
            context['order_by'] = self.request.GET['order_by']
        print "TIEMPO get_context_data: ", time() - t_inicial
        context['userGroups'] = self.request.user.groups.values_list('name', flat=True)
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Cancelar' in request.POST:
            if request.user.has_perm('adm.cancel_rut'):
                rut_id = request.POST.get('Cancelar')
                rut_obj = RUT.objects.get(pk=rut_id)
                obs = request.POST.get('observations', '')
                try:
                    rut_obj._toState_cancelada(obs)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        #Finalizo solo la RUT
        if 'Finalizar1' in request.POST:
            if request.user.has_perm('adm.finish_rut'):
                rut_id = request.POST.get('Finalizar1')
                rut_obj = RUT.objects.get(pk=rut_id)
                try:
                    rut_obj._toState_cobrada(False)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        #Finalizo la RUT y el Presupuesto asociado
        if 'Finalizar2' in request.POST:
            if request.user.has_perm('adm.finish_rut'):
                rut_id = request.POST.get('Finalizar2')
                rut_obj = RUT.objects.get(pk=rut_id)
                try:
                    rut_obj._toState_cobrada(True)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_rut'):
                rut_id = request.POST.get('Eliminar')
                rut_obj = RUT.objects.get(pk=rut_id)
                try:
                    rut_obj._delete()
                    response_dict['redirect'] = reverse_lazy('adm:rut-list').strip()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)

#===========================================
#================== SI =====================
#===========================================


class SICreate(CreateView):
    model = SI
    form_class = SIForm

    @method_decorator(permission_required('adm.add_si',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:si-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_si
                back_url_si = http_referer
        return super(SICreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SICreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_si
        return context

    def get_success_url(self):
        return reverse_lazy('adm:si-update', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        kwargs = super(SICreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        tarea_linea_form = Tarea_LineaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  tarea_linea_form=tarea_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        tarea_linea_form = Tarea_LineaFormSet(self.request.POST)
        if (form.is_valid() and tarea_linea_form.is_valid()):
            return self.form_valid(form, tarea_linea_form)
        else:
            return self.form_invalid(form, tarea_linea_form)

    def form_valid(self, form, tarea_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Factuas and Recibos then redirects to a
        success page.
        """
        self.object = form.save()
        tarea_linea_form.instance = self.object
        tarea_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, tarea_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  tarea_linea_form=tarea_linea_form))


class SIUpdate(UpdateView):
    model = SI
    form_class = SIForm
    template_name_suffix = '_form'

    @method_decorator(permission_required('adm.read_si',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:si-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_si
                back_url_si = http_referer
        return super(SIUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SIUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['back_url'] = back_url_si
        context['userGroups'] = self.request.user.groups.values_list('name', flat=True)
        return context

    def get_success_url(self):
        return reverse_lazy('adm:si-update', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        kwargs = super(SIUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates filled versions of the form
        and its inline formsets.
        """
        self.object = SI.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        tarea_linea_form = Tarea_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  tarea_linea_form=tarea_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = SI.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        tarea_linea_form = Tarea_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and tarea_linea_form.is_valid()):
            return self.form_valid(form, tarea_linea_form)
        else:
            return self.form_invalid(form, tarea_linea_form)

    def form_valid(self, form, tarea_linea_form):
        """
        Called if all forms are valid. Creates an OT instance along with
        associated Facturas and then redirects to a
        success page.
        """
        form.save()
        tarea_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, tarea_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  tarea_linea_form=tarea_linea_form))


class SIList(ListView):
    model = SI
    template_name = 'adm/si_list.html'
    paginate_by = 30

    def get_queryset(self):
        # Por defecto los ordeno por codigo (desc)
        queryset = SI.objects.all().order_by('-codigo')
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        # Busco solo por fecha de realizacion de la SOT
                        if re.match(r'^\d{2}\/\d{2}\/\d{4}-\d{2}\/\d{2}\/\d{4}$', arg):
                            start_date, end_date = map(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d'), arg.split("-"))
                            QList.append(Q(fecha_realizado__range=['%s' % start_date, '%s' % end_date]))
                            continue
                        QList.append(Q(estado__icontains="%s" % arg) |
                                    Q(codigo__contains="%s" % arg) |
                                    Q(ejecutor__icontains="%s" % arg) |
                                    Q(solicitante__icontains="%s" % arg) |
                                    Q(importe_neto__contains="%s" % arg))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        t_inicial = time()
        context = super(SIList, self).get_context_data(**kwargs)

        field_names = ['estado', 'codigo', 'solicitante', 'ejecutor', 'fecha_realizado']
        field_labels = ['Estado', 'Nro. SI', 'Area Solicitante', 'Area Ejecutora', 'Fecha Realizada']

        context['fields'] = list(zip(field_names, field_labels))
        # Fecha de hoy para coloreo de filas
        context['today'] = datetime.now().strftime("%d/%m/%Y")
        # Para la paginacion
        if 'order_by' in self.request.GET:
            context['order_by'] = self.request.GET['order_by']
        print "TIEMPO get_context_data: ", time() - t_inicial
        context['userGroups'] = self.request.user.groups.values_list('name', flat=True)
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        userGroups = request.user.groups.values_list('name', flat=True)
        if 'Cancelar' in request.POST:
            if request.user.has_perm('adm.cancel_si'):
                si_id = request.POST.get('Cancelar')
                si_obj = SI.objects.get(pk=si_id)
                obs = request.POST.get('observations', '')
                if si_obj.ejecutor in userGroups:
                    try:
                        si_obj._toState_cancelada(obs)
                    except StateError as e:
                        response_dict['ok'] = False
                        response_dict['msg'] = e.message
                else:
                    response_dict['ok'] = False
                    response_dict['msg'] = "No tiene permisos para realizar esta acción"
            else:
                raise PermissionDenied
        if 'Finalizar' in request.POST:
            if request.user.has_perm('adm.finish_si'):
                si_id = request.POST.get('Finalizar')
                si_obj = SI.objects.get(pk=si_id)
                if si_obj.ejecutor in userGroups:
                    try:
                        si_obj._toState_finalizada()
                    except StateError as e:
                        response_dict['ok'] = False
                        response_dict['msg'] = e.message
                else:
                    response_dict['ok'] = False
                    response_dict['msg'] = "No tiene permisos para realizar esta acción"
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_si'):
                si_id = request.POST.get('Eliminar')
                si_obj = SI.objects.get(pk=si_id)
                if si_obj.ejecutor in userGroups:
                    try:
                        si_obj._delete()
                        response_dict['redirect'] = reverse_lazy('adm:si-list').strip()
                    except StateError as e:
                        response_dict['ok'] = False
                        response_dict['msg'] = e.message
                else:
                    response_dict['ok'] = False
                    response_dict['msg'] = "No tiene permisos para realizar esta acción"
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)

#===========================================
#========== VISTAS PRESUPUESTO =============
#===========================================


class PresupuestoCreate(CreateView):
    model = Presupuesto
    form_class = PresupuestoForm
    back_url = reverse_lazy('adm:presup-list')

    @method_decorator(permission_required('adm.add_presupuesto',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:presup-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_presupuesto
                back_url_presupuesto = http_referer
        return super(PresupuestoCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PresupuestoCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_presupuesto
        return context

    def get_success_url(self):
        return reverse_lazy('adm:presup-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        instrumento_linea_form = Instrumento_LineaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  instrumento_linea_form=instrumento_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        instrumento_linea_form = Instrumento_LineaFormSet(self.request.POST)
        if (form.is_valid() and instrumento_linea_form.is_valid()):
            return self.form_valid(form, instrumento_linea_form)
        else:
            return self.form_invalid(form, instrumento_linea_form)

    def form_valid(self, form, instrumento_linea_form):
        """
        Called if all forms are valid. Creates a Turno instance along with
        associated OfertaTec_Lineas and then redirects to a
        success page.
        """
        self.object = form.save()
        instrumento_linea_form.instance = self.object
        instrumento_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, instrumento_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  instrumento_linea_form=instrumento_linea_form))


class PresupuestoList(ListView):
    model = Presupuesto
    template_name = 'adm/presupuesto_list.html'
    paginate_by = 30

    def _checkstate(self, queryset):
        """
        Chequeo los presupuestos que hay que cancelar.
        Seran cancelados los presupuestos que no hayan sido aceptados pasados 21 dias corridos
        de la fecha de realizacion del mismo.
        Para las asistencias el plazo es 60 dias corridos.
        """
        for presup in queryset.filter(estado='borrador').exclude(fecha_realizado=None):
            if ((presup.fecha_realizado + timedelta(days=21) < datetime.now().date() and presup.tipo != 'asistencia') or
               (presup.fecha_realizado + timedelta(days=60) < datetime.now().date() and presup.tipo == 'asistencia')):
                presup._toState_cancelado(obs="Registro automático: Presupuesto vencido")

    def get_queryset(self):
        queryset = Presupuesto.objects.select_related()
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        # Busco solo por fecha de realizacion del presupuesto
                        if re.match(r'^\d{2}\/\d{2}\/\d{4}-\d{2}\/\d{2}\/\d{4}$', arg):
                            start_date, end_date = map(lambda x: datetime.strptime(x, '%d/%m/%Y').strftime('%Y-%m-%d'), arg.split("-"))
                            QList.append(Q(fecha_realizado__range=['%s' % start_date, '%s' % end_date]))
                            continue
                        QList.append(Q(estado__icontains="%s" % arg) |
                                    Q(codigo__contains="%s" % arg) |
                                    Q(usuario__nombre__icontains="%s" % arg) |
                                    Q(usuario__nro_usuario__icontains="%s" % arg) |
                                    Q(codigo__contains="%s" % arg) |
                                    Q(turno__area__icontains="%s" % arg))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        self._checkstate(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PresupuestoList, self).get_context_data(**kwargs)

        presupuestos_by_page = context['object_list']
        turnos_by_page = [p.get_turnos_activos() for p in presupuestos_by_page]

        context['tuple_paginated_list'] = list(zip(presupuestos_by_page, turnos_by_page))

        field_names = ['estado', 'codigo', 'usuario__nombre', 'usuario__nro_usuario',
                       'turno__area',
                       'fecha_realizado',
                       'fecha_aceptado',
                       'instrumento__fecha_llegada',
                       'instrumento__nro_recepcion']
        field_labels = ['Estado', 'Nro.', 'Usuario', 'Nro Usuario',
                        'Area',
                        'Fecha de Realizacion',
                        'Fecha de Aceptacion',
                        'Llegada del Instrumento',
                        'Nro Recepcion']

        context['fields'] = list(zip(field_names, field_labels))
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
            turnoList = obj_presup.get_turnos_activos()
            for turno in turnoList:
                kwargs['pk'] = presup_id
                for linea in turno.ofertatec_linea_set.all():
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
                obs = request.POST.get('observations', '')
                try:
                    presup_obj._toState_cancelado(obs)
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
            else:
                raise PermissionDenied
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_presupuesto'):
                presup_id = request.POST.get('Eliminar')
                presup_obj = Presupuesto.objects.get(pk=presup_id)
                try:
                    presup_obj._delete()
                    response_dict['redirect'] = reverse_lazy('adm:presup-list').strip()
                except StateError as e:
                    response_dict['ok'] = False
                    response_dict['msg'] = e.message
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

    @method_decorator(permission_required('adm.read_presupuesto',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:presup-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_presupuesto
                back_url_presupuesto = http_referer
        return super(PresupuestoUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PresupuestoUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['turnos_activos'] = (context['object']).get_turnos_activos()
        context['revision'] = self.request.GET.get('revision', False)
        # Revisionado
        presupVers = Version.objects.get_for_object(self.object).exclude(revision__comment__contains='T_')
        turnoVersByRevision = []
        usuarioVersByRevision = []
        otLineaVersByRevision = []
        instrLineaVersByRevision = []
        pdtVersByRevision = []
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
                # Todas las lineas de ot versionados en la revision revId
                ot = objectsVersiones.filter(content_type__model='ofertatec_linea').order_by('object_id')
                otLineaVersByRevision.append(ot)
                # Todas las lineas de instrumento versionados en la revision revId
                instr = objectsVersiones.filter(content_type__model='instrumento').order_by('object_id')
                instrLineaVersByRevision.append(instr)
                # Todos los pdt versionados en la revision revId
                pdt = objectsVersiones.filter(content_type__model='pdt')
                pdtVersByRevision.append(pdt)
        context['presupVersions'] = zip(presupVers, turnoVersByRevision, usuarioVersByRevision, otLineaVersByRevision,
                                        instrLineaVersByRevision, pdtVersByRevision)
        context['back_url'] = back_url_presupuesto
        return context

    def get_success_url(self):
        return reverse_lazy('adm:presup-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates filled versions of the form
        and its inline formsets.
        """
        self.object = Presupuesto.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        instrumento_linea_form = Instrumento_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  instrumento_linea_form=instrumento_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = Presupuesto.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        instrumento_linea_form = Instrumento_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and instrumento_linea_form.is_valid()):
            return self.form_valid(form, instrumento_linea_form)
        else:
            return self.form_invalid(form, instrumento_linea_form)

    def form_valid(self, form, instrumento_linea_form):
        """
        Called if all forms are valid. Creates a Turno instance along with
        associated OfertaTec_Lineas and then redirects to a
        success page.
        """
        form.save()
        instrumento_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, instrumento_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  instrumento_linea_form=instrumento_linea_form))

#=================================================
#========= VISTAS OFERTA TECNOLOGICA =============
#=================================================


class OfertaTecList(ListView):
    model = OfertaTec
    paginate_by = 50

    def get_queryset(self):
        queryset = OfertaTec.objects.all()
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        QList.append(Q(proveedor__contains="%s" % arg) |
                                    Q(codigo__contains="%s" % arg) |
                                    Q(rubro__icontains="%s" % arg) |
                                    Q(subrubro__icontains="%s" % arg) |
                                    Q(tipo_servicio__icontains="%s" % arg) |
                                    Q(area__icontains="%s" % arg) |
                                    Q(detalle__icontains="%s" % arg) |
                                    Q(precio__contains="%s" % arg))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(OfertaTecList, self).get_context_data(**kwargs)
        field_names = ['proveedor', 'codigo', 'rubro', 'subrubro',
                       'tipo_servicio', 'area', 'detalle', 'precio']
        field_labels = ['Proveedor', 'Codigo', 'Rubro', 'Subrubro',
                        'Tipo de Servicio', 'Area', 'Detalle', 'Precio']
        context['fields'] = list(zip(field_names, field_labels))
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
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:ofertatec-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_ofertatec
                back_url_ofertatec = http_referer
        return super(OfertaTecCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OfertaTecCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_ofertatec
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
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:ofertatec-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_ofertatec
                back_url_ofertatec = http_referer
        return super(OfertaTecUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OfertaTecUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['back_url'] = back_url_ofertatec
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
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        QList.append(Q(nro_usuario__contains="%s" % arg) |
                                    Q(nombre__icontains="%s" % arg) |
                                    Q(cuit__contains="%s" % arg) |
                                    Q(mail__icontains="%s" % arg) |
                                    Q(rubro__icontains="%s" % arg))
                    QList = reduce(operator.and_, QList)
                    queryset = queryset.filter(QList).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UsuarioList, self).get_context_data(**kwargs)
        field_names = ['nro_usuario', 'nombre', 'cuit', 'mail', 'rubro']
        field_labels = ['Nro. Usuario', 'Nombre', 'Cuit', 'Mail', 'Rubro']

        context['fields'] = list(zip(field_names, field_labels))
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
                    response_dict['msg'] = 'No se puede borrar el usuario seleccionado'
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
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:usuarios-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_usuario
                back_url_usuario = http_referer
        return super(UsuarioCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsuarioCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_usuario
        return context

    def get_success_url(self):
        return reverse_lazy('adm:usuarios-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contacto_linea_form = Contacto_LineaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contacto_linea_form=contacto_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contacto_linea_form = Contacto_LineaFormSet(self.request.POST)
        if (form.is_valid() and contacto_linea_form.is_valid()):
            return self.form_valid(form, contacto_linea_form)
        else:
            return self.form_invalid(form, contacto_linea_form)

    def form_valid(self, form, contacto_linea_form):
        """
        Called if all forms are valid. Creates a Turno instance along with
        associated OfertaTec_Lineas and then redirects to a
        success page.
        """
        self.object = form.save()
        contacto_linea_form.instance = self.object
        contacto_linea_form.save()

        if self.request.POST.get('_popup', 0):
            nombre = self.object.nombre.upper()
            id = self.object.id
            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup( window, \'%s\', \'%s\' );</script>'
                    % (id, nombre))
        else:
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, contacto_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contacto_linea_form=contacto_linea_form))


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
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:usuarios-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_usuario
                back_url_usuario = http_referer
        return super(UsuarioUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsuarioUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['back_url'] = back_url_usuario
        return context

    def get_success_url(self):
        return reverse_lazy('adm:usuarios-update', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates filled versions of the form
        and its inline formsets.
        """
        self.object = Usuario.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contacto_linea_form = Contacto_LineaFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contacto_linea_form=contacto_linea_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = Usuario.objects.get(pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contacto_linea_form = Contacto_LineaFormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and contacto_linea_form.is_valid()):
            return self.form_valid(form, contacto_linea_form)
        else:
            return self.form_invalid(form, contacto_linea_form)

    def form_valid(self, form, contacto_linea_form):
        """
        Called if all forms are valid. Creates a Turno instance along with
        associated OfertaTec_Lineas and then redirects to a
        success page.
        """
        form.save()
        contacto_linea_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, contacto_linea_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contacto_linea_form=contacto_linea_form))


class UsuarioCreateModal(UsuarioCreate):
    template_name = "adm/usuario_modal.html"

    def get_context_data(self, **kwargs):
        context = super(UsuarioCreateModal, self).get_context_data(**kwargs)
        context['popup'] = self.request.GET.get('_popup', 0)
        context['create'] = 1
        return context

    def form_valid(self, form, contacto_linea_form):
        super(UsuarioCreateModal, self).form_valid(form, contacto_linea_form)

        nombre = escape(self.object)
        id = escape(self.object.id)
        return HttpResponse(
                '<script type="text/javascript">opener.dismissAddAnotherPopup( window, \'%s\', \'%s\' );</script>'
                % (id, nombre))


class UsuarioUpdateModal(UsuarioUpdate):
    template_name = "adm/usuario_modal.html"

    def get_context_data(self, **kwargs):
        context = super(UsuarioUpdateModal, self).get_context_data(**kwargs)
        context['popup'] = self.request.GET.get('_popup', 0)
        return context


class ContactoCreateModal(CreateView):
    model = Contacto
    template_name = "adm/contacto_modal.html"
    form_class = ContactoForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ContactoCreateModal, self).get_context_data(**kwargs)
        context['popup'] = self.request.GET.get('_popup', 0)
        context['parent_id'] = self.request.GET.get('parent_id', 0)
        context['create'] = 1
        context['edit'] = 1
        return context


    def form_valid(self, form):
        super(ContactoCreateModal, self).form_valid(form)

        nombre = escape(self.object)
        id = escape(self.object.id)
        return HttpResponse(
                '<script type="text/javascript">opener.dismissAddAnotherPopup( window, \'%s\', \'%s\' );</script>'
                % (id, nombre))


class ContactoUpdateModal(UpdateView):
    model = Contacto
    template_name = "adm/contacto_modal.html"
    form_class = ContactoForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ContactoUpdateModal, self).get_context_data(**kwargs)
        context['popup'] = self.request.GET.get('_popup', 0)
        context['parent_id'] = self.request.GET.get('parent_id', 0)
        context['edit'] = 0
        return context

    def form_valid(self, form):
        super(ContactoUpdateModal, self).form_valid(form)

        nombre = escape(self.object)
        id = escape(self.object.id)
        return HttpResponse(
            '<script type="text/javascript">opener.dismissAddAnotherPopup( window, \'%s\', \'%s\' );</script>'
            % (id, nombre))

#===========================================
#================== PDT ====================
#===========================================


class PDTList(ListView):
    model = PDT
    template_name = 'adm/pdt_list.html'
    paginate_by = 30

    def get_queryset(self):
        queryset = PDT.objects.all().exclude(codigo='0')
        for key, vals in self.request.GET.lists():
            if key != 'page':
                if key == 'order_by':
                    queryset = queryset.order_by(vals[0])
                if key == 'search':
                    searchArgs = vals[0].split(",")
                    QList = []
                    for arg in searchArgs:
                        QList = (Q(anio__icontains="%s" % arg) |
                                 Q(tipo__icontains="%s" % arg) |
                                 Q(codigo__icontains="%s" % arg) |
                                 Q(nombre__icontains="%s" % arg))
                    queryset = queryset.filter(QList).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PDTList, self).get_context_data(**kwargs)
        field_names = ['anio', 'tipo', 'codigo', 'nombre', 'cantidad_servicios', 'cantidad_contratos', 'facturacion_prevista']
        field_labels = ['Año', 'Tipo de Plan', 'Código', 'Nombre', 'Cantidad de Servicios', 'Cantidad de OT/SOT/RUT', 'Facturación Anual']

        context['fields'] = list(zip(field_names, field_labels))
        # Para la paginacion
        if self.request.GET.has_key('order_by'):
            context['order_by'] = self.request.GET['order_by']
        return context

    def post(self, request, *args, **kwargs):
        response_dict = {'ok': True, 'msg': None}
        if 'Eliminar' in request.POST:
            if request.user.has_perm('adm.delete_pdt'):
                pdt_id = request.POST.get('Eliminar')
                pdt_obj = PDT.objects.get(pk=pdt_id)
                if not pdt_obj._delete():
                    response_dict['ok'] = False
                    response_dict['msg'] = 'No se puede borrar el PDT ya que tiene\
                                            documentos asociados'
                else:
                    response_dict['redirect'] = reverse_lazy('adm:pdt-list').strip()
            else:
                raise PermissionDenied
        return JsonResponse(response_dict)


class PDTCreate(CreateView):
    model = PDT
    form_class = PDTForm

    @method_decorator(permission_required('adm.add_pdt',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:pdt-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_pdt
                back_url_pdt = http_referer
        return super(PDTCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PDTCreate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['back_url'] = back_url_pdt
        return context

    def get_success_url(self):
        return reverse_lazy('adm:pdt-update', kwargs={'pk': self.object.id})


class PDTUpdate(UpdateView):
    model = PDT
    form_class = PDTForm
    template_name_suffix = '_form'

    @method_decorator(permission_required('adm.read_pdt',
                      raise_exception=True))
    def dispatch(self, *args, **kwargs):
        if self.request.META.get('HTTP_REFERER', False):
            http_referer = self.request.META['HTTP_REFERER'].split(self.request.get_host())[1]
            pattern = re.compile("^" + reverse_lazy('adm:pdt-list').decode() + "(\?([a-zA-Z_]+=[^&]*&{0,1})+)*$")
            if pattern.match(http_referer):
                global back_url_pdt
                back_url_pdt = http_referer
        return super(PDTUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PDTUpdate, self).get_context_data(**kwargs)
        context['edit'] = self.request.GET.get('edit', False)
        context['back_url'] = back_url_pdt
        return context

    def get_success_url(self):
        return reverse_lazy('adm:pdt-update', kwargs={'pk': self.object.id})


class PDTDetail(TemplateView):
    template_name = "adm/pdt_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PDTDetail, self).get_context_data(**kwargs)
        pdt_id = kwargs.get('pk', None)
        context['pdt'] = PDT.objects.get(id=pdt_id)
        return context


