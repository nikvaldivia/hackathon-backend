#!/bin/bash

# Script para iniciar el proyecto Hackathon Backend
set -e

echo "🚀 Iniciando Hackathon Backend..."
echo ""

# Verificar que existe .env
echo "📋 Verificando archivo .env..."
[ -f .env ] || {
    [ -f .env.example ] && cp .env.example .env && echo "⚠️  Creado .env desde .env.example. Edita con tus credenciales."
    exit 1
}
echo "✅ Archivo .env encontrado"
echo ""

# Detectar Python (prioridad: python3, luego python)
echo "🐍 Detectando Python..."
if command -v python3 >/dev/null; then
    PYTHON=python3
    echo "✅ Python3 detectado: $(python3 --version)"
elif command -v python >/dev/null; then
    PYTHON=python
    echo "✅ Python detectado: $(python --version)"
else
    echo "❌ Python no instalado"; exit 1
fi
echo ""

# Verificar e instalar dependencias solo si es necesario
echo "📦 Verificando dependencias..."
$PYTHON -c "import fastapi, uvicorn, motor, google.generativeai" 2>/dev/null || {
    echo "⚠️  Algunas dependencias faltan"
    echo "📥 Instalando dependencias faltantes..."
    $PYTHON -m pip install --upgrade pip --quiet
    echo "   ✓ pip actualizado"
    $PYTHON -m pip install -r requirements.txt --quiet
    echo "   ✓ Dependencias instaladas desde requirements.txt"
} && echo "✅ Todas las dependencias están instaladas"
echo ""

# Ejecutar servidor
echo "🌐 Iniciando servidor..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$PYTHON server.py
