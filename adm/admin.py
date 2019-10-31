# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Presupuesto, Usuario, OfertaTec, Provincia, Localidad,\
    DireccionUsuario, Contacto, PDT, CentroDeCostos, AreaTematica, Instrumento,\
    OT, OTML, SOT, RUT, SI, Tarea_Linea, OT_Linea, Factura, Recibo, Remito
from lab.models import Turno
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from reversion.admin import VersionAdmin


class TurnoInline(admin.TabularInline):
    model = Turno
    fields = ('estado', 'fecha_inicio', 'fecha_fin', 'area', 'centro_costos', 'area_tematica', 'horizonte')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class InstrumentoInline(admin.TabularInline):
    model = Instrumento
    extra = 0


class ContactoInline(admin.TabularInline):
    model = Contacto
    extra = 0


class OTLineaInline(GenericTabularInline):
    model = OT_Linea
    fields = ('codigo', 'cantidad', 'cant_horas', 'precio', 'precio_total', 'observaciones')
    extra = 0


class TareaLineaInline(GenericTabularInline):
    model = Tarea_Linea
    extra = 0


class ReciboInline(admin.TabularInline):
    model = Recibo
    extra = 0


class RemitoInline(GenericTabularInline):
    model = Remito
    fields = ('numero', 'fecha',)
    extra = 0


def area(obj):
    return ", ".join(set(obj.get_area()))


@admin.register(Presupuesto)
class PresupuestoAdmin(VersionAdmin):
    search_fields = ['codigo', 'nro_presea', 'usuario__nombre', 'centro_costos__nombre', 'estado', 'turno__area']
    list_display = ('codigo', 'nro_presea', 'usuario', area, 'centro_costos', 'fecha_solicitado', 'fecha_realizado', 'estado')
    inlines = [
        InstrumentoInline,
        TurnoInline,
    ]


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'abreviatura']
    list_display = ('nombre', 'abreviatura')


@admin.register(CentroDeCostos)
class CentroDeCostoAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nombre']
    list_display = ('codigo', 'nombre')


@admin.register(Contacto)
class ContactoAdmin(VersionAdmin):
    search_fields = ['nombre', 'usuario__nombre']
    list_display = ('nombre', 'telefono', 'mail', 'usuario')


@admin.register(Usuario)
class UsuarioAdmin(VersionAdmin):
    search_fields = ['nro_usuario', 'nombre', 'cuit']
    list_display = ('nro_usuario', 'nombre', 'cuit', 'mail')
    inlines = [
        ContactoInline,
    ]


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    search_fields = ['numero',]
    list_display = ('numero', 'ot', 'fecha', 'importe', 'fecha_aviso')
    fields = ('numero', 'fecha', 'importe', 'fecha_aviso', 'ot')
    readonly_fields = ('ot',)
    inlines = [
        ReciboInline,
        RemitoInline
    ]

    def ot(self, obj):
        if obj.content_type_id == 15:
            return OT.objects.get(pk=obj.object_id).codigo
        elif obj.content_type_id == 20:
            return OTML.objects.get(pk=obj.object_id).codigo
        return ''

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Instrumento)
class InstrumentoAdmin(VersionAdmin):
    search_fields = ['nro_recepcion', 'presupuesto__codigo']
    list_display = ('nro_recepcion', 'fecha_llegada', 'presupuesto', 'detalle')


@admin.register(OfertaTec)
class OfertaTecAdmin(VersionAdmin):
    search_fields = ['codigo', 'rubro', 'subrubro', 'tipo_servicio', 'area', 'detalle']
    list_display = ('codigo', 'rubro', 'subrubro', 'tipo_servicio', 'area', 'detalle', 'precio')


@admin.register(OTML)
class OTMLAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'estado', 'vpe', 'vpr', 'vpuu', 'usuario__nombre', 'usuarioRep__nombre']
    list_display = ('codigo', 'estado', 'vpe', 'vpr', 'vpuu', 'usuario', 'usuarioRep', 'fecha_realizado', 'importe_bruto')


@admin.register(OT)
class OTAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'estado', 'presupuesto__codigo', 'presupuesto__nro_presea', 'presupuesto__usuario__nombre', 'presupuesto__turno__area']
    list_display = ('codigo', 'estado', 'nro_anexo', 'nro_presea', 'fecha_realizado', 'usuario', 'importe_bruto', 'area')
    inlines = [
        OTLineaInline,
    ]

    def nro_anexo(self, obj):
        if obj.presupuesto:
            return obj.presupuesto.codigo
        return ''

    def nro_presea(self, obj):
        if obj.presupuesto:
            return obj.presupuesto.nro_presea
        return ''

    def area(self, obj):
        return " - ".join(obj.presupuesto.get_area())

    def usuario(self, obj):
        if obj.presupuesto:
            return obj.presupuesto.usuario.nombre
        return ''


@admin.register(PDT)
class PDTAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nombre', 'anio', 'tipo']
    list_display = ('codigo', 'nombre', 'anio', 'tipo', 'contribucion')


@admin.register(AreaTematica)
class AreaTematicaAdmin(admin.ModelAdmin):
    search_fields = ['nombre', ]
    list_display = ('nombre', )


@admin.register(SOT)
class SOTAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'estado', 'presupuesto__codigo', 'solicitante',
                     'deudor__nombre', 'ejecutor__nombre', 'ot', 'usuario_final__nombre']
    list_display = ('codigo', 'estado', 'fecha_realizado', 'presupuesto', 'solicitante', 'deudor', 'ejecutor', 'ot', 'usuario_final')
    inlines = [
        OTLineaInline,
    ]


@admin.register(RUT)
class RUTAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'estado', 'solicitante', 'deudor__nombre', 'ejecutor__nombre']
    list_display = ('codigo', 'estado', 'fecha_realizado', 'solicitante', 'deudor', 'ejecutor')
    inlines = [
        OTLineaInline,
    ]


@admin.register(SI)
class SIAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'estado', 'presupuesto__codigo', 'solicitante', 'ejecutor']
    list_display = ('codigo', 'estado', 'fecha_realizado', 'presupuesto', 'solicitante', 'ejecutor')
    inlines = [
        TareaLineaInline
    ]

