from datetime import datetime

from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta


from .models import Servicio
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ServicioDespachoForm
from .forms import ReposicionForm, ServicioDespachoForm
from .models import Servicio, TarifaChofer
from django.db import models


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

    total_servicios = servicios.count()
    programados = servicios.filter(estado="PROGRAMADO").count()
    en_servicio = servicios.filter(estado="EN_SERVICIO").count()
    realizados = servicios.filter(estado="REALIZADO").count()
    requieren_atencion = servicios.filter(
        estado__in=["NO_SALIO", "PENDIENTE_REPOSICION"]
    ).count()

    contexto = {
        "fecha": fecha,
        "servicios": servicios,
        "total_servicios": total_servicios,
        "programados": programados,
        "en_servicio": en_servicio,
        "realizados": realizados,
        "requieren_atencion": requieren_atencion,
    }
    return render(request, "core/despacho_dia.html", contexto)

def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == "POST":
        form = ServicioDespachoForm(request.POST, instance=servicio)

        if form.is_valid():
            form.save()

            return redirect(
                f"/despacho/?fecha={servicio.fecha:%Y-%m-%d}"
            )
    else:
        form = ServicioDespachoForm(instance=servicio)

    contexto = {
        "servicio": servicio,
        "form": form,
    }

    return render(request, "core/editar_servicio.html", contexto)

def programar_reposicion(request, pk):
    servicio_original = get_object_or_404(
        Servicio,
        pk=pk,
        estado="PENDIENTE_REPOSICION",
    )

    if servicio_original.reposiciones.exists():
        reposicion = servicio_original.reposiciones.first()

        return redirect(
            f"/despacho/?fecha={reposicion.fecha:%Y-%m-%d}"
        )

    if request.method == "POST":
        form = ReposicionForm(request.POST)

        if form.is_valid():
            reposicion = form.save(commit=False)

            reposicion.orden = servicio_original.orden
            reposicion.publicidad = servicio_original.publicidad
            reposicion.camion_contratado = servicio_original.camion_contratado
            reposicion.recorrido = servicio_original.recorrido
            reposicion.perifoneo = servicio_original.perifoneo

            reposicion.es_reposicion = True
            reposicion.servicio_original = servicio_original
            reposicion.estado = "PROGRAMADO"

            reposicion.save()

            return redirect(
                f"/despacho/?fecha={reposicion.fecha:%Y-%m-%d}"
            )
    else:
        form = ReposicionForm(
            initial={
                "turno": servicio_original.turno,
                "camion_operativo": servicio_original.camion_operativo
                or servicio_original.camion_contratado,
                "chofer": servicio_original.chofer,
            }
        )

    contexto = {
        "servicio_original": servicio_original,
        "form": form,
    }

    return render(
        request,
        "core/programar_reposicion.html",
        contexto,
    )

def reporte_semanal_choferes(request):
    fecha_consulta = request.GET.get("fecha")

    if fecha_consulta:
        try:
            fecha_base = datetime.strptime(
                fecha_consulta,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            fecha_base = timezone.localdate()
    else:
        fecha_base = timezone.localdate()

    dias_desde_jueves = (fecha_base.weekday() - 3) % 7
    fecha_inicio = fecha_base - timedelta(days=dias_desde_jueves)
    fecha_fin = fecha_inicio + timedelta(days=6)

    tarifa_normal = (
        TarifaChofer.objects
        .filter(
            tipo="NORMAL",
            activa=True,
            fecha_inicio__lte=fecha_fin,
        )
        .filter(
            models.Q(fecha_fin__isnull=True) |
            models.Q(fecha_fin__gte=fecha_inicio)
        )
        .order_by("-fecha_inicio")
        .first()
    )

    tarifa_tercero = (
        TarifaChofer.objects
        .filter(
            tipo="TERCERO",
            activa=True,
            fecha_inicio__lte=fecha_fin,
        )
        .filter(
            models.Q(fecha_fin__isnull=True) |
            models.Q(fecha_fin__gte=fecha_inicio)
        )
        .order_by("-fecha_inicio")
        .first()
    )

    servicios = (
        Servicio.objects.filter(
            fecha__range=(fecha_inicio, fecha_fin),
            estado="REALIZADO",
            chofer__isnull=False,
        )
        .select_related("chofer", "turno")
        .order_by("chofer__nombre", "fecha", "turno")
    )

    resumen = {}

    for servicio in servicios:
        chofer = servicio.chofer

        if chofer.pk not in resumen:
            resumen[chofer.pk] = {
                "chofer": chofer,
                "primero": 0,
                "segundo": 0,
                "tercero": 0,
                "total": 0,
            }

        nombre_turno = str(servicio.turno).lower()

        if "primer" in nombre_turno:
            resumen[chofer.pk]["primero"] += 1
        elif "segundo" in nombre_turno:
            resumen[chofer.pk]["segundo"] += 1
        elif "tercer" in nombre_turno:
            resumen[chofer.pk]["tercero"] += 1

        resumen[chofer.pk]["total"] += 1


    importe_normal = tarifa_normal.importe if tarifa_normal else 0
    importe_tercero = tarifa_tercero.importe if tarifa_tercero else 0

    for fila in resumen.values():
        fila["importe_normal"] = importe_normal
        fila["importe_tercero"] = importe_tercero

        fila["total_pagar"] = (
            (fila["primero"] + fila["segundo"]) * importe_normal
            + fila["tercero"] * importe_tercero
        )


    total_general = sum(
        fila["total_pagar"]
        for fila in resumen.values()
)
    contexto = {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "resumen": resumen.values(),
        "servicios": servicios,
        "tarifa_normal": tarifa_normal,
        "tarifa_tercero": tarifa_tercero,
        "fecha_base": fecha_base,
        "total_general": total_general,
    }

    return render(
        request,
        "core/reporte_semanal_choferes.html",
        contexto,
    )


