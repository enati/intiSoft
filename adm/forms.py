# -*- coding: utf-8 -*-
from django import forms
from .models import Presupuesto, OfertaTec, Usuario, Contrato, OT, OTML, Factura, Recibo, Remito, OT_Linea
from django.contrib.contenttypes.forms import generic_inlineformset_factory, BaseGenericInlineFormSet
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms.forms import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError

editable_fields = ['fecha_instrumento', 'fecha_realizado', 'fecha_aceptado', 'nro_recepcion', 'asistencia', 'calibracion', 'in_situ', 'lia']


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
                # Solo se deben poder crear OTS a presupuestos aceptados
                self.fields['presupuesto'].queryset = \
                    Presupuesto.objects.filter(estado__in=['aceptado', 'en_proceso_de_facturacion']).order_by('-id')
            if self.instance.estado != 'sin_facturar':
                for f in self.fields:
                    if f != 'fecha_aviso':
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
                  'descuento']

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
        self.fields['codigo'].widget.attrs['class'] = 'OT_code'
        self.fields['codigo'].widget.attrs['form'] = 'OTMLForm'
        if self.instance:
            if self.instance.estado != 'sin_facturar':
                for f in self.fields:
                    if f != 'fecha_aviso':
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

    def clean_vpu(self):
        if self.instance and self.instance.estado != 'sin_facturar':
            return self.instance.vpu
        else:
            return self.cleaned_data['vpu']

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

    class Meta:
        model = OTML
        fields = ['estado',
                  'codigo',
                  'fecha_realizado',
                  'importe_bruto',
                  'importe_neto',
                  'descuento',
                  'vpe',
                  'vpu',
                  'vpuu',
                  'usuario',
                  'usuarioRep']

        error_messages = {
            'fecha_realizado': {
                'required': 'Campo obligatorio.',
            },
            'importe_bruto': {
                'required': 'Campo obligatorio.',
            },
        }

        widgets = {
            'fecha_realizado': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'vpu': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'vpuu': forms.DateInput(attrs={'class': 'datepicker',
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

        result = super(NestedGenericInlineFormset, self).is_valid()

        if self.is_bound:
            #import pdb; pdb.set_trace()
            # look at any nested formsets, as well
            for form in self.forms:
                if not self._should_delete_form(form):
                    result = True
                    for nested in form.nested:
                        result &= nested.is_valid()
        return result

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
                  'importe']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker',
                                                      'readonly': True},),
            'importe': forms.TextInput(),
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

Remito_LineaFormSet = inlineformset_factory(OT,
                                            Remito,
                                            min_num=1,
                                            extra=0,
                                            formfield_callback=bootstrap_format,
                                            form=Remito_LineaForm,
                                            formset=BaseInlineFormSet,
                                           )


class CustomInlineFormset(BaseGenericInlineFormSet):
    """
    Custom formset that support initial data
    """

    def __init__(self, *args, **kwargs):
        super(CustomInlineFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            ## Label del select de oferta tecnologica
            form.fields['ofertatec'].label_from_instance = lambda obj: "%s %s" \
                                                        % (obj.codigo, obj.detalle)
        if self.instance and self.instance.estado != 'sin_facturar':
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

    class Meta:

        model = OT_Linea
        fields = ['ofertatec',
                  'codigo',
                  'precio',
                  'precio_total',
                  'cantidad',
                  'cant_horas',
                  'detalle',
                  'tipo_servicio',
                  'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows':3}),
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
        }


OT_LineaFormSet = generic_inlineformset_factory(OT_Linea,
                                                min_num=1,
                                                extra=0,
                                                formfield_callback=bootstrap_format,
                                                form=OT_LineaForm,
                                                formset=CustomInlineFormset,
                                               )


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
        if self.instance and self.instance.estado not in \
                           ('borrador', 'aceptado'):
            return self.instance.fecha_realizado
        else:
            return self.cleaned_data['fecha_realizado']

    def clean_fecha_instrumento(self):
        if self.instance and self.instance.estado not in \
                           ('borrador', 'aceptado'):
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

    def clean_nro_recepcion(self):
        if self.instance and self.instance.estado not in \
                           ('borrador', 'aceptado'):
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

