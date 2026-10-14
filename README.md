# MVP · Sistema de Monitoreo de Calidad del Aire

MVP mínimo para la materia **Administración de Proyectos de Software**.

## Qué demuestra

- Persistencia de sensores y lecturas en SQLite.
- Importación de lecturas desde CSV.
- Trazabilidad mínima `sensor + fecha/hora`.
- Consulta por sensor y periodo.
- Selección de parámetro PM1, PM2.5, PM4, PM10 o CO₂.
- Tabla y gráfica temporal sin librerías externas de frontend.
- Pruebas automatizadas para importación, filtros y endpoint de salud.

No implementa todavía alertas, umbrales, integración directa con sensores ni servidor definitivo. Esas funciones quedan para incrementos posteriores y/o validación con la clienta.

## Ejecutar en macOS

```bash
cd MVP_Monitoreo_Aire_Oscar_Roman
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_datos data/datos_ejemplo.csv
python manage.py test
python manage.py runserver
```

Abrir: `http://127.0.0.1:8000/`

## Demo sugerida

1. Abrir el dashboard con los datos de ejemplo.
2. Filtrar por `G3`.
3. Elegir `PM 2.5`.
4. Cambiar fechas y comprobar que la tabla/gráfica cambian.
5. Importar `data/datos_ejemplo.csv` desde la interfaz: los registros existentes se actualizan en lugar de duplicarse.
6. Mostrar `/health/` para evidencia rápida del estado de la aplicación.

## CSV esperado

Columnas obligatorias:

```text
sensor,fecha_hora,pm1,pm25,pm4,pm10,co2
```

Opcionales: `nombre_sensor`, `ubicacion`.

`fecha_hora` usa formato ISO, por ejemplo `2025-11-23T12:00:00`.

## Datos de ejemplo

El CSV incluido usa promedios diarios de G3/G4 transcritos de los reportes de noviembre de 2025 proporcionados como material del proyecto. Se usan únicamente para la demo del MVP; el significado final de G3/G4, ubicación y formato/frecuencia real del sensor siguen pendientes de validación con la clienta.
