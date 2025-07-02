#!/usr/bin/env python3
"""
Script temporal para ejecutar create_schema.sql
"""
import psycopg2

def main():
    # Leer el archivo SQL
    with open('create_schema.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()

    try:
        conn = psycopg2.connect(
            host='localhost',
            database='final_project',
            user='postgres', 
            password='password123',
            port=5433
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print('🔨 Ejecutando script de creación de esquema...')
        cursor.execute(sql_content)
        print('✅ Esquema creado exitosamente')
        
        # Verificar tablas creadas
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cursor.fetchall()
        print(f'📊 Tablas creadas: {len(tables)}')
        for table in tables:
            print(f'  - {table[0]}')
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f'❌ Error ejecutando esquema: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
