# -*- coding: utf-8 -*-
from django import forms
from .models import Presupuesto, OfertaTec, Usuario

editable_fields = ['fecha_instrumento', 'fecha_realizado', 'fecha_aceptado', 'nro_recepcion', 'asistencia', 'calibracion', 'in_situ', 'lia']


def bootstrap_format(f, **kwargs):
    formfield = f.formfield(**kwargs)
    # Uppercase para usuario y ofertatec
    if f.name in ['nombre', 'rubro', 'subrubro', 'tipo_servicio', 'area']:
        formfield.widget.attrs.update({'style': 'text-transform: uppercase'})
    tmp = formfield.widget.attrs.get('class') or ''
    formfield.widget.attrs.update({'class': 'form-control ' + tmp})
    return formfield


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
        if self.instance and self.instance.estado in \
                           ('finalizado', 'cancelado'):
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

