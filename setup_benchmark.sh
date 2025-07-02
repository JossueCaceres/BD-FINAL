#!/bin/bash

echo "======================================================"
echo "CONFIGURACIÓN AUTOMÁTICA - BENCHMARK BD-FINAL"
echo "======================================================"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Instalarlo primero."
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"

# Verificar PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL no está disponible. Verificar instalación."
    exit 1
fi

echo "✅ PostgreSQL encontrado: $(psql --version)"

# Instalar dependencias Python
echo ""
echo "📦 Instalando dependencias de Python..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas correctamente"
else
    echo "❌ Error instalando dependencias. Intentando método alternativo..."
    pip3 install psycopg2-binary
fi

# Verificar conexión a PostgreSQL
echo ""
echo "🔍 Verificando conexión a PostgreSQL..."
if pg_isready -h localhost -p 5432 &> /dev/null; then
    echo "✅ PostgreSQL está funcionando"
else
    echo "⚠️  PostgreSQL no responde en localhost:5432"
    echo "   Verificar que el servicio esté iniciado:"
    echo "   - macOS: brew services start postgresql"  
    echo "   - Linux: sudo systemctl start postgresql"
fi

# Verificar si la base de datos existe
echo ""
echo "🗄️  Verificando base de datos 'fredys_food'..."
if psql -h localhost -U postgres -lqt | cut -d \| -f 1 | grep -qw fredys_food; then
    echo "✅ Base de datos 'fredys_food' encontrada"
else
    echo "⚠️  Base de datos 'fredys_food' no encontrada"
    echo "   Crear la base de datos primero con los scripts del proyecto"
fi

# Hacer ejecutable el script de benchmark
chmod +x benchmark_queries.py

echo ""
echo "======================================================"
echo "✅ CONFIGURACIÓN COMPLETADA"
echo "======================================================"
echo ""
echo "Pasos siguientes:"
echo "1. Configurar credenciales en benchmark_queries.py"
echo "2. Ejecutar: python3 benchmark_queries.py"
echo "3. Copiar tablas LaTeX generadas al documento"
echo ""
echo "Para más información ver: README_benchmark.md"
