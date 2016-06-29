# -*- coding: utf-8 -*-
from django import forms
from adm.models import OfertaTec, Presupuesto
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

    def __init__(self, *args, **kwargs):
        super(TurnoForm, self).__init__(*args, **kwargs)

        global initArea
        if 'area' in kwargs['initial']:
            initArea = kwargs['initial']['area']
        elif self.instance:
            initArea = self.instance.area

        #import pdb; pdb.set_trace()
        if self.instance and self.instance.estado == 'en_espera':
            # Filtro los presupuestos que no estan en borrador
            self.fields['presupuesto'].queryset = Presupuesto.objects.filter(estado='borrador')
        self.fields['area'].widget.attrs['style'] = "visibility:hidden"
        if self.instance and self.instance.estado in \
                 ('finalizado', 'cancelado'):
            for f in self.fields:
                self.fields[f].widget.attrs['disabled'] = True
                self.fields[f].required = False
        if self.instance and self.instance.estado != 'en_espera':
            self.fields['presupuesto'].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        presup = cleaned_data.get('presupuesto')
        if presup:
            if presup.estado not in ['borrador', 'aceptado']:
                msg = "El presupuesto seleccionado ya ha sido finalizado o\
                       se encuentra cancelado"
                self._errors['presupuesto'] = self.error_class([msg])
                del cleaned_data['presupuesto']
            elif presup.get_turno_activo() and\
                    presup.get_turno_activo() != self.instance:
                    msg = "El presupuesto seleccionado ya tiene un turno\
                               activo/finalizado asociado"
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
        if self.instance and self.instance.estado in \
                 ('activo', 'finalizado', 'cancelado'):
            return self.instance.presupuesto
        else:
            return self.cleaned_data['presupuesto']

    def clean_fecha_inicio(self):
        if self.instance and self.instance.estado in \
                 ('finalizado', 'cancelado'):
            return self.instance.fecha_inicio
        else:
            return self.cleaned_data['fecha_inicio']

    def clean_fecha_fin(self):
        if self.instance and self.instance.estado in \
                 ('finalizado', 'cancelado'):
            return self.instance.fecha_fin
        else:
            return self.cleaned_data['fecha_fin']

    def clean_estado(self):
        if self.instance and self.instance.estado in \
                 ('finalizado', 'cancelado'):
            return self.instance.estado
        else:
            return self.cleaned_data['estado']

    def clean_area(self):
        if self.instance and self.instance.estado in \
                 ('finalizado', 'cancelado'):
            return self.instance.estado
        else:
            return self.cleaned_data['area']

    class Meta:

        model = Turno
        fields = ['presupuesto',
                  'fecha_inicio',
                  'fecha_fin',
                  'estado',
                  'area']
        error_messages = {
            'presupuesto': {
                'required': 'Campo obligatorio.',
            },
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
        super(CustomInlineFormset, self).__init__(*args, **kwargs)

        for form in self.forms:
            ## Label del select de oferta tecnologica
            form.fields['ofertatec'].label_from_instance = lambda obj: "%s %s" \
                                                        % (obj.codigo, obj.detalle)
        if self.instance and self.instance.estado in \
                 ('finalizado', 'cancelado'):
            for form in self.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs['disabled'] = True
                    form.fields[field].required = False

    def add_fields(self, form, index):
        super(CustomInlineFormset, self).add_fields(form, index)
        form.fields['ofertatec'].queryset = OfertaTec.objects.filter(area=initArea)


class OfertaTec_LineaForm(forms.ModelForm):

    class Meta:

        model = OfertaTec_Linea
        fields = ['ofertatec',
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
