from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("despacho/", views.despacho_dia, name="despacho_dia"),
]

urlpatterns = [
    path("despacho/", views.despacho_dia, name="despacho_dia"),
    path(
        "despacho/servicio/<int:pk>/editar/",
        views.editar_servicio,
        name="editar_servicio",
    ),
    path(
        "despacho/servicio/<int:pk>/reposicion/",
        views.programar_reposicion,
        name="programar_reposicion",
    ),

    path(
        "reportes/choferes/semanal/",
        views.reporte_semanal_choferes,
        name="reporte_semanal_choferes",
    ),

    path(
        "reportes/choferes/semanal/excel/",
        views.exportar_reporte_semanal_excel,
        name="exportar_reporte_semanal_excel",
    ),

    path(
        "reportes/despacho/",
        views.reporte_despacho_dia,
        name="reporte_despacho_dia",
    ),

    path(
        "reportes/servicios/",
        views.reporte_servicios,
        name="reporte_servicios",
    ),
]

    