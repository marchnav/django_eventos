from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.models import Group
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .models import Evento, Participante
from .forms import EventoForm, ParticipanteForm

@login_required
@permission_required('eventos.add_evento', raise_exception=True)
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
            # Asignar propietario al usuario autenticado
            evento.propietario = request.user

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


def acceso_denegado(request, exception=None):
    messages.error(request, "No tienes permisos para realizar esta acción.")
    if request.user.is_authenticated:
        return redirect('eventos:listar')
    return redirect('login')


def registrar_usuario(request):
    """
    Registro básico con UserCreationForm.
    - Agrega al usuario nuevo al grupo 'Asistentes'
    - Inicia sesión y redirige a la lista de eventos
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Agregar a grupo por defecto: Asistentes
            grupo_asistentes, _ = Group.objects.get_or_create(name='Asistentes')
            user.groups.add(grupo_asistentes)

            messages.success(request, "✅ Cuenta creada. ¡Bienvenido!")
            auth_login(request, user)

            # Redirigir a la lista (evita chocar con permisos de 'registrar')
            return redirect("eventos:listar")
        else:
            messages.error(request, "Corrige los errores e intenta nuevamente.")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def listar_eventos(request):
    """
    Muestra:
    - Todos los eventos públicos (es_privado=False)
    - + Los eventos privados cuyo propietario es el usuario actual
    """
    qs = Evento.objects.filter(
        Q(es_privado=False) | Q(propietario=request.user)
    ).order_by("fecha", "nombre")

    return render(request, "eventos/listar_eventos.html", {"eventos": qs})


# ---- Edición con Mixins (login + permisos + dueño) ----

class SoloPropietarioOMods(UserPassesTestMixin):
    """
    Permite acceso a:
    - superuser
    - grupo 'AdministradoresEventos'
    - propietario del objeto
    """
    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        if not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        if u.groups.filter(name='AdministradoresEventos').exists():
            return True
        return getattr(obj, "propietario_id", None) == u.id


class EditarEventoView(LoginRequiredMixin, PermissionRequiredMixin, SoloPropietarioOMods, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = "eventos/editar_evento.html"
    permission_required = "eventos.change_evento"
    raise_exception = True  # dispara 403 si no tiene permiso
    success_url = reverse_lazy("eventos:listar")

    def form_valid(self, form):
        messages.success(self.request, "✅ Evento actualizado con éxito.")
        return super().form_valid(form)


# ---- Eliminación restringida a AdministradoresEventos / superuser ----

class SoloAdmins(UserPassesTestMixin):
    """Permite acceso solo a superuser o grupo 'AdministradoresEventos'."""
    def test_func(self):
        u = self.request.user
        if not u.is_authenticated:
            return False
        return u.is_superuser or u.groups.filter(name='AdministradoresEventos').exists()

class EliminarEventoView(LoginRequiredMixin, PermissionRequiredMixin, SoloAdmins, DeleteView):
    model = Evento
    template_name = "eventos/confirmar_eliminacion.html"
    permission_required = "eventos.delete_evento"
    raise_exception = True  # 403 si no tiene permiso
    success_url = reverse_lazy("eventos:listar")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "🗑️ Evento eliminado con éxito.")
        return super().delete(request, *args, **kwargs)


# ---- Logout compatible con GET/POST ----

def salir(request):
    """Cierra sesión y redirige al login (muestra mensaje)."""
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("login")
