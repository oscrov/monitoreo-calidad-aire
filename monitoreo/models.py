from django.db import models


class Sensor(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=120, blank=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["codigo"]

    def __str__(self):
        return self.codigo


class Lectura(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="lecturas")
    fecha_hora = models.DateTimeField()
    pm1 = models.FloatField()
    pm25 = models.FloatField()
    pm4 = models.FloatField()
    pm10 = models.FloatField()
    co2 = models.FloatField()

    class Meta:
        ordering = ["fecha_hora"]
        constraints = [
            models.UniqueConstraint(fields=["sensor", "fecha_hora"], name="lectura_sensor_fecha_unica")
        ]

    def __str__(self):
        return f"{self.sensor.codigo} · {self.fecha_hora:%Y-%m-%d %H:%M}"
