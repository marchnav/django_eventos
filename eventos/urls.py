from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("registrar/", views.registrar_evento, name="registrar"),
]
