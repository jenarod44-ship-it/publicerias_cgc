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