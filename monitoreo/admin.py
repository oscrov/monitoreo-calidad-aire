from django.contrib import admin
from .models import Lectura, Sensor


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "ubicacion", "activo")
    search_fields = ("codigo", "nombre", "ubicacion")


@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    list_display = ("sensor", "fecha_hora", "pm1", "pm25", "pm4", "pm10", "co2")
    list_filter = ("sensor",)
    date_hierarchy = "fecha_hora"
