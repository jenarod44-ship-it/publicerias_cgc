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
