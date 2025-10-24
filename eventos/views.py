from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from .models import Evento, Participante
from .forms import EventoForm, ParticipanteForm

def registrar_evento(request):
    ParticipanteFormSet = inlineformset_factory(
        Evento,
        Participante,
        form=ParticipanteForm,
        extra=2,           # cantidad de formularios vacíos inicialmente
        can_delete=False,
        min_num=1,
        validate_min=True,
    )

    if request.method == "POST":
        evento_form = EventoForm(request.POST)
        formset = ParticipanteFormSet(request.POST)

        if evento_form.is_valid():
            # Crear instancia sin guardar para vincular formset
            evento = evento_form.save(commit=False)
            # Validar formset con instancia
            formset = ParticipanteFormSet(request.POST, instance=evento)
            if formset.is_valid():
                evento.save()
                formset.save()
                messages.success(request, "✅ Evento registrado con éxito.")
                return redirect("eventos:registrar")
        else:
            formset = ParticipanteFormSet(request.POST)

    else:
        evento_form = EventoForm()
        formset = ParticipanteFormSet()

    context = {
        "evento_form": evento_form,
        "formset": formset,
    }
    return render(request, "eventos/registrar_evento.html", context)
