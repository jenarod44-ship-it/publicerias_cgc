from django.contrib import admin

from .models import (
    Camion,
    Telefono,
    Chofer,
    Ejecutivo,
    Publicidad,
    Turno,
    TarifaChofer,
    MotivoNoSalida,
    OrdenTrabajo,
    Servicio,
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

@admin.register(MotivoNoSalida)
class MotivoNoSalidaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "genera_reposicion", "activo")
    list_filter = ("genera_reposicion", "activo")
    search_fields = ("nombre",)

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        "folio",
        "fecha_orden",
        "publicidad",
        "ejecutivo",
        "camion",
        "turno",
        "fecha_inicio",
        "fecha_fin",
        "estado",
    )

    list_filter = (
        "estado",
        "turno",
        "perifoneo",
        "firma_bitacora",
        "fecha_orden",
    )

    search_fields = (
        "folio",
        "publicidad__nombre",
        "ejecutivo__nombre",
        "camion__clave",
        "recorrido",
    )

    fieldsets = (
        (
            "Orden de trabajo",
            {
                "fields": (
                    "folio",
                    "fecha_orden",
                    "publicidad",
                    "ejecutivo",
                    "camion",
                    "turno",
                )
            },
        ),
        (
            "Vigencia y días de trabajo",
            {
                "fields": (
                    "fecha_inicio",
                    "fecha_fin",
                    (
                        "lunes",
                        "martes",
                        "miercoles",
                        "jueves",
                        "viernes",
                        "sabado",
                        "domingo",
                    ),
                )
            },
        ),
        (
            "Condiciones del servicio",
            {
                "fields": (
                    "recorrido",
                    "perifoneo",
                    "firma_bitacora",
                )
            },
        ),
        (
            "Evidencias",
            {
                "fields": (
                    "evidencia_ejecutivo",
                    "evidencia_grupo_choferes",
                    "evidencia_cliente",
                    "referencia_cliente",
                )
            },
        ),
        (
            "Operación",
            {
                "fields": (
                    "chofer_base",
                    "observaciones",
                    "estado",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.generar_servicios()

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "orden",
        "publicidad",
        "turno",
        "camion_contratado",
        "camion_operativo",
        "chofer",
        "telefono",
        "estado",
        "es_reposicion",
    )

    list_filter = (
        "fecha",
        "turno",
        "estado",
        "es_reposicion",
        "perifoneo",
    )

    search_fields = (
        "orden__folio",
        "publicidad__nombre",
        "camion_contratado__clave",
        "camion_operativo__clave",
        "chofer__nombre",
        "telefono__clave",
        "recorrido",
    )

    fieldsets = (
        (
            "Servicio programado",
            {
                "fields": (
                    "orden",
                    "fecha",
                    "publicidad",
                    "turno",
                    "camion_contratado",
                    "recorrido",
                    "perifoneo",
                )
            },
        ),
        (
            "Despacho",
            {
                "fields": (
                    "camion_operativo",
                    "chofer",
                    "telefono",
                    "hora_salida",
                    "hora_regreso",
                )
            },
        ),
        (
            "Resultado",
            {
                "fields": (
                    "estado",
                    "motivo_no_salida",
                    "observaciones",
                )
            },
        ),
        (
            "Reposición",
            {
                "fields": (
                    "es_reposicion",
                    "servicio_original",
                )
            },
        ),
    )