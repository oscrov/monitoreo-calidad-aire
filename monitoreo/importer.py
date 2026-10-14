import csv
import io
from datetime import datetime
from django.utils import timezone
from .models import Lectura, Sensor

REQUIRED_COLUMNS = {"sensor", "fecha_hora", "pm1", "pm25", "pm4", "pm10", "co2"}


def _parse_datetime(value: str):
    value = (value or "").strip()
    if not value:
        raise ValueError("fecha_hora vacía")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def import_csv_text(text: str):
    reader = csv.DictReader(io.StringIO(text))
    columns = set(reader.fieldnames or [])
    missing = sorted(REQUIRED_COLUMNS - columns)
    if missing:
        raise ValueError("Faltan columnas: " + ", ".join(missing))

    imported = 0
    updated = 0
    errors = []

    for line_no, row in enumerate(reader, start=2):
        try:
            codigo = (row.get("sensor") or "").strip()
            if not codigo:
                raise ValueError("sensor vacío")
            dt = _parse_datetime(row.get("fecha_hora"))
            values = {
                "pm1": float(row["pm1"]),
                "pm25": float(row["pm25"]),
                "pm4": float(row["pm4"]),
                "pm10": float(row["pm10"]),
                "co2": float(row["co2"]),
            }
            sensor, _ = Sensor.objects.get_or_create(
                codigo=codigo,
                defaults={
                    "nombre": (row.get("nombre_sensor") or codigo).strip(),
                    "ubicacion": (row.get("ubicacion") or "").strip(),
                },
            )
            obj, created = Lectura.objects.update_or_create(
                sensor=sensor,
                fecha_hora=dt,
                defaults=values,
            )
            imported += int(created)
            updated += int(not created)
        except Exception as exc:
            errors.append(f"Línea {line_no}: {exc}")

    return {"imported": imported, "updated": updated, "errors": errors}
