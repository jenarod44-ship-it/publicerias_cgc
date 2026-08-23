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

        if (
            servicio.estado == "NO_SALIO"
            and servicio.motivo_no_salida
            and servicio.motivo_no_salida.genera_reposicion
        ):
            servicio.estado = "PENDIENTE_REPOSICION"

        if commit:
            servicio.save()

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