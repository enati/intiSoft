from django.contrib import admin
from .models import Turno, OfertaTec_Linea, OfertaTec_Descripcion
from reversion.admin import VersionAdmin



class OfertatecTecLineaInline(admin.TabularInline):
    model = OfertaTec_Linea
    fields = ('ofertatec', 'codigo', 'detalle', 'tipo_servicio', 'cantidad', 'cant_horas', 'precio', 'precio_total', 'observaciones')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(OfertaTec_Descripcion)
class OfertaTec_DescripcionAdmin(VersionAdmin):
    pass

@admin.register(OfertaTec_Linea)
class OfertaTecLineaAdmin(VersionAdmin):
    search_fields = ('id', 'codigo',)
    list_display = ('id', 'codigo',)
    fields = ('ofertatec', 'codigo', 'detalle', 'tipo_servicio', 'cantidad', 'cant_horas', 'precio', 'precio_total',
              'observaciones')

@admin.register(Turno)
class TurnoAdmin(VersionAdmin):
    search_fields = ['estado', 'presupuesto__usuario__nombre', 'presupuesto__codigo', 'presupuesto__nro_presea']
    list_display = ('estado', 'usuario', 'fecha_inicio', 'fecha_fin', 'aceptacion_presupuesto', 'nro_anexo', 'nro_presea')
    inlines = [
        OfertatecTecLineaInline,
    ]

    def usuario(self, obj):
        if obj.presupuesto:
            return obj.presupuesto.usuario
        elif obj.si:
            return obj.si.solicitante
        else:
            return ''

    def nro_anexo(self, obj):
        if obj.presupuesto:
            return obj.presupuesto.codigo
        return ''

    def nro_presea(self, obj):
        if obj.presupuesto:
            return obj.presupuesto.nro_presea
        return ''

    def aceptacion_presupuesto(self, obj):
        if obj.presupuesto and obj.presupuesto.fecha_aceptado:
            return obj.presupuesto.fecha_aceptado
        else:
            return ''