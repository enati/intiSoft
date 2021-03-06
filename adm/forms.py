# -*- coding: utf-8 -*-
from time import time
from django import forms
from simple_autocomplete.widgets import AutoCompleteWidget
from django.conf import settings
from adm.widgets import RelatedFieldWidgetCanAdd, NestedRelatedFieldWidgetCanAdd
from lab.models import Turno
from .models import Presupuesto, OfertaTec, Usuario, Contrato, OT, OTML, SI, Factura, \
    Recibo, Remito, OT_Linea, SOT, RUT, Tarea_Linea, Instrumento, PDT, Contacto, DireccionUsuario, Localidad, \
    CentroDeCostos
from django.contrib.contenttypes.forms import generic_inlineformset_factory, BaseGenericInlineFormSet
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms.forms import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, User
from searchableselect.widgets import SearchableSelect
from datetime import datetime

editable_fields = ['fecha_realizado', 'fecha_aceptado', 'tipo', 'centro_costos', 'area_tematica', 'horizonte']


def bootstrap_format(f, **kwargs):
    formfield = f.formfield(**kwargs)
    # Uppercase para usuario y ofertatec
    if f.name in ['nombre', 'rubro', 'subrubro', 'tipo_servicio', 'area']:
        formfield.widget.attrs.update({'style': 'text-transform: uppercase'})
    tmp = formfield.widget.attrs.get('class') or ''
    if f.name != 'descuento_fijo':
        formfield.widget.attrs.update({'class': 'form-control ' + tmp})
    return formfield


def base_bootstrap_format(f, **kwargs):
    formfield = f.formfield(**kwargs)
    tmp = formfield.widget.attrs.get('class') or ''
    formfield.widget.attrs.update({'class': 'form-control ' + tmp})
    return formfield


class OTForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    def __init__(self, *args, **kwargs):
        super(OTForm, self).__init__(*args, **kwargs)
        # Filtro los centros de costos segun la region
        self.fields['centro_costos'].queryset = CentroDeCostos.objects.filter(region='CENTRO')
        # El nro de presup no tiene que tener form-control
        self.fields['codigo'].widget.attrs['class'] = 'OT_code'
        self.fields['codigo'].widget.attrs['form'] = 'OTForm'
        self.fields['importe_bruto'].widget.attrs['readonly'] = True
        self.fields['importe_neto'].widget.attrs['readonly'] = True
        if not self.instance or self.instance.estado == 'sin_facturar':
            year = datetime.now().year
            self.fields['pdt'].queryset = PDT.objects.filter(anio=year) | PDT.objects.filter(anio__isnull=True)
        if self.instance:
            if self.instance.estado in ['sin_facturar']:
                # Solo se deben poder crear OTS a presupuestos aceptados
                self.fields['presupuesto'].queryset = \
                    Presupuesto.objects.filter(estado__in=['aceptado', 'en_proceso_de_facturacion']).order_by('-id')
            if self.instance.estado != 'sin_facturar':
                for f in self.fields:
                    if f not in ['fecha_aviso', 'centro_costos', 'area_tematica', 'horizonte']:
                        self.fields[f].widget.attrs['disabled'] = True
                        self.fields[f].required = False

    def clean_fecha_realizado(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.fecha_realizado
        else:
            return self.cleaned_data['fecha_realizado']

    def clean_fecha_aviso(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.fecha_aviso
        else:
            return self.cleaned_data['fecha_aviso']

    def clean_importe_bruto(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.importe_bruto
        else:
            return self.cleaned_data['importe_bruto']

    def clean_importe_neto(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.importe_neto
        else:
            return self.cleaned_data['importe_neto']

    def clean_descuento(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.descuento
        else:
            return self.cleaned_data['descuento']

    def clean_centro_costos(self):
        if self.instance and self.instance.estado not in ['sin_facturar', 'no_pago']:
            return self.instance.centro_costos
        else:
            return self.cleaned_data['centro_costos']

    def clean_area_tematica(self):
        if self.instance and self.instance.estado not in ['sin_facturar', 'no_pago']:
            return self.instance.area_tematica
        else:
            return self.cleaned_data['area_tematica']

    def clean_horizonte(self):
        if self.instance and self.instance.estado not in ['sin_facturar', 'no_pago']:
            return self.instance.horizonte
        else:
            return self.cleaned_data['horizonte']

    def clean_codigo(self):
        codigoList = OTML.objects.values_list('codigo', flat=True)
        if self.instance and self.instance.estado != 'sin_facturar':
            codigo = self.instance.codigo
        else:
            codigo = self.cleaned_data['codigo']
        if codigo in codigoList:
            raise ValidationError(
                ('Ya existe una OT con ese número.'),
                code='unique',
            )
        return codigo

    def clean_presupuesto(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.presupuesto
        else:
            return self.cleaned_data['presupuesto']



    class Meta:
        model = OT
        fields = ['estado',
                  'codigo',
                  'presupuesto',
                  'fecha_realizado',
                  'importe_bruto',
                  'importe_neto',
                  'descuento',
                  'pdt',
                  'centro_costos',
                  'area_tematica',
                  'horizonte']

        error_messages = {
            'presupuesto': {
                'required': 'Campo obligatorio.',
            },
            'fecha_realizado': {
                'required': 'Campo obligatorio.',
            },
            'importe_bruto': {
                'required': 'Campo obligatorio.',
            },
            'pdt': {
                'required': 'Campo obligatorio.',
            },
            'centro_costos': {
                'required': 'Campo obligatorio.',
            },
            'area_tematica': {
                'required': 'Campo obligatorio.',
            },
            'horizonte': {
                'required': 'Campo obligatorio.',
            }
        }

        widgets = {
            'fecha_realizado': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'importe_bruto': forms.TextInput(),
        }


class OTMLForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    def __init__(self, *args, **kwargs):
        super(OTMLForm, self).__init__(*args, **kwargs)
        # Filtro los centros de costos segun la region
        self.fields['centro_costos'].queryset = CentroDeCostos.objects.filter(region='CENTRO')
        self.fields['codigo'].widget.attrs['class'] = 'OT_code'
        self.fields['codigo'].widget.attrs['form'] = 'OTMLForm'
        self.fields['importe_neto'].widget.attrs['readonly'] = True
        self.fields['importe_bruto'].widget.attrs['readonly'] = True
        if not self.instance or self.instance.estado == 'sin_facturar':
            year = datetime.now().year
            self.fields['pdt'].queryset = PDT.objects.filter(anio=year) | PDT.objects.filter(anio__isnull=True)
        if self.instance:
            if self.instance.estado != 'sin_facturar':
                for f in self.fields:
                    if f != 'fecha_aviso' and f != 'checkbox_sot':
                        self.fields[f].widget.attrs['disabled'] = True
                        self.fields[f].required = False

    def clean_codigo(self):
        codigoList = OT.objects.values_list('codigo', flat=True)
        if self.instance and self.instance.estado != 'sin_facturar':
            codigo = self.instance.codigo
        else:
            codigo = self.cleaned_data['codigo']
        if codigo in codigoList:
            raise ValidationError(
                ('Ya existe una OT con ese número.'),
                code='unique',
            )
        return codigo

    def clean_importe_bruto(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.importe_bruto
        else:
            return self.cleaned_data['importe_bruto']

    def clean_importe_neto(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.importe_neto
        else:
            return self.cleaned_data['importe_neto']

    def clean_descuento(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.descuento
        else:
            return self.cleaned_data['descuento']

    def clean_vpe(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.vpe
        else:
            return self.cleaned_data['vpe']

    def clean_vpr(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.vpr
        else:
            return self.cleaned_data['vpr']

    def clean_vpuu(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.vpuu
        else:
            return self.cleaned_data['vpuu']

    def clean_usuario(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.usuario
        else:
            return self.cleaned_data['usuario']

    def clean_usuarioRep(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.usuarioRep
        else:
            return self.cleaned_data['usuarioRep']

    def clean_checkbox_sot(self):
        if self.instance and self.instance.estado in ['pagado', 'cancelado']:
            return self.instance.checkbox_sot
        else:
            return self.cleaned_data['checkbox_sot']

    def clean_centro_costos(self):
        if self.instance and self.instance.estado not in ['sin_facturar', 'no_pago']:
            return self.instance.centro_costos
        else:
            return self.cleaned_data['centro_costos']

    def clean_area_tematica(self):
        if self.instance and self.instance.estado not in ['sin_facturar', 'no_pago']:
            return self.instance.area_tematica
        else:
            return self.cleaned_data['area_tematica']

    def clean_horizonte(self):
        if self.instance and self.instance.estado not in ['sin_facturar', 'no_pago']:
            return self.instance.horizonte
        else:
            return self.cleaned_data['horizonte']

    class Meta:
        model = OTML
        fields = ['estado',
                  'codigo',
                  'fecha_realizado',
                  'importe_bruto',
                  'importe_neto',
                  'descuento',
                  'vpe',
                  'vpr',
                  'vpuu',
                  'usuario',
                  'usuarioRep',
                  'checkbox_sot',
                  'pdt',
                  'centro_costos',
                  'area_tematica',
                  'horizonte']

        error_messages = {
            'fecha_realizado': {
                'required': 'Campo obligatorio.',
            },
            'importe_bruto': {
                'required': 'Campo obligatorio.',
            },
            'usuarioRep': {
                'required': 'Campo obligatorio.',
            },
            'usuario': {
                'required': 'Campo obligatorio.',
            },
            'pdt': {
                'required': 'Campo obligatorio.',
            }
        }

        widgets = {
            'fecha_realizado': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'importe_bruto': forms.TextInput(),
        }


class SOTForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SOTForm, self).__init__(*args, **kwargs)
        # Restrinjo el area solicitante al area del usuario logueado
        groups = Group.objects.filter(user=user).values_list('name', 'name')
        choices = self.fields['solicitante'].choices
        if ('Administracion', 'Administracion') not in groups:
            self.fields['solicitante'].choices = list(set(choices) & set(groups))

        self.fields['codigo'].widget.attrs['class'] = 'OT_code'
        self.fields['codigo'].widget.attrs['form'] = 'SOTForm'
        self.fields['codigo'].widget.attrs['maxlength'] = '10'
        self.fields['importe_bruto'].widget.attrs['readonly'] = True
        self.fields['importe_neto'].widget.attrs['readonly'] = True
        if not self.instance or self.instance.estado == 'borrador':
            year = datetime.now().year
            self.fields['pdt'].queryset = PDT.objects.filter(anio=year) | PDT.objects.filter(anio__isnull=True)
        if self.instance:
            # Solo se deben poder crear SOTs a presupuestos aceptados y del area del usuario logueado
            userAreas = user.groups.values_list('name', flat=True)
            if 'Administracion' in userAreas:
                self.fields['presupuesto'].queryset = Presupuesto.objects.filter(estado__in=['aceptado', 'en_proceso_de_facturacion']).order_by('-id')
            else:
                ids = Turno.objects.filter(area__in=userAreas).values_list('presupuesto_id', flat=True)
                self.fields['presupuesto'].queryset = Presupuesto.objects.filter(id__in=ids, estado__in=['aceptado', 'en_proceso_de_facturacion']).order_by('-id')
            if self.instance.estado != 'borrador':
                for f in self.fields:
                    # Los campos importe bruto e importe neto son readonly en lugar de disabled asi
                    # se pueden actualizar con el boton por si quedaron en 0
                    if f == 'importe_neto' or f == 'importe_bruto':
                        self.fields[f].widget.attrs['readonly'] = True
                        self.fields[f].required = False
                    elif f not in ['firmada', 'fecha_envio_cc']:
                        self.fields[f].widget.attrs['disabled'] = True
                        self.fields[f].required = False

    def clean_presupuesto(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.presupuesto
        else:
            return self.cleaned_data['presupuesto']

    def clean_deudor(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.deudor
        else:
            return self.cleaned_data['deudor']

    def clean_usuario_final(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.usuario_final
        else:
            return self.cleaned_data['usuario_final']

    def clean_ejecutor(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.ejecutor
        else:
            return self.cleaned_data['ejecutor']

    def clean_importe_bruto(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.importe_bruto
        else:
            return self.cleaned_data['importe_bruto']

    def clean_importe_neto(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.importe_neto
        else:
            return self.cleaned_data['importe_neto']

    def clean_fecha_prevista(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.fecha_prevista
        else:
            return self.cleaned_data['fecha_prevista']

    def clean_fecha_envio_ut(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.fecha_envio_ut
        else:
            return self.cleaned_data['fecha_envio_ut']

    def clean_fecha_envio_cc(self):
        if self.instance and self.instance.estado not in ['borrador', 'pendiente']:
            return self.instance.fecha_envio_cc
        else:
            return self.cleaned_data['fecha_envio_cc']

    def clean_firmada(self):
        if self.instance and self.instance.estado not in ['borrador', 'pendiente']:
            return self.instance.firmada
        else:
            return self.cleaned_data['firmada']

    def clean_ot(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.ot
        else:
            return self.cleaned_data['ot']

    def clean_expediente(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.expediente
        else:
            return self.cleaned_data['expediente']

    def clean_descuento_fijo(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.descuento_fijo
        else:
            return self.cleaned_data['descuento_fijo']

    class Meta:
        model = SOT
        fields = ['estado',
                  'codigo',
                  'fecha_realizado',
                  'importe_bruto',
                  'importe_neto',
                  'descuento',
                  'fecha_prevista',
                  'deudor',
                  'ejecutor',
                  'usuario_final',
                  'ot',
                  'expediente',
                  'presupuesto',
                  'fecha_envio_ut',
                  'fecha_envio_cc',
                  'firmada',
                  'solicitante',
                  'descuento_fijo',
                  'pdt']

        error_messages = {
                'fecha_realizado': {
                    'required': 'Campo obligatorio.',
                },
                'fecha_prevista': {
                    'required': 'Campo obligatorio.',
                },
                'deudor': {
                    'required': 'Campo obligatorio.',
                },
                'ejecutor': {
                    'required': 'Campo obligatorio.',
                },
                'usuario_final': {
                    'required': 'Campo obligatorio.',
                },
                'presupuesto': {
                    'required': 'Campo obligatorio.',
                },
                'solicitante': {
                    'required': 'Campo obligatorio.',
                },
                'pdt': {
                    'required': 'Campo obligatorio.',
                }
            }

        widgets = {
                'fecha_realizado': forms.DateInput(attrs={'class': 'datepicker',
                                                          'readonly': True},),
                'fecha_envio_ut': forms.DateInput(attrs={'class': 'datepicker',
                                                          'readonly': True},),
                'fecha_envio_cc': forms.DateInput(attrs={'class': 'datepicker',
                                                          'readonly': True},),
                'fecha_prevista': forms.DateInput(attrs={'class': 'datepicker',
                                                          'readonly': True},),
                'importe_bruto': forms.TextInput(),
            }


class RUTForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(RUTForm, self).__init__(*args, **kwargs)
        # Restrinjo el area solicitante al area del usuario logueado
        groups = Group.objects.filter(user=user).values_list('name', 'name')
        choices = self.fields['solicitante'].choices
        if ('Administracion', 'Administracion') not in groups:
            self.fields['solicitante'].choices = list(set(choices) & set(groups))

        self.fields['codigo'].widget.attrs['class'] = 'OT_code'
        self.fields['codigo'].widget.attrs['form'] = 'RUTForm'
        self.fields['codigo'].widget.attrs['maxlength'] = '10'
        self.fields['importe_bruto'].widget.attrs['readonly'] = True
        self.fields['importe_neto'].widget.attrs['readonly'] = True
        if not self.instance or self.instance.estado == 'borrador':
            year = datetime.now().year
            self.fields['pdt'].queryset = PDT.objects.filter(anio=year) | PDT.objects.filter(anio__isnull=True)
        if self.instance:
            # Solo se deben poder crear RUTs a presupuestos aceptados y del area del usuario logueado
            userAreas = user.groups.values_list('name', flat=True)
            if 'Administracion' in userAreas:
                self.fields['presupuesto'].queryset = Presupuesto.objects.filter(estado__in=['aceptado', 'en_proceso_de_facturacion']).order_by('-id')
            else:
                ids = Turno.objects.filter(area__in=userAreas).values_list('presupuesto_id', flat=True)
                self.fields['presupuesto'].queryset = Presupuesto.objects.filter(id__in=ids, estado__in=['aceptado',
                                                                                                     'en_proceso_de_facturacion']).order_by('-id')
            if self.instance.estado != 'borrador':
                for f in self.fields:
                    # Los campos importe bruto e importe neto son readonly en lugar de disabled asi
                    # se pueden actualizar con el boton por si quedaron en 0
                    if f == 'importe_neto' or f == 'importe_bruto':
                        self.fields[f].widget.attrs['readonly'] = True
                        self.fields[f].required = False
                    elif f not in ['firmada', 'fecha_envio_cc']:
                        self.fields[f].widget.attrs['disabled'] = True
                        self.fields[f].required = False

    def clean_presupuesto(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.presupuesto
        else:
            return self.cleaned_data['presupuesto']

    def clean_codigo(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.codigo
        else:
            return self.cleaned_data['codigo']

    def clean_fecha_realizado(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.fecha_realizado
        else:
            return self.cleaned_data['fecha_realizado']

    def clean_importe_bruto(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.importe_bruto
        else:
            return self.cleaned_data['importe_bruto']

    def clean_importe_neto(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.importe_neto
        else:
            return self.cleaned_data['importe_neto']

    def clean_fecha_prevista(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.fecha_prevista
        else:
            return self.cleaned_data['fecha_prevista']

    def clean_deudor(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.deudor
        else:
            return self.cleaned_data['deudor']

    def clean_ejecutor(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.ejecutor
        else:
            return self.cleaned_data['ejecutor']

    def clean_solicitante(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.solicitante
        else:
            return self.cleaned_data['solicitante']

    def clean_fecha_envio_ut(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.fecha_envio_ut
        else:
            return self.cleaned_data['fecha_envio_ut']

    def clean_fecha_envio_cc(self):
        if self.instance and self.instance.estado not in ['borrador', 'pendiente']:
            return self.instance.fecha_envio_cc
        else:
            return self.cleaned_data['fecha_envio_cc']

    def clean_firmada(self):
        if self.instance and self.instance.estado not in ['borrador', 'pendiente']:
            return self.instance.firmada
        else:
            return self.cleaned_data['firmada']

    def clean_descuento_fijo(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.descuento_fijo
        else:
            return self.cleaned_data['descuento_fijo']

    class Meta:
        model = RUT

        fields = ['estado',
                  'codigo',
                  'fecha_realizado',
                  'fecha_prevista',
                  'importe_bruto',
                  'importe_neto',
                  'descuento',
                  'fecha_envio_ut',
                  'fecha_envio_cc',
                  'firmada',
                  'deudor',
                  'ejecutor',
                  'solicitante',
                  'presupuesto',
                  'descuento_fijo',
                  'pdt']

        error_messages = {
            'fecha_realizado': {
                'required': 'Campo obligatorio.',
            },

            'fecha_prevista': {
                'required': 'Campo obligatorio.',
            },
            'deudor': {
                'required': 'Campo obligatorio.',
            },
            'ejecutor': {
                'required': 'Campo obligatorio.',
            },
            'solicitante': {
                'required': 'Campo obligatorio.',
            },
            'presupuesto': {
                'required': 'Campo obligatorio.',
            },
            'pdt': {
                'required': 'Campo obligatorio.',
            }
        }

        widgets = {
            'fecha_realizado': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'fecha_prevista': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'fecha_envio_ut': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'fecha_envio_cc': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'importe_bruto': forms.TextInput(),
        }


class SIForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SIForm, self).__init__(*args, **kwargs)
        if not self.instance or self.instance.estado == 'borrador':
            year = datetime.now().year
            self.fields['pdt'].queryset = PDT.objects.filter(anio=year) | PDT.objects.filter(anio__isnull=True)
        # Restrinjo el area ejecutora al area del usuario logueado
        groups = Group.objects.filter(user=user).values_list('name', 'name')
        choices = self.fields['ejecutor'].choices
        self.fields['ejecutor'].choices = list(set(choices) & set(groups))

        self.fields['codigo'].widget.attrs['class'] = 'OT_code'
        self.fields['codigo'].widget.attrs['form'] = 'SIForm'
        if self.instance:
            if self.instance.estado != 'borrador':
                for f in self.fields:
                    self.fields[f].widget.attrs['disabled'] = True
                    self.fields[f].required = False

    def clean_codigo(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.codigo
        else:
            return self.cleaned_data['codigo']

    def clean_fecha_realizado(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.fecha_realizado
        else:
            return self.cleaned_data['fecha_realizado']

    def clean_solicitante(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.solicitante
        else:
            return self.cleaned_data['solicitante']

    def clean_ejecutor(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.ejecutor
        else:
            return self.cleaned_data['ejecutor']

    class Meta:
        model = SI

        fields = ['estado',
                  'codigo',
                  'fecha_realizado',
                  'solicitante',
                  'ejecutor',
                  'fecha_fin_real',
                  'pdt']

        error_messages = {
            'fecha_realizado': {
                'required': 'Campo obligatorio.',
            },
            'solicitante': {
                'required': 'Campo obligatorio.',
            },
            'ejecutor': {
                'required': 'Campo obligatorio.',
            },
            'pdt': {
                'required': 'Campo obligatorio.',
            }
        }

        widgets = {
            'fecha_realizado': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'importe_bruto': forms.TextInput(),
        }


class NestedGenericInlineFormset(BaseGenericInlineFormSet):
    """
    Custom formset that support initial data
    """

    def __init__(self, *args, **kwargs):
        super(NestedGenericInlineFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            if form.instance:
                form.fields['estado'].widget.attrs.update({'style': 'display: none'})
                if form.instance.estado == 'cancelada':
                    for field in form.fields:
                        # Con el id se rompe
                        if field != 'id':
                            form.fields[field].widget.attrs['disabled'] = True
                            form.fields[field].required = False
                    for nested in form.nested:
                        for nestedForm in nested.forms:
                            for field in nestedForm.fields:
                                if field != 'id':
                                    if field in ['comprobante_cobro', 'fecha']:
                                        nestedForm.fields[field].widget.attrs['disabled'] = True
                                    else:
                                        nestedForm.fields[field].widget.attrs['readonly'] = True
                                nestedForm.fields[field].required = False

    def add_fields(self, form, index):

        # allow the super class to create the fields as usual
        super(NestedGenericInlineFormset, self).add_fields(form, index)
        form.nested = []
        for i, nested_formset in enumerate(self.nested_formset_class):
            form.nested.append(nested_formset(
                instance=form.instance,
                data=form.data if self.is_bound else None,
                prefix='%s-%s' % (
                    form.prefix,
                    nested_formset.get_default_prefix(),
                ),
            ))

    def is_valid(self):

        is_valid = super(NestedGenericInlineFormset, self).is_valid()

        if self.is_bound and is_valid:
            # look at any nested formsets, as well
            for form in self.forms:
                if not self._should_delete_form(form):
                    for nested in form.nested:
                        is_valid &= nested.is_valid()
        return is_valid

    def save(self, commit=True):

        result = super(NestedGenericInlineFormset, self).save(commit=commit)

        for form in self.forms:
            if not self._should_delete_form(form):
                for nested in form.nested:
                    nested.save(commit=commit)
        return result


class Factura_LineaForm(forms.ModelForm):

    #def clean_numero(self):
        #if self.instance and self.instance.estado != 'cancelada':
            #return self.instance.numero
        #else:
            #return self.cleaned_data['numero']

    #def clean_fecha(self):
        #if self.instance and self.instance.estado != 'cancelada':
            #return self.instance.fecha
        #else:
            #return self.cleaned_data['fecha']

    #def clean_importe(self):
        #if self.instance and self.instance.estado != 'cancelada':
            #return self.instance.importe
        #else:
            #return self.cleaned_data['importe']

    class Meta:

        model = Factura
        fields = ['numero',
                  'fecha',
                  'estado',
                  'importe',
                  'fecha_aviso']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'fecha_aviso': forms.DateInput(attrs={'class': 'datepicker',
                                                           'readonly': True},),
            'importe': forms.TextInput(),
            }
        error_messages = {
            'numero': {
                'required': 'Campo obligatorio.',
            },
            'fecha': {
                'required': 'Campo obligatorio.',
            },
            'importe': {
                'required': 'Campo obligatorio.',
            },
        }


class Recibo_LineaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Recibo_LineaForm, self).__init__(*args, **kwargs)
    # El nro de presup no tiene que tener form-control
    #if self.instance and self.instance.factura_id:
        #if self.instance.factura.estado == 'cancelada':
        for f in self.fields:
            #self.fields[f].widget.attrs['disabled'] = True
            self.fields[f].required = False

    class Meta:

        model = Recibo
        fields = ['comprobante_cobro',
                  'numero',
                  'fecha',
                  'importe',
                  'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'importe': forms.TextInput(),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }
        error_messages = {
            'numero': {
                'required': 'Campo obligatorio.',
                'unique': 'Ya existe una factura con ese numero.',
            },
            'fecha': {
                'required': 'Campo obligatorio.',
            },
            'importe': {
                'required': 'Campo obligatorio.',
            },
            'comprobante_cobro': {
                'required': 'Campo obligatorio.',
            },
        }


def nested_formset_factory(child_model, grandchilds):

    parent_child = generic_inlineformset_factory(
        child_model,
        formset=NestedGenericInlineFormset,
        #min_num=1,
        extra=1,
        formfield_callback=bootstrap_format,
        form=Factura_LineaForm,
    )

    parent_child.nested_formset_class = []

    for (grandchild, g_form) in grandchilds:
        parent_child.nested_formset_class.append(inlineformset_factory(
            child_model,
            grandchild,
            min_num=1,
            extra=0,
            formfield_callback=bootstrap_format,
            form=g_form,
        ))

    return parent_child

Factura_LineaFormSet = nested_formset_factory(Factura, [(Recibo, Recibo_LineaForm)])


class Remito_LineaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Remito_LineaForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].required = False

    class Meta:

        model = Recibo
        fields = ['numero',
                  'fecha']

        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            }

#Remito_LineaFormSet = inlineformset_factory(OT,
#                                            Remito,
#                                            min_num=1,
#                                            extra=0,
#                                            formfield_callback=bootstrap_format,
#                                            form=Remito_LineaForm,
#                                            formset=BaseInlineFormSet,
#                                           )
Remito_LineaFormSet = generic_inlineformset_factory(Remito,
                                                    formset=BaseGenericInlineFormSet,
                                                    form=Remito_LineaForm,
                                                    min_num=1,
                                                    extra=0,
                                                    formfield_callback=bootstrap_format
                                                    )

class CustomInlineFormset(BaseGenericInlineFormSet):
    """
    Custom formset that support initial data
    """

    def __init__(self, *args, **kwargs):
        super(CustomInlineFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            ## Label del select de oferta tecnologica
            form.fields['ofertatec'].label_from_instance = lambda obj: "%s - %s - %s" \
                                                        % (obj.codigo, obj.subrubro, obj.detalle)
        if self.instance and self.instance.estado not in ['sin_facturar', 'borrador']:
            for form in self.forms:
                form.fields['ofertatec'].widget.attrs['disabled'] = True
                for field in form.fields:
                    if field != 'id':
                        form.fields[field].widget.attrs['readonly'] = True
                        form.fields[field].required = False

    #def add_fields(self, form, index):
        #super(CustomInlineFormset, self).add_fields(form, index)
        #form.fields['ofertatec'].queryset = OfertaTec.objects.filter(area=initArea)


class OT_LineaForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        res = super(OT_LineaForm, self).__init__(*args, **kwargs)
        self.fields['precio_total'].widget.attrs['readonly'] = True
        initial_val = ''
        if self.instance.pk and self.instance.ofertatec_old:
            initial_val = self.instance.ofertatec_old.detalle
        self.fields['ofertatec_old'].widget = AutoCompleteWidget(url=settings.DOMAIN+'ofertatec_autocomplete',
                                                                 initial_display=initial_val)
        return res


    def clean_precio_total(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.precio_total
        else:
            return self.cleaned_data['precio_total']

    class Meta:

        model = OT_Linea
        fields = ['ofertatec',
                  'ofertatec_old',
                  'codigo',
                  'precio',
                  'precio_total',
                  'cantidad',
                  'cant_horas',
                  'detalle',
                  'tipo_servicio',
                  'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3}),
            }
        error_messages = {
            'ofertatec': {
                'required': 'Campo obligatorio.',
            },
            'cantidad': {
                'required': 'Campo obligatorio.',
            },
            'precio': {
                'required': 'Campo obligatorio.',
            },
            'precio_total': {
                'required': 'Campo obligatorio.',
            },
        }


OT_LineaFormSet = generic_inlineformset_factory(OT_Linea,
                                                min_num=1,
                                                extra=0,
                                                formfield_callback=bootstrap_format,
                                                form=OT_LineaForm,
                                                formset=CustomInlineFormset,
                                               )


class Tarea_LineaForm(forms.ModelForm):

    class Meta:

        model = Tarea_Linea
        fields = ['tarea',
                  'horas',
                  'arancel']

        error_messages = {
            'tarea': {
                'required': 'Campo obligatorio.',
            },
            'horas': {
                'required': 'Campo obligatorio.',
            }
        }


Tarea_LineaFormSet = generic_inlineformset_factory(Tarea_Linea,
                                                   min_num=0,
                                                   max_num=9,
                                                   extra=1,
                                                   formfield_callback=bootstrap_format,
                                                   form=Tarea_LineaForm,
                                                   formset=BaseGenericInlineFormSet,
                                                  )


class Instrumento_LineaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Instrumento_LineaForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].required = False

    class Meta:

        model = Instrumento
        fields = ['detalle',
                  'fecha_llegada',
                  'nro_recepcion']

        widgets = {
            'fecha_llegada': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            }

Instrumento_LineaFormSet = inlineformset_factory(Presupuesto,
                                                Instrumento,
                                                min_num=1,
                                                extra=0,
                                                formfield_callback=bootstrap_format,
                                                form=Instrumento_LineaForm,
                                                formset=BaseInlineFormSet,
                                               )


class PresupuestoForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        # Filtro los centros de costos segun la region
        self.fields['centro_costos'].queryset = CentroDeCostos.objects.filter(region='CENTRO')
        # Traigo los datos del turno asociado si es que hay
        if self.instance and len(self.instance.turno_set.all()) > 0:
            turno = self.instance.turno_set.all()[0]                # Deberia haber solo un turno asociado asi que agarro el primero
            self.initial['centro_costos'] = turno.centro_costos.id if turno.centro_costos else ''
            self.initial['area_tematica'] = turno.area_tematica.id if turno.area_tematica else ''
            self.initial['horizonte'] = turno.horizonte
        # El nro de presup no tiene que tener form-control
        self.fields['codigo'].widget.attrs['class'] = 'presup_code'
        self.fields['codigo'].widget.attrs['form'] = 'presupForm'
        if self.instance and self.instance.estado != 'borrador':
            for f in self.fields:
                if (f not in editable_fields) or\
                   (self.instance.estado != 'aceptado'):
                    self.fields[f].widget.attrs['disabled'] = True
                    self.fields[f].required = False
        # Queryset contacto y direccion
        self.fields['contacto'].queryset = Contacto.objects.none()
        if not self.instance or self.instance.estado == 'borrador':
            year = datetime.now().year
            self.fields['pdt'].queryset = PDT.objects.filter(anio=year) | PDT.objects.filter(anio__isnull=True)
        if 'usuario' in self.data:
            try:
                usuario_id = int(self.data.get('usuario'))
                self.fields['contacto'].queryset = Contacto.objects.filter(usuario=usuario_id).order_by('nombre')
                self.fields['direccion'].queryset = DireccionUsuario.objects.filter(usuario=usuario_id).order_by('calle')
            except (ValueError, TypeError):
                pass    # Invalid input from the client, ignore and fallback to empty Contacto queryset
        elif self.instance.pk:
            self.fields['contacto'].queryset = self.instance.usuario.contacto_set.order_by('nombre')
            self.fields['direccion'].queryset = self.instance.usuario.direccionusuario_set.order_by('calle')

    def clean_codigo(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.codigo
        else:
            if len(self.cleaned_data['codigo']) != 5:
                msg = "Se esperan 5 dígitos."
                self._errors['codigo'] = self.error_class([msg])
            return self.cleaned_data['codigo']

    def clean_fecha_realizado(self):
        if self.instance and self.instance.estado not in \
                           ('borrador', 'aceptado'):
            return self.instance.fecha_realizado
        else:
            return self.cleaned_data['fecha_realizado']

    def clean_fecha_solicitado(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.fecha_solicitado
        else:
            return self.cleaned_data['fecha_solicitado']

    def clean_usuario(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.usuario
        else:
            return self.cleaned_data['usuario']

    def clean_fecha_aceptado(self):
        if self.instance and self.instance.estado not in \
                           ('borrador', 'aceptado'):
            return self.instance.fecha_aceptado
        else:
            return self.cleaned_data['fecha_aceptado']

    def clean_estado(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.estado
        else:
            return self.cleaned_data['estado']

    def clean_centro_costos(self):
        if self.instance and self.instance.estado not in ['borrador', 'aceptado']:
            return self.instance.centro_costos
        else:
            return self.cleaned_data['centro_costos']

    def clean_area_tematica(self):
        if self.instance and self.instance.estado not in ['borrador', 'aceptado']:
            return self.instance.area_tematica
        else:
            return self.cleaned_data['area_tematica']

    def clean_horizonte(self):
        if self.instance and self.instance.estado not in ['borrador', 'aceptado']:
            return self.instance.horizonte
        else:
            return self.cleaned_data['horizonte']
    def clean_nro_presea(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.nro_presea
        else:
            return self.cleaned_data['nro_presea']

    def clean(self):
        cleaned_data = super(PresupuestoForm, self).clean()
        fecha_aceptado = cleaned_data.get('fecha_aceptado')
        fecha_realizado = cleaned_data.get('fecha_realizado')
        if fecha_aceptado and not fecha_realizado:
            msg = "El campo no puede ser vacio."
            self._errors['fecha_realizado'] = self.error_class([msg])
            del cleaned_data['fecha_aceptado']
        return cleaned_data

    class Meta:
        model = Presupuesto
        fields = ['codigo',
                  'nro_presea',
                  'fecha_solicitado',
                  'usuario',
                  'direccion',
                  'contacto',
                  'fecha_realizado',
                  'fecha_aceptado',
                  'estado',
                  'tipo',
                  'pdt',
                  'centro_costos',
                  'area_tematica',
                  'horizonte']

        error_messages = {
            'fecha_solicitado': {
                'required': 'Campo obligatorio.',
                'invalid': 'Fecha invalida.',
            },
            'usuario': {
                'required': 'Campo obligatorio.',
            },
            'fecha_realizado': {
                'required': 'Campo obligatorio.',
                'invalid': 'Fecha invalida.',
            },
            'fecha_aceptado': {
                'required': 'Campo obligatorio.',
                'invalid': 'Fecha invalida.',
            },
            'pdt': {
                'required': 'Campo obligatorio.',
            },
        }
        widgets = {
                'fecha_solicitado': forms.DateInput(attrs={'class':
                                                               'datepicker',
                                                           'readonly': True},),
                'fecha_realizado': forms.DateInput(attrs={'class':
                                                               'datepicker',
                                                          'readonly': True},),
                'fecha_aceptado': forms.DateInput(attrs={'class':
                                                               'datepicker',
                                                         'readonly': True},),
                'usuario': RelatedFieldWidgetCanAdd(Usuario,
                                                    add_related_url="adm:usuarios-create-modal",
                                                    view_related_url="adm:usuarios-update-modal"),
                'direccion': NestedRelatedFieldWidgetCanAdd(Usuario,
                                                           DireccionUsuario,
                                                           add_related_url="adm:direcciones-create-modal"),
                'contacto': NestedRelatedFieldWidgetCanAdd(Usuario,
                                                           Contacto,
                                                           add_related_url="adm:contactos-create-modal",
                                                           view_related_url="adm:contactos-update-modal"),
            }


class OfertaTecForm(forms.ModelForm):
    # Para cambiar el widget de los dateFields
    formfield_callback = bootstrap_format

    def clean_rubro(self):
        return self.cleaned_data['rubro'].upper()

    def clean_subrubro(self):
        return self.cleaned_data['subrubro'].upper()

    def clean_tipo_servicio(self):
        return self.cleaned_data['tipo_servicio'].upper()

    def clean_area(self):
        return self.cleaned_data['area'].upper()

    class Meta:
        model = OfertaTec
        fields = ['proveedor',
                  'codigo',
                  'rubro',
                  'subrubro',
                  'tipo_servicio',
                  'area',
                  'detalle',
                  'precio']
        error_messages = {
            'proveedor': {
                'required': 'Campo obligatorio.',
                'invalid': 'Se requieren 3 digitos.',
            },
            'codigo': {
                'required': 'Campo obligatorio.',
                'invalid': 'Se requieren 14 digitos.',
                'max_length': 'Largo permitido excedido.',
            },
            'rubro': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
            },
            'subrubro': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
            },
            'tipo_servicio': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
            },
            'area': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
            },
            'detalle': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
            },
            'precio': {
                'required': 'Campo obligatorio.',
                'invalid': 'El campo debe ser numerico.',
            },
        }


class UsuarioForm(forms.ModelForm):
    # Para cambiar el widget de los dateFields
    formfield_callback = bootstrap_format

    def clean_nombre(self):
        return self.cleaned_data['nombre'].upper()

    def clean_rubro(self):
        return self.cleaned_data['rubro'].upper()

    class Meta:
        model = Usuario
        fields = ['nro_usuario',
                  'nombre',
                  'cuit',
                  'mail',
                  'rubro']
        error_messages = {
            'nro_usuario': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
                'invalid': 'Se requieren 5 digitos.'
            },
            'nombre': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.'
            },
            'cuit': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
                'invalid': 'Se requieren 11 digitos.'
            },
            'mail': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
            },
            'rubro': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
            },
        }


class ContactoForm(forms.ModelForm):
    formfield_callback = base_bootstrap_format

    class Meta:
        model = Contacto
        fields = ['usuario',
                  'nombre',
                  'telefono',
                  'mail']
        error_messages = {
            'nombre': {
                'required': 'Campo obligatorio.',
            },
            'mail': {
                'required': 'Campo obligatorio.',
            },
        }


class PDTForm(forms.ModelForm):
    formfield_callback = base_bootstrap_format

    def __init__(self, *args, **kwargs):
        super(PDTForm, self).__init__(*args, **kwargs)
        self.fields['agentes'].queryset = User.objects.exclude(username='admin').exclude(is_active=False).order_by('first_name')
        year = datetime.now().year
        if self.instance and int(self.instance.anio) < int(year):
            for f in self.fields:
                self.fields[f].widget.attrs['disabled'] = True
                self.fields[f].required = False

    class Meta:
        model = PDT
        fields = ['contribucion',
                  'anio',
                  'tipo',
                  'codigo',
                  'nombre',
                  'cantidad_servicios',
                  'cantidad_contratos',
                  'facturacion_prevista',
                  'generacion_neta',
                  'agentes']

        widgets = {
            'nombre': forms.Textarea(attrs={'rows': 2}),
            'agentes': forms.CheckboxSelectMultiple(),
        }

        error_messages = {
            'nombre': {
                'required': 'Campo obligatorio.',
            },
            'codigo': {
                'required': 'Campo obligatorio.',
            },
            'agentes': {
                'required': 'Campo obligatorio.',
            },
            'tipo': {
                'required': 'Campo obligatorio.',
            },
        }


class ContactoInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(ContactoInlineFormset, self).__init__(*args, **kwargs)
        if self.total_form_count() > 1:
            self.extra = 0


class Contacto_LineaForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = ['usuario',
                  'nombre',
                  'telefono',
                  'mail']

        error_messages = {
            'nombre': {
                'required': 'Campo obligatorio.',
            },
            'mail': {
                'required': 'Campo obligatorio.',
            },
        }


Contacto_LineaFormSet = inlineformset_factory(Usuario,
                                              Contacto,
                                              min_num=0,
                                              extra=1,
                                              formfield_callback=base_bootstrap_format,
                                              form=Contacto_LineaForm,
                                              formset=ContactoInlineFormset)


class DireccionForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    def __init__(self, *args, **kwargs):
        super(DireccionForm, self).__init__(*args, **kwargs)
        # Queryset localidad
        self.fields['localidad'].queryset = Localidad.objects.none()
        provincia_key = self.prefix + '-provincia' if self.prefix else 'provincia'
        if provincia_key in self.data:
            try:
                provincia_id = int(self.data.get(provincia_key))
                self.fields['localidad'].queryset = Localidad.objects.filter(provincia=provincia_id).order_by(
                    'nombre')
            except (ValueError, TypeError):
                pass  # Invalid input from the client, ignore and fallback to empty Localidad queryset
        elif self.instance.pk:
            self.fields['localidad'].queryset = self.instance.provincia.localidad_set.order_by('nombre')


    class Meta:
        model = DireccionUsuario
        fields = ['usuario',
                  'calle',
                  'numero',
                  'piso',
                  'provincia',
                  'localidad']

        error_messages = {
            'calle': {
                'required': 'Campo obligatorio.',
            },
            'numero': {
                'required': 'Campo obligatorio.',
            },
            'provincia': {
                'required': 'Campo obligatorio.',
            },
            'localidad': {
                'required': 'Campo obligatorio.',
            },
        }


class DireccionUsuarioInlineFormset(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(DireccionUsuarioInlineFormset, self).__init__(*args, **kwargs)
        if self.total_form_count() > 1:
            self.extra = 0


Direccion_LineaFormSet = inlineformset_factory(Usuario,
                                               DireccionUsuario,
                                               min_num=0,
                                               extra=1,
                                               formfield_callback=base_bootstrap_format,
                                               form=DireccionForm,
                                               formset=DireccionUsuarioInlineFormset)
