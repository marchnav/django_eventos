from django.contrib import admin
from .models import Evento, Participante

class ParticipanteInline(admin.TabularInline):
    model = Participante
    extra = 0

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "fecha", "ubicacion")
    search_fields = ("nombre", "ubicacion")
    list_filter = ("fecha",)
    inlines = [ParticipanteInline]

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "evento")
    search_fields = ("nombre", "email", "evento__nombre")
