#!/bin/bash
# Script de configuración para el entorno de medición de rendimiento
# Fredys Food Database Performance Testing

echo "🔧 CONFIGURANDO ENTORNO DE MEDICIÓN DE RENDIMIENTO"
echo "=================================================="

# Verificar Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "✅ $python_version encontrado"
else
    echo "❌ Python 3 no encontrado. Por favor instale Python 3.7 o superior"
    exit 1
fi

# Verificar PostgreSQL
echo ""
echo "🐘 Verificando PostgreSQL..."
if command -v psql &> /dev/null; then
    pg_version=$(psql --version)
    echo "✅ $pg_version encontrado"
else
    echo "❌ PostgreSQL no encontrado. Por favor instale PostgreSQL"
    exit 1
fi

# Instalar dependencias Python
echo ""
echo "📦 Instalando dependencias Python..."
if pip3 install -r requirements.txt; then
    echo "✅ Dependencias instaladas correctamente"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi

# Verificar conexión a PostgreSQL
echo ""
echo "🔌 Verificando conexión a PostgreSQL..."

# Intentar conectar con las credenciales por defecto
if psql -h localhost -U postgres -d postgres -c "SELECT 1;" &> /dev/null; then
    echo "✅ Conexión a PostgreSQL exitosa"
else
    echo "⚠️  No se puede conectar a PostgreSQL con las credenciales por defecto"
    echo "   Por favor verifique que PostgreSQL esté ejecutándose"
    echo "   y que las credenciales en measure_performance.py sean correctas"
fi

# Verificar si existe la base de datos
echo ""
echo "🗄️  Verificando base de datos final_project..."
if psql -h localhost -U postgres -d final_project -c "SELECT 1;" &> /dev/null; then
    echo "✅ Base de datos 'final_project' encontrada"
else
    echo "⚠️  Base de datos 'final_project' no encontrada"
    echo "   Creando base de datos..."
    
    if psql -h localhost -U postgres -c "CREATE DATABASE final_project;" &> /dev/null; then
        echo "✅ Base de datos 'final_project' creada"
    else
        echo "❌ Error creando base de datos. Verifique permisos."
    fi
fi

# Verificar esquema
echo ""
echo "📋 Verificando esquema de tablas..."
if psql -h localhost -U postgres -d final_project -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" &> /dev/null; then
    table_count=$(psql -h localhost -U postgres -d final_project -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
    table_count=$(echo $table_count | xargs)  # Trim whitespace
    
    if [ "$table_count" -gt "0" ]; then
        echo "✅ Esquema encontrado ($table_count tablas)"
    else
        echo "⚠️  No se encontraron tablas. Ejecutando create_schema.sql..."
        if psql -h localhost -U postgres -d final_project -f create_schema.sql &> /dev/null; then
            echo "✅ Esquema creado exitosamente"
        else
            echo "❌ Error creando esquema"
        fi
    fi
else
    echo "❌ Error verificando esquema"
fi

# Verificar datos
echo ""
echo "📊 Verificando datos en tablas..."
if psql -h localhost -U postgres -d final_project -c "SELECT COUNT(*) FROM Usuario;" &> /dev/null; then
    user_count=$(psql -h localhost -U postgres -d final_project -t -c "SELECT COUNT(*) FROM Usuario;")
    user_count=$(echo $user_count | xargs)
    
    if [ "$user_count" -gt "0" ]; then
        echo "✅ Datos encontrados ($user_count usuarios)"
    else
        echo "⚠️  No se encontraron datos. Ejecute:"
        echo "     python3 main.py 1000    # Para 1K registros"
        echo "     python3 main.py 10000   # Para 10K registros"
        echo "     python3 main.py 100000  # Para 100K registros"
    fi
else
    echo "❌ Error verificando datos"
fi

echo ""
echo "🚀 CONFIGURACIÓN COMPLETADA"
echo "=========================="
echo ""
echo "📚 Pasos siguientes:"
echo ""
echo "1. Si no tiene datos, genere datos de prueba:"
echo "   python3 main.py 10000"
echo ""
echo "2. Ejecute el test de rendimiento:"
echo "   python3 measure_performance.py"
echo ""
echo "3. Los resultados se guardarán en:"
echo "   - performance_results_[escala].json"
echo "   - performance_tables_[escala].tex"
echo ""
echo "4. Use el archivo .tex para actualizar el documento LaTeX"
echo ""
echo "🎯 Para obtener resultados más robustos, use escalas de datos mayores:"
echo "   - 1K registros: Pruebas rápidas"
echo "   - 10K registros: Pruebas estándar"  
echo "   - 100K registros: Pruebas completas"
echo "   - 1M registros: Pruebas de escala empresarial"
