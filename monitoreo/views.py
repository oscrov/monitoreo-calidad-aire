import json
from datetime import date
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .importer import import_csv_text
from .models import Lectura, Sensor

PARAMETERS = {
    "pm1": "PM 1.0",
    "pm25": "PM 2.5",
    "pm4": "PM 4.0",
    "pm10": "PM 10",
    "co2": "CO₂",
}


def _filtered_queryset(request):
    qs = Lectura.objects.select_related("sensor").all()
    sensor = request.GET.get("sensor", "").strip()
    desde = request.GET.get("desde", "").strip()
    hasta = request.GET.get("hasta", "").strip()

    if sensor:
        qs = qs.filter(sensor__codigo=sensor)
    if desde:
        qs = qs.filter(fecha_hora__date__gte=desde)
    if hasta:
        qs = qs.filter(fecha_hora__date__lte=hasta)
    return qs


def dashboard(request):
    parametro = request.GET.get("parametro", "pm25")
    if parametro not in PARAMETERS:
        parametro = "pm25"

    qs = _filtered_queryset(request)
    rows = list(qs.order_by("fecha_hora", "sensor__codigo"))
    chart_data = [
        {
            "label": lectura.fecha_hora.strftime("%d/%m %H:%M") + " · " + lectura.sensor.codigo,
            "value": getattr(lectura, parametro),
        }
        for lectura in rows
    ]

    dates = [r.fecha_hora.date() for r in rows]
    context = {
        "sensores": Sensor.objects.all(),
        "lecturas": rows[-100:],
        "total_lecturas": len(rows),
        "total_sensores": len({r.sensor_id for r in rows}),
        "fecha_min": min(dates).isoformat() if dates else "—",
        "fecha_max": max(dates).isoformat() if dates else "—",
        "parametros": PARAMETERS,
        "parametro": parametro,
        "parametro_label": PARAMETERS[parametro],
        "chart_data": chart_data,
        "filters": {
            "sensor": request.GET.get("sensor", ""),
            "desde": request.GET.get("desde", ""),
            "hasta": request.GET.get("hasta", ""),
        },
    }
    return render(request, "monitoreo/dashboard.html", context)


@require_POST
def importar_csv(request):
    archivo = request.FILES.get("archivo")
    if not archivo:
        messages.error(request, "Selecciona un archivo CSV.")
        return redirect("dashboard")

    try:
        text = archivo.read().decode("utf-8-sig")
        result = import_csv_text(text)
        if result["errors"]:
            messages.warning(
                request,
                f"Importación parcial: {result['imported']} nuevas, {result['updated']} actualizadas. "
                + " | ".join(result["errors"][:3]),
            )
        else:
            messages.success(
                request,
                f"Importación correcta: {result['imported']} nuevas, {result['updated']} actualizadas.",
            )
    except Exception as exc:
        messages.error(request, f"No se pudo importar: {exc}")
    return redirect("dashboard")


def health(request):
    return JsonResponse({
        "status": "ok",
        "sensores": Sensor.objects.count(),
        "lecturas": Lectura.objects.count(),
    })
