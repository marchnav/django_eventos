from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("registrar/", views.registrar_evento, name="registrar"),
    path("listar/", views.listar_eventos, name="listar"),
    path("<int:pk>/editar/", views.EditarEventoView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.EliminarEventoView.as_view(), name="eliminar"),
]
