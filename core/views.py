from datetime import datetime

from django.shortcuts import render
from django.utils import timezone

from .models import Servicio


def despacho_dia(request):
    fecha_texto = request.GET.get("fecha")

    if fecha_texto:
        try:
            fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
        except ValueError:
            fecha = timezone.localdate()
    else:
        fecha = timezone.localdate()

    servicios = (
        Servicio.objects
        .filter(fecha=fecha)
        .select_related(
            "orden",
            "publicidad",
            "turno",
            "camion_contratado",
            "camion_operativo",
            "chofer",
            "telefono",
        )
        .order_by("turno__hora_inicio", "camion_contratado__clave")
    )

    contexto = {
        "fecha": fecha,
        "servicios": servicios,
    }

    return render(request, "core/despacho_dia.html", contexto)


