from django.contrib import admin

from .models import Camion, Telefono


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