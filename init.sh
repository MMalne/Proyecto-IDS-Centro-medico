#!/bin/bash
# init.sh - Script de inicialización de entorno y dependencias

echo "Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "Instalando dependencias del proyecto..."
pip install Flask mysql-connector-python qrcode[pil] requests

echo "Dependencias instaladas correctamente."