# -*- coding: utf-8 -*-
from django import forms
from adm.models import OfertaTec, Presupuesto, SI
from .models import Turno, OfertaTec_Linea
from django.forms.models import inlineformset_factory
from django.forms import formsets
from django.forms.models import BaseInlineFormSet

initArea = ''


def bootstrap_format(f, **kwargs):
    formfield = f.formfield(**kwargs)
    tmp = formfield.widget.attrs.get('class') or ''
    formfield.widget.attrs.update({'class': 'form-control ' + tmp})
    if f.name == 'observaciones':
        formfield.widget.attrs.update({'rows': '1', 'cols': '40'})
    #if f.name == 'ofertatec':
        #formfield.widget.attrs.update({'onchange': 'javascript:onchange_ofertatec()'})
    #if f.name == 'ofertatec':
        #formfield.widget.attrs.update({'class': 'form-control chosen-select' + tmp})
        #formfield.widget.attrs.update({'multiple': 1})
    return formfield


class TurnoForm(forms.ModelForm):
    formfield_callback = bootstrap_format
    isRev = False

    def __init__(self, *args, **kwargs):
        if 'revision' in kwargs:
            self.isRev = kwargs.pop('revision')
        else:
            self.isRev = False
        super(TurnoForm, self).__init__(*args, **kwargs)
        global initArea
        if 'area' in kwargs['initial']:
            initArea = kwargs['initial']['area']
        elif self.instance:
            initArea = self.instance.area
        self.fields['area'].widget.attrs['style'] = "visibility:hidden"
        if self.instance and self.isRev:
            if self.instance.estado != 'en_espera':
                # Si estoy revisionando solo dejo readonly el presupuesto y la SI
                self.fields['presupuesto'].widget.attrs['disabled'] = True
                self.fields['presupuesto'].required = False
                self.fields['si'].widget.attrs['disabled'] = True
                self.fields['si'].required = False
        else:
            if self.instance and self.instance.estado == 'en_espera':
                # Filtro los presupuestos que no estan en borrador
                self.fields['presupuesto'].queryset = Presupuesto.objects.filter(estado='borrador')
                # Filtro las solicitudes internas que corresponden al lab actual
                self.fields['si'].queryset = SI.objects.filter(ejecutor=initArea, estado__in=['borrador', 'pendiente'])
            else:
                for f in self.fields:
                    self.fields[f].widget.attrs['disabled'] = True
                    self.fields[f].required = False

    def clean(self):
        cleaned_data = self.cleaned_data
        presup = cleaned_data.get('presupuesto')
        if presup:
            if presup.estado not in ['borrador', 'aceptado']:
                msg = "El presupuesto seleccionado ya ha sido finalizado o\
                       se encuentra cancelado"
                self._errors['presupuesto'] = self.error_class([msg])
                del cleaned_data['presupuesto']
            else:
                # Cambio el estado del turno segun el presupuesto seleccionado
                if presup.estado == 'borrador':
                    cleaned_data['estado'] = 'en_espera'
                elif presup.estado == 'aceptado':
                    cleaned_data['estado'] = 'activo'
        return cleaned_data

    def clean_presupuesto(self):
        if self.fields['presupuesto'].widget.attrs.get('disabled', False):
            return self.instance.presupuesto
        else:
            return self.cleaned_data['presupuesto']

    def clean_si(self):
        if self.fields['si'].widget.attrs.get('disabled', False):
            return self.instance.si
        else:
            return self.cleaned_data['si']

    def clean_fecha_inicio(self):
        if self.fields['fecha_inicio'].widget.attrs.get('disabled', False):
            return self.instance.fecha_inicio
        else:
            return self.cleaned_data['fecha_inicio']

    def clean_fecha_fin(self):
        if self.fields['fecha_fin'].widget.attrs.get('disabled', False):
            return self.instance.fecha_fin
        else:
            return self.cleaned_data['fecha_fin']

    def clean_estado(self):
        if self.fields['estado'].widget.attrs.get('disabled', False):
            return self.instance.estado
        else:
            return self.cleaned_data['estado']

    def clean_area(self):
        if self.fields['area'].widget.attrs.get('disabled', False):
            return self.instance.area
        else:
            return self.cleaned_data['area']

    class Meta:

        model = Turno
        fields = ['presupuesto',
                  'si',
                  'fecha_inicio',
                  'fecha_fin',
                  'estado',
                  'area']
        error_messages = {
            'fecha_inicio': {
                'required': 'Campo obligatorio.',
                'invalid': 'Fecha invalida.',
            },
            'fecha_fin': {
                'required': 'Campo obligatorio.',
                'invalid': 'Fecha invalida.',
            },
        }
        widgets = {
                'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker',
                                                       'readonly': True}),
                'fecha_fin': forms.DateInput(attrs={'class': 'datepicker',
                                                    'readonly': True}),
            }


class CustomInlineFormset(BaseInlineFormSet):
    """
    Custom formset that support initial data
    """

    def __init__(self, *args, **kwargs):
        if 'revision' in kwargs:
            isRev = kwargs.pop('revision')
        else:
            isRev = False
        super(CustomInlineFormset, self).__init__(*args, **kwargs)
        ## Label del select de oferta tecnologica
        for form in self.forms:
            form.fields['ofertatec'].label_from_instance = lambda obj: "%s %s" \
                                                        % (obj.codigo, obj.detalle)
        if self.instance:
            if isRev:
                return
            elif self.instance.estado != 'en_espera':
                for form in self.forms:
                    for field in form.fields:
                        if field != 'id':
                            form.fields[field].widget.attrs['disabled'] = True
                            form.fields[field].required = False

    def add_fields(self, form, index):
        super(CustomInlineFormset, self).add_fields(form, index)
        if initArea == 'TICS':
            form.fields['ofertatec'].queryset = OfertaTec.objects.filter(area__in=['DES', 'TODAS'])
        else:
            form.fields['ofertatec'].queryset = OfertaTec.objects.filter(area__in=[initArea, 'TODAS'])


class OfertaTec_LineaForm(forms.ModelForm):

    def clean_ofertatec(self):
        if self.fields['ofertatec'].widget.attrs.get('disabled', False):
            return self.instance.ofertatec
        else:
            return self.cleaned_data['ofertatec']

    def clean_codigo(self):
        if self.fields['codigo'].widget.attrs.get('disabled', False):
            return self.instance.codigo
        else:
            return self.cleaned_data['codigo']

    def clean_precio(self):
        if self.fields['precio'].widget.attrs.get('disabled', False):
            return self.instance.precio
        else:
            return self.cleaned_data['precio']

    def clean_precio_total(self):
        if self.fields['precio_total'].widget.attrs.get('disabled', False):
            return self.instance.precio_total
        else:
            return self.cleaned_data['precio_total']

    def clean_cantidad(self):
        if self.fields['cantidad'].widget.attrs.get('disabled', False):
            return self.instance.cantidad
        else:
            return self.cleaned_data['cantidad']

    def clean_detalle(self):
        if self.fields['detalle'].widget.attrs.get('disabled', False):
            return self.instance.detalle
        else:
            return self.cleaned_data['detalle']

    def clean_tipo_servicio(self):
        if self.fields['tipo_servicio'].widget.attrs.get('disabled', False):
            return self.instance.tipo_servicio
        else:
            return self.cleaned_data['tipo_servicio']

    class Meta:

        model = OfertaTec_Linea
        fields = ['ofertatec',
                  'codigo',
                  'precio',
                  'precio_total',
                  'cantidad',
                  'cant_horas',
                  'observaciones',
                  'turno',
                  'detalle',
                  'tipo_servicio']
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
        }


OfertaTec_LineaFormSet = inlineformset_factory(Turno,
                                               OfertaTec_Linea,
                                               min_num=1,
                                               extra=0,
                                               formfield_callback=bootstrap_format,
                                               form=OfertaTec_LineaForm,
                                               formset=CustomInlineFormset,
                                               )
