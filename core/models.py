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