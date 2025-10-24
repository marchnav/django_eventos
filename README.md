# Registro de Eventos — Django

Aplicación de ejemplo para registrar **Eventos** y **Participantes** usando **Django 5** con **FormClass**, validaciones y **inline formset**.

## Requisitos
- Python 3.10+ (recomendado)
- pip

## Instalación
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Ejecutar
python manage.py migrate
python manage.py runserver
Abrir: http://127.0.0.1:8000/

## Crear Superusuario
python manage.py createsuperuser
Admin: http://127.0.0.1:8000/admin/

## Estructura principal
config/                 # settings, urls
eventos/                # app con modelos, forms, vistas
templates/
  base.html
  eventos/
    _evento_form.html
    _participante_form.html
    registrar_evento.html

## Validaciones

Evento.nombre: máx. 100 caracteres.

Evento.fecha: debe ser futura.

Participante: nombre y email obligatorios.

Se muestran errores bajo cada campo.

## Entrega incliye

Código fuente

requirements.txt

Este README.md