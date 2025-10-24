from django.db import models

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    ubicacion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.nombre} — {self.fecha}"

class Participante(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="participantes")
    nombre = models.CharField(max_length=120)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} <{self.email}>"
