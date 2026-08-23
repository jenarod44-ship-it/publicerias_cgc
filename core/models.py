from django.db import models


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

    def __str__(self):
        return f"{self.folio} - {self.publicidad}"