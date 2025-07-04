from django.contrib import admin
from .models import Resolucion, DetalleResolucion, ResponsableObra, Zonificacion, LicenciaUso


@admin.register(ResponsableObra)
class ResponsableObraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cip_cap']
    search_fields = ['nombre', 'cip_cap']


@admin.register(Zonificacion)
class ZonificacionAdmin(admin.ModelAdmin):
    list_display = ['zonificacion', 'departamento', 'provincia', 'distrito']
    list_filter = ['departamento', 'provincia']
    search_fields = ['zonificacion', 'distrito']


@admin.register(LicenciaUso)
class LicenciaUsoAdmin(admin.ModelAdmin):
    list_display = ['nombre_licencia', 'uso_licencia']
    search_fields = ['nombre_licencia', 'uso_licencia']


@admin.register(Resolucion)
class ResolucionAdmin(admin.ModelAdmin):
    list_display = ['num_resolucion', 'fecha_emision', 'administrado', 'nombre_licencia', 'usuario']
    list_filter = ['fecha_emision', 'nombre_licencia', 'propietario']
    search_fields = ['num_resolucion', 'num_expediente', 'administrado']
    date_hierarchy = 'fecha_emision'


@admin.register(DetalleResolucion)
class DetalleResolucionAdmin(admin.ModelAdmin):
    list_display = ['resolucion', 'responsable_obra', 'num_pisos', 'altura', 'areatechada_total']
    list_filter = ['num_pisos', 'semisotano']
    search_fields = ['resolucion__num_resolucion', 'responsable_obra__nombre']
