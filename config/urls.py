from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from eventos import views as eventos_views  # registro de usuarios

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='eventos:registrar', permanent=False)),
    path('admin/', admin.site.urls),
    path('eventos/', include('eventos.urls')),

    # Auth
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Signup
    path('register/', eventos_views.registrar_usuario, name='register'),
]

handler403 = "eventos.views.acceso_denegado"
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from eventos import views as eventos_views  # registrar_usuario y salir

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='eventos:registrar', permanent=False)),
    path('admin/', admin.site.urls),
    path('eventos/', include('eventos.urls')),

    # Auth
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', eventos_views.salir, name='logout'),  # 👈 logout compatible GET/POST

    # Signup
    path('register/', eventos_views.registrar_usuario, name='register'),
]

handler403 = "eventos.views.acceso_denegado"
