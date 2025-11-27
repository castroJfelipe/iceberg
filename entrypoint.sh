#!/bin/bash
set -e

echo "⏳ Instalando sqlalchemy-trino..."
pip install sqlalchemy-trino
pip install trino

echo "⚙️ Inicializando Superset..."
superset db upgrade
superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@superset.local \
    --password admin || echo "👤 Usuario admin ya existe"

superset init

echo "🚀 Ejecutando Superset en 0.0.0.0:8088"
exec superset run -h 0.0.0.0 -p 8088