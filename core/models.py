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