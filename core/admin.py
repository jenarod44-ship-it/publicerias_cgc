from django.contrib import admin

from .models import Camion


@admin.register(Camion)
class CamionAdmin(admin.ModelAdmin):
    list_display = ("clave", "tamano", "activo")
    list_filter = ("tamano", "activo")
    search_fields = ("clave",)