from django.contrib import admin

from .models import (
    Camion,
    Telefono,
    Chofer,
    Ejecutivo,
    Publicidad,
    Turno,
    TarifaChofer,
)


@admin.register(Camion)
class CamionAdmin(admin.ModelAdmin):
    list_display = ("clave", "tamano", "activo")
    list_filter = ("tamano", "activo")
    search_fields = ("clave",)


@admin.register(Telefono)
class TelefonoAdmin(admin.ModelAdmin):
    list_display = ("clave", "numero", "activo")
    list_filter = ("activo",)
    search_fields = ("clave", "numero")

@admin.register(Chofer)
class ChoferAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)

@admin.register(Ejecutivo)
class EjecutivoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)

@admin.register(Publicidad)
class PublicidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre",)

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "hora_inicio",
        "hora_fin",
        "cruza_medianoche",
        "activo",
    )
    list_filter = ("activo", "cruza_medianoche")
    search_fields = ("nombre",)

@admin.register(TarifaChofer)
class TarifaChoferAdmin(admin.ModelAdmin):
    list_display = (
        "tipo",
        "importe",
        "fecha_inicio",
        "fecha_fin",
        "activa",
    )
    list_filter = ("tipo", "activa")

