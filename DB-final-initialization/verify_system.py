#!/usr/bin/env python3
"""
Script de Verificación Rápida
Verifica que todos los componentes estén funcionando correctamente
"""

import sys
import os

def check_imports():
    """Verificar que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias Python...")
    
    try:
        import psycopg2
        print("✅ psycopg2 - OK")
    except ImportError:
        print("❌ psycopg2 - FALTA (pip install psycopg2-binary)")
        return False
    
    try:
        from faker import Faker
        print("✅ Faker - OK")
    except ImportError:
        print("❌ Faker - FALTA (pip install Faker)")
        return False
    
    try:
        from faker_food import FoodProvider
        print("✅ faker_food - OK")
    except ImportError:
        print("❌ faker_food - FALTA (pip install faker_food)")
        return False
    
    return True

def check_database_connection():
    """Verificar conexión a PostgreSQL"""
    print("\n🔌 Verificando conexión a base de datos...")
    
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            database="final_project",
            user="postgres", 
            password="password123"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Conexión exitosa: {version}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def check_schema():
    """Verificar que el esquema esté creado"""
    print("\n📋 Verificando esquema de base de datos...")
    
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            database="final_project",
            user="postgres",
            password="password123"
        )
        cursor = conn.cursor()
        
        # Verificar tablas principales
        expected_tables = ['Usuario', 'Cliente', 'Trabajador', 'Repartidor', 
                          'Administrador', 'Menu', 'Plato', 'Pedido', 
                          'ZonaEntrega', 'Pertenece', 'Tiene', 'Hace', 'Vive', 'Cubre']
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = []
        for table in expected_tables:
            if table in existing_tables:
                print(f"✅ Tabla {table} - OK")
            else:
                print(f"❌ Tabla {table} - FALTA")
                missing_tables.append(table)
        
        cursor.close()
        conn.close()
        
        if missing_tables:
            print(f"\n⚠️  Faltan {len(missing_tables)} tablas. Ejecute:")
            print("   psql -U postgres -d final_project -f create_schema.sql")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando esquema: {e}")
        return False

def check_data():
    """Verificar que hay datos en la base"""
    print("\n📊 Verificando datos en base de datos...")
    
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            database="final_project", 
            user="postgres",
            password="password123"
        )
        cursor = conn.cursor()
        
        # Contar registros en tablas principales
        tables_to_check = ['Usuario', 'Pedido', 'Menu', 'Plato']
        total_records = 0
        
        for table in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"📈 {table}: {count:,} registros")
        
        cursor.close()
        conn.close()
        
        if total_records == 0:
            print("\n⚠️  No hay datos. Genere datos ejecutando:")
            print("   python3 main.py 1000")
            return False
        elif total_records < 1000:
            print(f"\n⚠️  Pocos datos ({total_records}). Para mejores mediciones:")
            print("   python3 main.py 10000")
        
        print(f"\n✅ Total: {total_records:,} registros disponibles")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🎯 VERIFICACIÓN RÁPIDA DEL SISTEMA")
    print("=" * 50)
    
    checks = [
        ("Dependencias Python", check_imports),
        ("Conexión Base de Datos", check_database_connection),
        ("Esquema de Tablas", check_schema),
        ("Datos Disponibles", check_data)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}:")
        print("-" * 30)
        if check_func():
            passed += 1
        else:
            print(f"❌ Verificación '{check_name}' falló")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡Sistema listo para ejecutar mediciones!")
        print("\nPasos siguientes:")
        print("1. python3 measure_performance.py")
        print("2. Usar archivos .tex generados en el documento")
    else:
        print("⚠️  Sistema requiere configuración adicional")
        print("\nSoluciones sugeridas:")
        if passed == 0:
            print("1. ./setup_performance_test.sh")
        print("2. Revisar README.md para configuración manual")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
