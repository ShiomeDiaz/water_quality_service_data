#!/bin/bash
set -e

# Crea el entorno virtual si no existe
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activa el entorno virtual
source venv/bin/activate

# Instala dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Ejecuta el microservicio
python dataservicio.py
