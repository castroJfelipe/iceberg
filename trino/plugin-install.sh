#!/bin/bash
set -e

echo "⚙️ Descargando plugin de Ranger para Trino..."
wget -q https://downloads.apache.org/ranger/2.4.0/ranger-2.4.0-trino-plugin.tar.gz -O /tmp/ranger-plugin.tar.gz

echo "📦 Extrayendo plugin..."
mkdir -p /usr/lib/trino/plugin/ranger
tar -xzf /tmp/ranger-plugin.tar.gz -C /usr/lib/trino/plugin/ranger --strip-components=1

echo "🔌 Plugin de Ranger instalado en /usr/lib/trino/plugin/ranger"
