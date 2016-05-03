# -*- coding: utf-8 -*-
from django import forms
from .models import Presupuesto, OfertaTec, Usuario, OT, Factura, Recibo
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet

editable_fields = ['fecha_instrumento', 'fecha_realizado', 'nro_recepcion', 'asistencia', 'calibracion', 'in_situ', 'lia']


def bootstrap_format(f, **kwargs):
    formfield = f.formfield(**kwargs)
    # Uppercase para usuario y ofertatec
    if f.name in ['nombre', 'rubro', 'subrubro', 'tipo_servicio', 'area']:
        formfield.widget.attrs.update({'style': 'text-transform: uppercase'})
    tmp = formfield.widget.attrs.get('class') or ''
    formfield.widget.attrs.update({'class': 'form-control ' + tmp})
    return formfield


class OTForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    def __init__(self, *args, **kwargs):
        super(OTForm, self).__init__(*args, **kwargs)
        # El nro de presup no tiene que tener form-control
        self.fields['codigo'].widget.attrs['class'] = 'OT_code'
        self.fields['codigo'].widget.attrs['form'] = 'OTForm'
        if self.instance:
            if self.instance.estado in ['sin_facturar']:
                # Filtro los presupuestos que no estan finalizados
                self.fields['presupuesto'].queryset = Presupuesto.objects.filter(estado='finalizado')
            if self.instance.estado != 'sin_facturar':
                for f in self.fields:
                    self.fields[f].widget.attrs['disabled'] = True
                    self.fields[f].required = False

    def clean_codigo(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.codigo
        else:
            return self.cleaned_data['codigo']

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

    def clean_importe(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.importe
        else:
            return self.cleaned_data['importe']

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
                  'fecha_aviso',
                  'importe']
        widgets = {
            'fecha_realizado': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'fecha_aviso': forms.DateInput(attrs={'class': 'datepicker',
                                                  'readonly': True},),
            }
        error_messages = {
            'presupuesto': {
                'required': 'Campo obligatorio.',
            },
            'fecha_realizado': {
                'required': 'Campo obligatorio.',
            },
            'importe': {
                'required': 'Campo obligatorio.',
            },
        }


class NestedInlineFormset(BaseInlineFormSet):
    """
    Custom formset that support initial data
    """

    def __init__(self, *args, **kwargs):
        super(NestedInlineFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            if self.instance and self.instance.estado in ['pagado', 'cancelado']:
                for field in form.fields:
                    form.fields[field].widget.attrs['disabled'] = True
                    form.fields[field].required = False

    def add_fields(self, form, index):

        # allow the super class to create the fields as usual
        super(NestedInlineFormset, self).add_fields(form, index)
        #import pdb; pdb.set_trace()
        form.nested = self.nested_formset_class(
            instance=form.instance,
            data=form.data if self.is_bound else None,
            prefix='%s-%s' % (
                form.prefix,
                self.nested_formset_class.get_default_prefix(),
            ),
        )
        #import pdb; pdb.set_trace()

    def is_valid(self):

        result = super(NestedInlineFormset, self).is_valid()

        if self.is_bound:
            #import pdb; pdb.set_trace()
            # look at any nested formsets, as well
            for form in self.forms:
                if not self._should_delete_form(form):
                    result = result and form.nested.is_valid()
        return result

    def save(self, commit=True):

        result = super(NestedInlineFormset, self).save(commit=commit)

        for form in self.forms:
            if not self._should_delete_form(form):
                form.nested.save(commit=commit)

        return result


class Factura_LineaForm(forms.ModelForm):

    class Meta:

        model = Factura
        fields = ['numero',
                  'fecha',
                  'importe']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
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

    class Meta:

        model = Recibo
        fields = ['comprobante_cobro',
                  'numero',
                  'fecha',
                  'importe']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
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
        }


def nested_formset_factory(parent_model, child_model, grandchild_model):

    parent_child = inlineformset_factory(
        parent_model,
        child_model,
        formset=NestedInlineFormset,
        extra=1,
        formfield_callback=bootstrap_format,
        form=Factura_LineaForm,
    )

    parent_child.nested_formset_class = inlineformset_factory(
        child_model,
        grandchild_model,
        extra=1,
        formfield_callback=bootstrap_format,
        form=Recibo_LineaForm,
    )

    return parent_child

Factura_LineaFormSet = nested_formset_factory(OT, Factura, Recibo)


class PresupuestoForm(forms.ModelForm):
    formfield_callback = bootstrap_format

    __fecha_instrumento_orig = None

    def __init__(self, *args, **kwargs):
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        # El nro de presup no tiene que tener form-control
        self.fields['codigo'].widget.attrs['class'] = 'presup_code'
        self.fields['codigo'].widget.attrs['form'] = 'presupForm'
        self.fields['asistencia'].widget.attrs['class'] = ''
        self.fields['calibracion'].widget.attrs['class'] = ''
        self.fields['in_situ'].widget.attrs['class'] = ''
        self.fields['lia'].widget.attrs['class'] = ''
        if self.instance and self.instance.estado != 'borrador':
            for f in self.fields:
                # fecha_instrumento' debe ser el unico campo editable en estado
                # 'aceptado'
                if (f not in editable_fields) or\
                   (self.instance.estado != 'aceptado'):
                    self.fields[f].widget.attrs['disabled'] = True
                    self.fields[f].required = False

    def clean_codigo(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.codigo
        else:
            if len(self.cleaned_data['codigo']) != 5:
                msg = "Se esperan 5 dígitos."
                self._errors['codigo'] = self.error_class([msg])
            return self.cleaned_data['codigo']

    def clean_fecha_realizado(self):
        if self.instance and self.instance.estado in \
                           ('finalizado', 'cancelado'):
            return self.instance.fecha_realizado
        else:
            return self.cleaned_data['fecha_realizado']

    def clean_fecha_instrumento(self):
        if self.instance and self.instance.estado in \
                           ('finalizado', 'cancelado'):
            return self.instance.fecha_instrumento
        else:
            return self.cleaned_data['fecha_instrumento']

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
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.fecha_aceptado
        else:
            return self.cleaned_data['fecha_aceptado']

    def clean_estado(self):
        if self.instance and self.instance.estado != 'borrador':
            return self.instance.estado
        else:
            return self.cleaned_data['estado']

    def clean_nro_recepcion(self):
        if self.instance and self.instance.estado in \
                           ('finalizado', 'cancelado'):
            return self.instance.nro_recepcion
        else:
            return self.cleaned_data['nro_recepcion']

    #def clean_asistencia(self):
        #if self.instance and self.instance.estado != 'borrador':
            #return self.instance.asistencia
        #else:
            #return self.cleaned_data['asistencia']

    #def clean_calibracion(self):
        #if self.instance and self.instance.estado != 'borrador':
            #return self.instance.calibracion
        #else:
            #return self.cleaned_data['calibracion']

    #def clean_in_situ(self):
        #if self.instance and self.instance.estado != 'borrador':
            #return self.instance.in_situ
        #else:
            #return self.cleaned_data['in_situ']

    #def clean_lia(self):
        #if self.instance and self.instance.estado != 'borrador':
            #return self.instance.lia
        #else:
            #return self.cleaned_data['lia']

    def clean(self):
        #cleaned_data = self.cleaned_data
        cleaned_data = super(PresupuestoForm, self).clean()
        fecha_aceptado = cleaned_data.get('fecha_aceptado')
        fecha_realizado = cleaned_data.get('fecha_realizado')
        if fecha_aceptado:
            if fecha_realizado:
                self.instance._toState_aceptado()
                cleaned_data['estado'] = 'aceptado'
            else:
                msg = "El campo no puede ser vacio."
                self._errors['fecha_realizado'] = self.error_class([msg])
                del cleaned_data['fecha_aceptado']
        return cleaned_data

    class Meta:
        model = Presupuesto
        fields = ['codigo',
                  'fecha_solicitado',
                  'usuario',
                  'fecha_realizado',
                  'fecha_aceptado',
                  'fecha_instrumento',
                  'estado',
                  'nro_recepcion',
                  'asistencia',
                  'calibracion',
                  'in_situ',
                  'lia']

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
            'fecha_instrumento': {
                'required': 'Campo obligatorio.',
                'invalid': 'Fecha invalida.',
            },
            'nro_recepcion': {
                'required': 'Campo obligatorio.',
                'max_length': 'Largo permitido excedido.',
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
                'fecha_instrumento': forms.DateInput(attrs={'class':
                                                               'datepicker',
                                                            'readonly': True},),
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

#class OfertaTec_LineaForm(forms.ModelForm):

