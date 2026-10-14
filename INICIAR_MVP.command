#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "=============================================="
echo " MVP · Monitoreo de Calidad del Aire"
echo " Preparando entorno..."
echo "=============================================="

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: No se encontró python3."
  echo "Instala Python 3 y vuelve a ejecutar este archivo."
  read -p "Presiona Enter para cerrar..."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "[1/5] Creando entorno virtual..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "[2/5] Instalando/verificando Django..."
python -m pip install -q -r requirements.txt

echo "[3/5] Preparando base de datos..."
python manage.py migrate --noinput

echo "[4/5] Cargando datos de ejemplo..."
python manage.py cargar_datos data/datos_ejemplo.csv

echo "[5/5] Ejecutando pruebas..."
python manage.py test

echo ""
echo "TODO OK. Abriendo http://127.0.0.1:8000/"
(sleep 2; open "http://127.0.0.1:8000/") &
python manage.py runserver 127.0.0.1:8000
