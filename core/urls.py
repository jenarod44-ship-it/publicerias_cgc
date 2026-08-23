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
]