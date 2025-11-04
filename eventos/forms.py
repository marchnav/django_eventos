from django import forms
from django.utils import timezone
from .models import Evento, Participante

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["nombre", "fecha", "ubicacion", "es_privado"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "")
        if len(nombre) > 100:
            raise forms.ValidationError("El nombre del evento no debe superar los 100 caracteres.")
        return nombre

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if fecha is None:
            return fecha
        hoy = timezone.localdate()
        if fecha <= hoy:
            raise forms.ValidationError("La fecha del evento debe ser futura.")
        return fecha


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ["nombre", "email"]
