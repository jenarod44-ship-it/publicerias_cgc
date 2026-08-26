from django import forms

from .models import Servicio


class ServicioDespachoForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "camion_operativo",
            "chofer",
            "telefono",
            "hora_salida",
            "hora_regreso",
            "estado",
            "motivo_no_salida",
            "observaciones",
        ]
        widgets = {
            "hora_salida": forms.TimeInput(attrs={"type": "time"}),
            "hora_regreso": forms.TimeInput(attrs={"type": "time"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()

        estado = cleaned_data.get("estado")
        motivo = cleaned_data.get("motivo_no_salida")
        hora_salida = cleaned_data.get("hora_salida")
        hora_regreso = cleaned_data.get("hora_regreso")
        telefono = cleaned_data.get("telefono")

        # No salida: motivo obligatorio.
        if estado in ["NO_SALIO", "PENDIENTE_REPOSICION"] and not motivo:
            self.add_error(
                "motivo_no_salida",
                "Debe indicar el motivo por el cual el servicio no salió.",
            )

        # No debe existir motivo en un servicio normal.
        if estado not in ["NO_SALIO", "PENDIENTE_REPOSICION"] and motivo:
            self.add_error(
                "motivo_no_salida",
                "Solo debe indicar un motivo cuando el servicio no salió.",
            )

        # No puede haber regreso sin salida.
        if hora_regreso and not hora_salida:
            self.add_error(
                "hora_regreso",
                "No puede registrar hora de regreso sin haber registrado la hora de salida.",
            )

        # El mismo teléfono no puede usarse en otro servicio
        # de la misma fecha y turno.
        if telefono and self.instance.fecha and self.instance.turno_id:
            telefono_ocupado = (
                Servicio.objects.filter(
                    fecha=self.instance.fecha,
                    turno=self.instance.turno,
                    telefono=telefono,
                )
                .exclude(pk=self.instance.pk)
                .exclude(estado="NO_SALIO")
                .exists()
            )

            if telefono_ocupado:
                self.add_error(
                    "telefono",
                    "Este teléfono ya está asignado a otro servicio en la misma fecha y turno.",
                )

        return cleaned_data

    def save(self, commit=True):
        servicio = super().save(commit=False)

        # Hora de salida = En servicio.
        if (
            servicio.hora_salida
            and not servicio.hora_regreso
            and servicio.estado == "PROGRAMADO"
        ):
            servicio.estado = "EN_SERVICIO"

        # Hora de regreso = Realizado.
        if (
            servicio.hora_salida
            and servicio.hora_regreso
            and servicio.estado in ["PROGRAMADO", "EN_SERVICIO"]
        ):
            servicio.estado = "REALIZADO"

        # No salió + motivo que genera reposición.
        if (
            servicio.estado == "NO_SALIO"
            and servicio.motivo_no_salida
            and servicio.motivo_no_salida.genera_reposicion
        ):
            servicio.estado = "PENDIENTE_REPOSICION"

        if commit:
            servicio.save()

            # Reposición realizada = original Repuesto.
            if (
                servicio.es_reposicion
                and servicio.servicio_original
                and servicio.estado == "REALIZADO"
            ):
                original = servicio.servicio_original
                original.estado = "REPUESTO"
                original.save(update_fields=["estado"])

        return servicio

class ReposicionForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "fecha",
            "turno",
            "camion_operativo",
            "chofer",
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }