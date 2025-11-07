from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from eventos import views as eventos_views

urlpatterns = [
    # Página principal: muestra eventos recientes
    path('', eventos_views.eventos_recientes, name='home'),

    path('admin/', admin.site.urls),
    path('eventos/', include('eventos.urls')),

    # Autenticación
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path('logout/', eventos_views.salir, name='logout'),

    # Registro de usuarios
    path('register/', eventos_views.registrar_usuario, name='register'),
]

handler403 = "eventos.views.acceso_denegado"
