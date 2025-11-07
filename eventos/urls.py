from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    # Lista de todos los eventos registrados
    path('', views.listar_eventos, name='listar'),

    # Registrar nuevo evento + participantes
    path('registrar/', views.registrar_evento, name='registrar'),

    # Detalle de un evento específico
    path('<int:pk>/', views.detalle_evento, name='detalle'),

    # Editar / eliminar (con permisos y propietario)
    path('<int:pk>/editar/', views.EditarEventoView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.EliminarEventoView.as_view(), name='eliminar'),
]
