#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
  echo "Primero ejecuta INICIAR_MVP.command al menos una vez."
  read -p "Presiona Enter para cerrar..."
  exit 1
fi
source .venv/bin/activate
python manage.py check
python manage.py test
echo ""
echo "Pruebas terminadas correctamente."
read -p "Presiona Enter para cerrar..."
