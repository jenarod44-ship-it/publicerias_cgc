from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError


class Camion(models.Model):
    TAMANOS = [
        ("GRANDE", "Grande"),
        ("CHICO", "Chico"),
    ]

    clave = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Camión"
    )
    tamano = models.CharField(
        max_length=10,
        choices=TAMANOS,
        verbose_name="Tamaño"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Camión"
        verbose_name_plural = "Camiones"
        ordering = ["clave"]

    def __str__(self):
        return self.clave


class Telefono(models.Model):
    clave = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Teléfono"
    )
    numero = models.CharField(
        max_length=20,
        verbose_name="Número telefónico"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Teléfono"
        verbose_name_plural = "Teléfonos"
        ordering = ["clave"]

    def __str__(self):
        return f"{self.clave} - {self.numero}"

class Chofer(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Chofer"
        verbose_name_plural = "Choferes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Ejecutivo(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Ejecutivo de ventas"
        verbose_name_plural = "Ejecutivos de ventas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Publicidad(models.Model):
    nombre = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Publicidad"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )

    class Meta:
        verbose_name = "Publicidad"
        verbose_name_plural = "Publicidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Turno(models.Model):
    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Turno"
    )
    hora_inicio = models.TimeField(
        verbose_name="Hora de inicio"
    )
    hora_fin = models.TimeField(
        verbose_name="Hora de fin"
    )
    cruza_medianoche = models.BooleanField(
        default=False,
        verbose_name="Cruza medianoche"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        ordering = ["hora_inicio"]

    def __str__(self):
        return self.nombre

class TarifaChofer(models.Model):
    TIPOS = [
        ("NORMAL", "Primer y Segundo turno"),
        ("TERCERO", "Tercer turno"),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        verbose_name="Tipo de tarifa"
    )
    importe = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Importe"
    )
    fecha_inicio = models.DateField(
        verbose_name="Vigente desde"
    )
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Vigente hasta"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )

    class Meta:
        verbose_name = "Tarifa de chofer"
        verbose_name_plural = "Tarifas de chofer"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.get_tipo_display()} - ${self.importe}"

class MotivoNoSalida(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Motivo"
    )
    genera_reposicion = models.BooleanField(
        default=True,
        verbose_name="Genera reposición"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Motivo de no salida"
        verbose_name_plural = "Motivos de no salida"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class OrdenTrabajo(models.Model):
    ESTADOS = [
        ("ACTIVA", "Activa"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    ]

    folio = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Folio"
    )

    fecha_orden = models.DateField(
        verbose_name="Fecha de la orden"
    )

    publicidad = models.ForeignKey(
        Publicidad,
        on_delete=models.PROTECT,
        related_name="ordenes",
        verbose_name="Publicidad"
    )

    ejecutivo = models.ForeignKey(
        Ejecutivo,
        on_delete=models.PROTECT,
        related_name="ordenes",
        verbose_name="Ejecutivo de ventas"
    )

    camion = models.ForeignKey(
        Camion,
        on_delete=models.PROTECT,
        related_name="ordenes",
        verbose_name="Camión contratado"
    )

    turno = models.ForeignKey(
        Turno,
        on_delete=models.PROTECT,
        related_name="ordenes",
        verbose_name="Turno"
    )

    fecha_inicio = models.DateField(
        verbose_name="Fecha de inicio"
    )

    fecha_fin = models.DateField(
        verbose_name="Fecha de fin"
    )

    lunes = models.BooleanField(default=False, verbose_name="Lunes")
    martes = models.BooleanField(default=False, verbose_name="Martes")
    miercoles = models.BooleanField(default=False, verbose_name="Miércoles")
    jueves = models.BooleanField(default=False, verbose_name="Jueves")
    viernes = models.BooleanField(default=False, verbose_name="Viernes")
    sabado = models.BooleanField(default=False, verbose_name="Sábado")
    domingo = models.BooleanField(default=False, verbose_name="Domingo")

    recorrido = models.TextField(
        verbose_name="Recorrido"
    )

    perifoneo = models.BooleanField(
        default=False,
        verbose_name="Perifoneo"
    )

    firma_bitacora = models.BooleanField(
        default=False,
        verbose_name="Firma de bitácora"
    )

    evidencia_ejecutivo = models.BooleanField(
        default=True,
        verbose_name="Enviar evidencia a ejecutivo"
    )

    evidencia_grupo_choferes = models.BooleanField(
        default=True,
        verbose_name="Enviar evidencia al grupo de choferes"
    )

    evidencia_cliente = models.BooleanField(
        default=False,
        verbose_name="Enviar evidencia al cliente"
    )

    referencia_cliente = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Referencia del cliente"
    )

    chofer_base = models.ForeignKey(
        Chofer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ordenes_base",
        verbose_name="Chofer asignado"
    )

    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="ACTIVA",
        verbose_name="Estado"
    )

    class Meta:
        verbose_name = "Orden de trabajo"
        verbose_name_plural = "Órdenes de trabajo"
        ordering = ["-fecha_orden", "folio"]

    def clean(self):
        super().clean()

        errores = {}

        if self.estado == "CANCELADA":
            return

        if not (
            self.camion_id
            and self.turno_id
            and self.fecha_inicio
            and self.fecha_fin
        ):
            return

        if self.fecha_fin < self.fecha_inicio:
            errores["fecha_fin"] = (
                "La fecha de fin no puede ser menor que la fecha de inicio."
            )

        dias_actuales = {
            0: self.lunes,
            1: self.martes,
            2: self.miercoles,
            3: self.jueves,
            4: self.viernes,
            5: self.sabado,
            6: self.domingo,
        }

        fechas_actuales = set()

        if self.fecha_inicio and self.fecha_fin:
            fecha = self.fecha_inicio

            while fecha <= self.fecha_fin:
                if dias_actuales[fecha.weekday()]:
                    fechas_actuales.add(fecha)

                fecha += timedelta(days=1)

        if not fechas_actuales:
            if errores:
                raise ValidationError(errores)
            return

        def obtener_conflictos(otra):
            dias_otra = {
                0: otra.lunes,
                1: otra.martes,
                2: otra.miercoles,
                3: otra.jueves,
                4: otra.viernes,
                5: otra.sabado,
                6: otra.domingo,
            }

            fecha_actual = max(self.fecha_inicio, otra.fecha_inicio)
            fecha_limite = min(self.fecha_fin, otra.fecha_fin)

            conflictos = []

            while fecha_actual <= fecha_limite:
                if (
                    fecha_actual in fechas_actuales
                    and dias_otra[fecha_actual.weekday()]
                ):
                    conflictos.append(fecha_actual)

                fecha_actual += timedelta(days=1)

            return conflictos

        # -------------------------
        # VALIDAR CAMIÓN
        # -------------------------
        otras_ordenes_camion = OrdenTrabajo.objects.filter(
            camion=self.camion,
            turno=self.turno,
            fecha_inicio__lte=self.fecha_fin,
            fecha_fin__gte=self.fecha_inicio,
        ).exclude(
            pk=self.pk
        ).exclude(
            estado="CANCELADA"
        )

        for otra in otras_ordenes_camion:
            conflictos = obtener_conflictos(otra)

            if conflictos:
                fechas = ", ".join(
                    fecha.strftime("%d/%m/%Y")
                    for fecha in conflictos[:5]
                )

                if len(conflictos) > 5:
                    fechas += ", ..."

                errores["camion"] = (
                    f"El camión {self.camion} ya está ocupado en el "
                    f"{self.turno} por la orden {otra.folio}. "
                    f"Fechas en conflicto: {fechas}."
                )

                break

        # -------------------------
        # VALIDAR CHOFER
        # -------------------------
        if self.chofer_base_id:
            otras_ordenes_chofer = OrdenTrabajo.objects.filter(
                chofer_base=self.chofer_base,
                turno=self.turno,
                fecha_inicio__lte=self.fecha_fin,
                fecha_fin__gte=self.fecha_inicio,
            ).exclude(
                pk=self.pk
            ).exclude(
                estado="CANCELADA"
            )

            for otra in otras_ordenes_chofer:
                conflictos = obtener_conflictos(otra)

                if conflictos:
                    fechas = ", ".join(
                        fecha.strftime("%d/%m/%Y")
                        for fecha in conflictos[:5]
                    )

                    if len(conflictos) > 5:
                        fechas += ", ..."

                    errores["chofer_base"] = (
                        f"El chofer {self.chofer_base} ya está asignado "
                        f"al {self.turno} en la orden {otra.folio}. "
                        f"Fechas en conflicto: {fechas}."
                    )

                    break

        if errores:
            raise ValidationError(errores)

    def generar_servicios(self):
        dias_activos = {
            0: self.lunes,
            1: self.martes,
            2: self.miercoles,
            3: self.jueves,
            4: self.viernes,
            5: self.sabado,
            6: self.domingo,
        }

        fechas_validas = set()
        fecha_actual = self.fecha_inicio

        while fecha_actual <= self.fecha_fin:
            if dias_activos[fecha_actual.weekday()]:
                fechas_validas.add(fecha_actual)

            fecha_actual += timedelta(days=1)

        # Eliminar solamente servicios PROGRAMADOS que ya no
        # corresponden a los días definidos en la Orden.
        self.servicios.filter(
            estado="PROGRAMADO",
            es_reposicion=False,
        ).exclude(
            fecha__in=fechas_validas
        ).delete()

        # Crear o actualizar los servicios que sí corresponden.
        for fecha in fechas_validas:
            servicio, creado = Servicio.objects.get_or_create(
                orden=self,
                fecha=fecha,
                es_reposicion=False,
                defaults={
                    "publicidad": self.publicidad,
                    "turno": self.turno,
                    "camion_contratado": self.camion,
                    "camion_operativo": self.camion,
                    "chofer": self.chofer_base,
                    "recorrido": self.recorrido,
                    "perifoneo": self.perifoneo,
                    "estado": "PROGRAMADO",
                },
            )

            # Si ya existía y todavía está PROGRAMADO,
            # sincronizarlo con la Orden.
            if not creado and servicio.estado == "PROGRAMADO":
                servicio.publicidad = self.publicidad
                servicio.turno = self.turno
                servicio.camion_contratado = self.camion
                servicio.camion_operativo = self.camion
                servicio.chofer = self.chofer_base
                servicio.recorrido = self.recorrido
                servicio.perifoneo = self.perifoneo
                servicio.save()

        def __str__(self):
            return f"{self.folio} - {self.publicidad}"

class Servicio(models.Model):
    ESTADOS = [
        ("PROGRAMADO", "Programado"),
        ("EN_SERVICIO", "En servicio"),
        ("REALIZADO", "Realizado"),
        ("NO_SALIO", "No salió"),
        ("PENDIENTE_REPOSICION", "Pendiente de reposición"),
        ("REPUESTO", "Repuesto"),
        ("CANCELADO", "Cancelado"),
    ]

    orden = models.ForeignKey(
        OrdenTrabajo,
        on_delete=models.PROTECT,
        related_name="servicios",
        verbose_name="Orden de trabajo"
    )

    fecha = models.DateField(
        verbose_name="Fecha del servicio"
    )

    # Datos copiados de la Orden para conservar el histórico.
    publicidad = models.ForeignKey(
        Publicidad,
        on_delete=models.PROTECT,
        related_name="servicios",
        verbose_name="Publicidad"
    )

    turno = models.ForeignKey(
        Turno,
        on_delete=models.PROTECT,
        related_name="servicios",
        verbose_name="Turno"
    )

    camion_contratado = models.ForeignKey(
        Camion,
        on_delete=models.PROTECT,
        related_name="servicios_contratados",
        verbose_name="Camión contratado"
    )

    recorrido = models.TextField(
        verbose_name="Recorrido"
    )

    perifoneo = models.BooleanField(
        default=False,
        verbose_name="Perifoneo"
    )

    # Datos reales de operación.
    camion_operativo = models.ForeignKey(
        Camion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="servicios_operados",
        verbose_name="Camión operativo"
    )

    chofer = models.ForeignKey(
        Chofer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="servicios",
        verbose_name="Chofer"
    )

    telefono = models.ForeignKey(
        Telefono,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="servicios",
        verbose_name="Teléfono"
    )

    hora_salida = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Hora de salida"
    )

    hora_regreso = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Hora de regreso"
    )

    estado = models.CharField(
        max_length=25,
        choices=ESTADOS,
        default="PROGRAMADO",
        verbose_name="Estado"
    )

    motivo_no_salida = models.ForeignKey(
        MotivoNoSalida,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="servicios",
        verbose_name="Motivo de no salida"
    )

    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones"
    )

    es_reposicion = models.BooleanField(
        default=False,
        verbose_name="Es reposición"
    )

    servicio_original = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reposiciones",
        verbose_name="Servicio original"
    )

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ["fecha", "turno"]

    def __str__(self):
        return f"{self.fecha} - {self.orden.folio} - {self.turno}"