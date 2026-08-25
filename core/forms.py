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

        if estado in ["NO_SALIO", "PENDIENTE_REPOSICION"] and not motivo:
            self.add_error(
                "motivo_no_salida",
                "Debe indicar el motivo por el cual el servicio no salió.",
            )

        if estado not in ["NO_SALIO", "PENDIENTE_REPOSICION"] and motivo:
            self.add_error(
                "motivo_no_salida",
                "Solo debe indicar un motivo cuando el servicio no salió.",
            )

        return cleaned_data

    def save(self, commit=True):
        servicio = super().save(commit=False)

        # Si registra hora de salida, el servicio queda en operación.
        if (
            servicio.hora_salida
            and not servicio.hora_regreso
            and servicio.estado == "PROGRAMADO"
        ):
            servicio.estado = "EN_SERVICIO"

        # Si registra hora de regreso, el servicio queda realizado.
        if (
            servicio.hora_salida
            and servicio.hora_regreso
            and servicio.estado in ["PROGRAMADO", "EN_SERVICIO"]
        ):
            servicio.estado = "REALIZADO"

        # Si el servicio no salió y el motivo genera reposición,
        # queda pendiente de reposición.
        if (
            servicio.estado == "NO_SALIO"
            and servicio.motivo_no_salida
            and servicio.motivo_no_salida.genera_reposicion
        ):
            servicio.estado = "PENDIENTE_REPOSICION"

    def clean(self):
        cleaned_data = super().clean()

        hora_salida = cleaned_data.get("hora_salida")
        hora_regreso = cleaned_data.get("hora_regreso")

        if hora_regreso and not hora_salida:
            self.add_error(
                "hora_regreso",
                "No puede registrar hora de regreso sin haber registrado la hora de salida."
               )

        return cleaned_data

        if commit:
            servicio.save()

            # Si este servicio es una reposición y ya fue realizado,
            # marcar el servicio original como REPUESTO.
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