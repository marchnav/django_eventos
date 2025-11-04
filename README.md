# Plataforma de Registro de Eventos — Django 5

App de ejemplo para **registrar eventos y participantes** con **Django 5**, usando:
- `FormClass` + **validaciones** y **inline formset** (participantes)
- **Autenticación y autorización** con el modelo **Auth** (roles y permisos)
- **Mixins** de acceso (`LoginRequiredMixin`, `PermissionRequiredMixin`) y reglas de **propiedad**
- Plantillas reutilizables y **mensajes** de feedback

## Requisitos
- Python 3.10+ (probado con 3.13)
- pip
- Git (opcional)

## Instalación rápida


git clone https://github.com/marchnav/django_eventos
cd <REPO>

python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Abrir: http://127.0.0.1:8000/

## Grupos y roles

Crea tres grupos en /admin → Grupos:

AdministradoresEventos
Permisos: add/change/delete/view de evento y participante (pueden todo).

Organizadores
Permisos: al menos add/change/view sobre evento y participante.
Regla de negocio: solo pueden editar sus propios eventos (propietario).

Asistentes
Sin permisos de edición; pueden listar eventos públicos y sus privados.

El registro vía /register agrega automáticamente al usuario al grupo Asistentes.

## Rutas principales
/login (Django Auth)

/logout (vista propia salir, permite GET/POST)

/register (registro con UserCreationForm, agrega a Asistentes)

/eventos/registrar/ (crear evento + inline formset; requiere add_evento)

/eventos/listar/ (lista públicos + privados del propietario)

/eventos/<id>/editar/ (solo propietario / admin / grupo AdministradoresEventos)

/eventos/<id>/eliminar/ (solo AdministradoresEventos / superuser)

## Redirecciones

LOGIN_REDIRECT_URL = eventos:listar

LOGOUT_REDIRECT_URL = login

## Validaciones de negocio

Evento

nombre: CharField(max_length=100)

fecha: futura (validación en EventoForm)

ubicacion: opcional

es_privado: público/privado

propietario: se asigna con request.user al crear

Participante

nombre: obligatorio

email: EmailField obligatorio
Los errores se muestran debajo de cada campo.

## Flujo esperado por rol

| Acción               | Asistentes | Organizadores             | AdministradoresEventos / superuser |
| -------------------- | ---------- | ------------------------- | ---------------------------------- |
| Listar eventos       | ✅          | ✅                         | ✅                                  |
| Registrar evento     | ❌          | ✅ (crea como propietario) | ✅                                  |
| Editar evento propio | N/A        | ✅                         | ✅                                  |
| Editar evento ajeno  | ❌          | ❌                         | ✅                                  |
| Eliminar evento      | ❌          | ❌                         | ✅                                  |

