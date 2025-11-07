--------------------------------------------------
README - DJANGO EVENTOS
Repositorio disponible del proyecto en : https://github.com/marchnav/django_eventos
Desarrollado por: Marcelo Navarrete
--------------------------------------------------

1. Descripción del proyecto

Este proyecto es una aplicación web desarrollada con Django para la gestión de eventos y sus participantes, con énfasis en el uso de autenticación, permisos, grupos y propiedad de objetos.

Permite:
- Registrar eventos con información clave.
- Asociar participantes a cada evento mediante un formset.
- Controlar qué eventos ve cada usuario según su autenticación y rol.
- Visualizar detalle completo de eventos y participantes.
- Administrar eventos respetando reglas de seguridad y permisos.

--------------------------------------------------
2. Tecnologías utilizadas

- Python 3.x
- Django 5.x
- SQLite como base de datos por defecto
- HTML + CSS (templates de Django)

--------------------------------------------------
3. Modelos principales

A) Evento
- nombre: nombre del evento.
- fecha: fecha del evento.
- ubicacion: lugar (opcional).
- es_privado: indica si el evento es privado.
- propietario: usuario que crea y administra el evento.

B) Participante
- evento: relación con Evento.
- nombre: nombre del participante.
- email: correo opcional.

Relación:
- Un Evento tiene múltiples Participantes.
- Cada Participante pertenece a un solo Evento.

--------------------------------------------------
4. Funcionalidades clave

- Página de inicio:
  - Muestra eventos recientes visibles según el usuario.
- Registro de usuarios:
  - Creación de cuentas con `UserCreationForm`.
- Autenticación:
  - Login y logout.
- Registro de eventos:
  - Formulario protegido con permisos.
  - Uso de formset para registrar participantes asociados.
- Listado de eventos:
  - Vista para mostrar eventos accesibles al usuario (públicos + propios).
- Detalle de evento:
  - Vista dedicada a un evento específico.
  - Muestra participantes vinculados.
- Edición y eliminación:
  - Restringida a usuarios con permisos y/o propietarios del evento.
- Manejo de acceso denegado:
  - Vista personalizada para redirigir o informar cuando no hay permisos.

--------------------------------------------------
5. Estructura básica del proyecto (resumen)

- config/
  - settings.py
  - urls.py
  - wsgi.py
- eventos/
  - models.py
  - views.py
  - forms.py
  - urls.py
  - templates/eventos/
    - eventos_recientes.html
    - listar_eventos.html
    - registrar_evento.html
    - detalle_evento.html
    - editar_evento.html
    - confirmar_eliminacion.html
- templates/registration/
  - login.html
  - register.html
- base.html
  - Plantilla base para el resto de las vistas.

--------------------------------------------------
6. Instalación y ejecución

1) Clonar el repositorio
Descargar o clonar el proyecto en el equipo local.

2) Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate   (Windows)

3) Instalar dependencias
pip install -r requirements.txt
(En su defecto, instalar al menos Django.)

4) Aplicar migraciones
python manage.py migrate

5) Crear superusuario (opcional)
python manage.py createsuperuser

6) Ejecutar el servidor
python manage.py runserver

Acceder en el navegador a:
http://localhost:8000/

--------------------------------------------------
7. Uso de la aplicación

- /register/:
  Registrar un nuevo usuario.

- /login/:
  Iniciar sesión.

- /:
  Ver eventos recientes.

- /eventos/:
  Ver listado de eventos registrados accesibles para el usuario actual.

- /eventos/registrar/:
  Registrar un nuevo evento (requiere permisos).

- /eventos/<id>/:
  Ver el detalle de un evento y sus participantes.

- /eventos/<id>/editar/:
  Editar evento (solo propietario o usuario con permisos).

- /eventos/<id>/eliminar/:
  Eliminar evento (solo usuario autorizado).

--------------------------------------------------
8. Permisos y seguridad

- Uso de @login_required y @permission_required para proteger vistas sensibles.
- Uso de mixins (LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin) en vistas basadas en clases.
- Validación de propiedad del evento para edición/eliminación.
- Restricción en la visualización de eventos privados:
  - Solo propietario o superusuario puede ver el detalle.

--------------------------------------------------
9. Notas finales

Este proyecto no solo cumple con los requisitos funcionales del ejercicio, sino que además incorpora:
- Separación clara de responsabilidades entre vistas, modelos y templates.
- Buenas prácticas en manejo de permisos y visibilidad.
- Ajustes específicos realizados en respuesta a la retroalimentación del docente, garantizando que:
  - Los eventos sean visibles en el home.
  - Los eventos registrados sean accesibles.
  - Cada evento tenga vista de detalle.
  - Los participantes de cada evento se muestren claramente donde corresponde.
