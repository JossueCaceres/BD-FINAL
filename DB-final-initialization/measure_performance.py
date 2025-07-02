#!/usr/bin/env python3
"""
Script de Medición de Tiempos para Consultas SQL
Proyecto: Fredys Food Database Performance Analysis

Este script implementa la metodología experimental descrita en el documento:
- Medición de tiempos con y sin índices
- Múltiples ejecuciones para obtener promedios estadísticamente válidos
- Limpieza de caché entre ejecuciones
- Configuración controlada de PostgreSQL
- Generación automática de reportes para LaTeX

Autor: Proyecto BD Final
Fecha: Julio 2025
"""

import psycopg2
import time
import statistics
import json
import sys
import os
from datetime import datetime


class DatabasePerformanceTester:
    def __init__(self, host="localhost", database="final_project", 
                 user="postgres", password="password123", port=5433):
        self.connection_params = {
            'host': host,
            'database': database, 
            'user': user,
            'password': password,
            'port': port
        }
        self.results = {}
        
    def connect(self):
        """Establecer conexión limpia a la base de datos"""
        try:
            conn = psycopg2.connect(**self.connection_params)
            conn.autocommit = True
            return conn
        except Exception as e:
            print(f"Error conectando a la base de datos: {e}")
            sys.exit(1)
    
    def prepare_database_for_testing(self, cursor):
        """Configurar PostgreSQL para mediciones controladas según metodología"""
        print("🔧 Configurando PostgreSQL para mediciones controladas...")
        
        # Configuraciones optimizadas para usar índices efectivamente
        config_queries = [
            # Permitir uso de índices pero desactivar algunas optimizaciones para medición pura
            "SET enable_indexscan = ON",
            "SET enable_indexonlyscan = ON", 
            "SET enable_bitmapscan = ON",
            "SET enable_seqscan = ON",  # Permitir seq scan para comparación
            
            # Desactivar optimizaciones que pueden enmascarar diferencias
            "SET enable_mergejoin = OFF",
            "SET enable_hashjoin = OFF", 
            "SET enable_sort = OFF",
            "SET enable_material = OFF",
            
            # Configurar costos para favorecer índices cuando sea apropiado
            "SET random_page_cost = 4.0",
            "SET seq_page_cost = 1.0",
            "SET cpu_index_tuple_cost = 0.005",
            "SET cpu_operator_cost = 0.0025",
            
            # Configuración de memoria para operaciones
            "SET effective_cache_size = '1GB'",
            "SET work_mem = '8MB'",
            "SET maintenance_work_mem = '256MB'"
        ]
        
        for query in config_queries:
            try:
                cursor.execute(query)
                print(f"✅ {query}")
            except Exception as e:
                print(f"⚠️  Error en configuración: {query} - {e}")
    
    def clean_cache_and_analyze(self, cursor):
        """Limpiar caché y actualizar estadísticas según metodología"""
        print("🧹 Limpiando caché y actualizando estadísticas...")
        try:
            # VACUUM FULL para liberar caché como indica la metodología
            cursor.execute("VACUUM FULL")
            # ANALYZE para actualizar estadísticas del planificador
            cursor.execute("ANALYZE")
            print("✅ Caché limpiado y estadísticas actualizadas")
        except Exception as e:
            print(f"⚠️  Error limpiando caché: {e}")
    
    def get_query_definitions(self):
        """Obtener las 4 consultas experimentales del documento"""
        return {
            "consulta_1": {
                "name": "Platos populares con información del administrador y zona",
                "sql": """
                SELECT 
                    p.nombre AS nombre_plato,
                    p.categoria,
                    p.precio,
                    u.nombre || ' ' || u.apellido AS administrador_creador,
                    pd.zona_entrega,
                    COUNT(DISTINCT pd.id_pedido) AS total_pedidos,
                    ROUND(AVG(h.calificacion::numeric), 2) AS calificacion_promedio,
                    COUNT(h.calificacion) AS total_calificaciones,
                    SUM(p.precio) AS ingresos_generados
                FROM Plato p
                JOIN Pertenece pe ON p.id_plato = pe.id_plato
                JOIN Menu m ON pe.id_menu = m.id_menu
                JOIN Administrador a ON m.id_administrador = a.id_usuario
                JOIN Usuario u ON a.id_usuario = u.id_usuario
                JOIN Tiene t ON m.id_menu = t.id_menu
                JOIN Pedido pd ON t.id_pedido = pd.id_pedido
                LEFT JOIN Hace h ON pd.id_pedido = h.id_pedido
                WHERE pd.fecha >= CURRENT_DATE - INTERVAL '30 days'
                  AND pd.estado = 'Entregado'
                GROUP BY p.id_plato, p.nombre, p.categoria, p.precio, 
                         u.nombre, u.apellido, pd.zona_entrega
                HAVING COUNT(DISTINCT pd.id_pedido) >= 5
                ORDER BY total_pedidos DESC, calificacion_promedio DESC
                LIMIT 15;
                """
            },
            "consulta_2": {
                "name": "Rendimiento de entregas por zona con información de repartidores",
                "sql": """
                SELECT 
                    pd.zona_entrega,
                    ze.costo AS costo_zona,
                    COUNT(pd.id_pedido) AS total_entregas,
                    COUNT(CASE WHEN pd.estado = 'Entregado' THEN 1 END) AS entregas_exitosas,
                    ROUND(
                        COUNT(CASE WHEN pd.estado = 'Entregado' THEN 1 END)::numeric / 
                        COUNT(pd.id_pedido)::numeric * 100, 2
                    ) AS porcentaje_exito,
                    ROUND(AVG(
                        EXTRACT(EPOCH FROM (pd.hora_entrega - pd.hora_salida)) / 60
                    ), 2) AS tiempo_promedio_minutos,
                    ROUND(AVG(
                        EXTRACT(EPOCH FROM (pd.hora_entrega - pd.hora_entrega_estimada)) / 60
                    ), 2) AS diferencia_estimado_real,
                    COUNT(DISTINCT c.id_usuario) AS repartidores_activos,
                    STRING_AGG(DISTINCT u.nombre || ' ' || u.apellido, ', ') AS nombres_repartidores
                FROM Pedido pd
                JOIN ZonaEntrega ze ON pd.zona_entrega = ze.nombre
                JOIN Cubre c ON pd.zona_entrega = c.zona_entrega
                JOIN Usuario u ON c.id_usuario = u.id_usuario
                WHERE pd.fecha >= CURRENT_DATE - INTERVAL '30 days'
                  AND pd.hora_salida IS NOT NULL
                  AND pd.hora_entrega IS NOT NULL
                  AND pd.hora_entrega_estimada IS NOT NULL
                GROUP BY pd.zona_entrega, ze.costo
                HAVING COUNT(pd.id_pedido) >= 5
                ORDER BY porcentaje_exito DESC, tiempo_promedio_minutos ASC;
                """
            },
            "consulta_3": {
                "name": "Repartidores con mejor desempeño por zona",
                "sql": """
                SELECT 
                    u.nombre || ' ' || u.apellido AS nombre_repartidor,
                    t.nro_telef_emergencia AS telefono_emergencia,
                    c.zona_entrega,
                    COUNT(pd.id_pedido) AS entregas_realizadas,
                    COUNT(CASE WHEN pd.estado = 'Entregado' THEN 1 END) AS entregas_exitosas,
                    ROUND(
                        COUNT(CASE WHEN pd.estado = 'Entregado' THEN 1 END)::numeric / 
                        COUNT(pd.id_pedido)::numeric * 100, 2
                    ) AS tasa_exito,
                    ROUND(AVG(h.calificacion::numeric), 2) AS calificacion_promedio,
                    ROUND(AVG(
                        EXTRACT(EPOCH FROM (pd.hora_entrega - pd.hora_salida)) / 60
                    ), 2) AS tiempo_promedio_entrega,
                    COUNT(DISTINCT DATE(pd.fecha)) AS dias_trabajados,
                    ROW_NUMBER() OVER (
                        PARTITION BY c.zona_entrega 
                        ORDER BY COUNT(CASE WHEN pd.estado = 'Entregado' THEN 1 END) DESC,
                                 AVG(h.calificacion::numeric) DESC
                    ) AS ranking_zona
                FROM Usuario u
                JOIN Trabajador t ON u.id_usuario = t.id_usuario
                JOIN Repartidor r ON t.id_usuario = r.id_usuario
                JOIN Cubre c ON r.id_usuario = c.id_usuario
                JOIN Pedido pd ON pd.zona_entrega = c.zona_entrega
                LEFT JOIN Hace h ON pd.id_pedido = h.id_pedido
                WHERE pd.estado IN ('Entregado', 'En reparto')
                  AND pd.fecha >= CURRENT_DATE - INTERVAL '30 days'
                  AND pd.hora_salida IS NOT NULL
                  AND pd.hora_entrega IS NOT NULL
                GROUP BY u.id_usuario, u.nombre, u.apellido, t.nro_telef_emergencia, c.zona_entrega
                HAVING COUNT(pd.id_pedido) >= 3
                ORDER BY c.zona_entrega, ranking_zona;
                """
            },
            "consulta_4": {
                "name": "Clientes más activos y patrones de consumo",
                "sql": """
                SELECT 
                    u.nombre || ' ' || u.apellido AS nombre_cliente,
                    cl.empresa,
                    v.zona_entrega,
                    COUNT(pd.id_pedido) AS total_pedidos,
                    ROUND(AVG(p.precio), 2) AS ticket_promedio,
                    SUM(p.precio) AS valor_total_consumido,
                    COUNT(DISTINCT pe.id_plato) AS variedad_platos_consumidos,
                    COUNT(DISTINCT DATE(pd.fecha)) AS dias_activos,
                    ROUND(AVG(h.calificacion::numeric), 2) AS calificacion_promedio,
                    MAX(pd.fecha) AS ultimo_pedido,
                    STRING_AGG(DISTINCT p.categoria, ', ') AS categorias_preferidas,
                    CASE 
                        WHEN COUNT(pd.id_pedido) >= 20 THEN 'Cliente VIP'
                        WHEN COUNT(pd.id_pedido) >= 10 THEN 'Cliente Frecuente'
                        WHEN COUNT(pd.id_pedido) >= 5 THEN 'Cliente Regular'
                        ELSE 'Cliente Ocasional'
                    END AS categoria_fidelidad,
                    EXTRACT(DAYS FROM (CURRENT_DATE - MAX(pd.fecha))) AS dias_sin_pedido
                FROM Usuario u
                JOIN Cliente cl ON u.id_usuario = cl.id_usuario
                JOIN Vive v ON u.id_usuario = v.id_usuario
                JOIN Hace ha ON u.id_usuario = ha.id_usuario
                JOIN Pedido pd ON ha.id_pedido = pd.id_pedido
                JOIN Tiene t ON pd.id_pedido = t.id_pedido
                JOIN Menu m ON t.id_menu = m.id_menu
                JOIN Pertenece pe ON m.id_menu = pe.id_menu
                JOIN Plato p ON pe.id_plato = p.id_plato
                LEFT JOIN Hace h ON pd.id_pedido = h.id_pedido
                WHERE pd.fecha >= CURRENT_DATE - INTERVAL '60 days'
                  AND pd.estado = 'Entregado'
                GROUP BY u.id_usuario, u.nombre, u.apellido, cl.empresa, v.zona_entrega
                HAVING COUNT(pd.id_pedido) >= 3
                ORDER BY total_pedidos DESC, valor_total_consumido DESC
                LIMIT 20;
                """
            }
        }
    
    def get_index_definitions(self):
        """Índices optimizados basados en análisis detallado de cada consulta"""
        return {
            "indices_consulta_1": [
                # Consulta 1: Platos populares - Optimizado para JOINs y filtros
                "CREATE INDEX idx_pedido_fecha_estado_zona ON Pedido(fecha DESC, estado, zona_entrega) WHERE estado = 'Entregado'",
                "CREATE INDEX idx_plato_id_categoria ON Plato(id_plato, categoria, precio)",
                "CREATE INDEX idx_pertenece_plato_menu ON Pertenece(id_plato, id_menu)",
                "CREATE INDEX idx_menu_id_admin ON Menu(id_menu, id_administrador)",
                "CREATE INDEX idx_tiene_menu_pedido ON Tiene(id_menu, id_pedido)",
                "CREATE INDEX idx_hace_pedido_calificacion ON Hace(id_pedido, calificacion)",
                "CREATE INDEX idx_administrador_usuario ON Administrador(id_usuario)"
            ],
            "indices_consulta_2": [
                # Consulta 2: Rendimiento entregas - Optimizado para agregaciones por zona
                "CREATE INDEX idx_pedido_zona_fecha_horas ON Pedido(zona_entrega, fecha DESC, estado, hora_salida, hora_entrega, hora_entrega_estimada)",
                "CREATE INDEX idx_zona_entrega_nombre_costo ON ZonaEntrega(nombre, costo)",
                "CREATE INDEX idx_cubre_zona_usuario ON Cubre(zona_entrega, id_usuario)",
                "CREATE INDEX idx_usuario_id_nombre ON Usuario(id_usuario, nombre, apellido)"
            ],
            "indices_consulta_3": [
                # Consulta 3: Repartidores por zona - Optimizado para la cadena de JOINs
                "CREATE INDEX idx_repartidor_usuario ON Repartidor(id_usuario)",
                "CREATE INDEX idx_trabajador_id_telefono ON Trabajador(id_usuario, nro_telef_emergencia)",
                "CREATE INDEX idx_usuario_id_nombre_apellido ON Usuario(id_usuario, nombre, apellido)",
                "CREATE INDEX idx_cubre_usuario_zona_rep ON Cubre(id_usuario, zona_entrega)",
                "CREATE INDEX idx_pedido_zona_estado_fecha_horas ON Pedido(zona_entrega, estado, fecha DESC, hora_salida, hora_entrega) WHERE estado IN ('Entregado', 'En reparto')",
                "CREATE INDEX idx_hace_pedido_usuario_calificacion ON Hace(id_pedido, id_usuario, calificacion)"
            ],
            "indices_consulta_4": [
                # Consulta 4: Clientes activos - Optimizado para múltiples JOINs
                "CREATE INDEX idx_cliente_usuario_empresa ON Cliente(id_usuario, empresa)",
                "CREATE INDEX idx_vive_usuario_zona ON Vive(id_usuario, zona_entrega)",
                "CREATE INDEX idx_hace_usuario_pedido_calificacion ON Hace(id_usuario, id_pedido, calificacion)",
                "CREATE INDEX idx_pedido_fecha_estado_cliente ON Pedido(fecha DESC, estado, id_pedido) WHERE estado = 'Entregado'",
                "CREATE INDEX idx_tiene_pedido_menu ON Tiene(id_pedido, id_menu)",
                "CREATE INDEX idx_menu_id_pertenece ON Menu(id_menu)",
                "CREATE INDEX idx_pertenece_menu_plato_opt ON Pertenece(id_menu, id_plato)",
                "CREATE INDEX idx_plato_id_categoria_precio ON Plato(id_plato, categoria, precio)"
            ]
        }
    
    def execute_timed_query(self, cursor, query, query_name):
        """Ejecutar consulta con medición de tiempo usando EXPLAIN ANALYZE"""
        try:
            # Usar EXPLAIN ANALYZE para obtener tiempo real de ejecución
            explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"
            
            start_time = time.time()
            cursor.execute(explain_query)
            end_time = time.time()
            
            result = cursor.fetchone()[0][0]  # Obtener el JSON del plan
            execution_time = result['Execution Time']  # Tiempo real en ms
            
            return execution_time
            
        except Exception as e:
            print(f"❌ Error ejecutando {query_name}: {e}")
            return None
    
    def measure_query_performance(self, query_dict, data_size, with_indexes=False):
        """Medir rendimiento de todas las consultas según metodología (10 ejecuciones)"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Configurar base de datos para mediciones
        self.prepare_database_for_testing(cursor)
        
        results = {}
        
        for query_id, query_info in query_dict.items():
            print(f"\n📊 Midiendo {query_info['name']} ({'CON' if with_indexes else 'SIN'} índices)...")
            
            times = []
            
            # 10 ejecuciones + 1 de warm-up (que se descarta)
            for i in range(11):
                # Limpiar caché entre ejecuciones según metodología
                self.clean_cache_and_analyze(cursor)
                
                # Pequeña pausa para estabilizar el sistema
                time.sleep(0.5)
                
                execution_time = self.execute_timed_query(
                    cursor, query_info['sql'], f"{query_id}_run_{i}"
                )
                
                if execution_time is not None:
                    # Descartar primera ejecución (warm-up)
                    if i > 0:
                        times.append(execution_time)
                        print(f"  Ejecución {i}: {execution_time:.2f} ms")
                else:
                    print(f"  ⚠️  Error en ejecución {i}")
            
            if times:
                # Calcular estadísticas
                avg_time = statistics.mean(times)
                std_dev = statistics.stdev(times) if len(times) > 1 else 0
                
                results[query_id] = {
                    'name': query_info['name'],
                    'times': times,
                    'average': avg_time,
                    'std_dev': std_dev,
                    'min': min(times),
                    'max': max(times),
                    'data_size': data_size,
                    'with_indexes': with_indexes
                }
                
                print(f"  📈 Promedio: {avg_time:.2f} ms (±{std_dev:.2f})")
            else:
                print(f"  ❌ No se pudieron obtener mediciones válidas para {query_id}")
        
        cursor.close()
        conn.close()
        
        return results
    
    def create_indexes(self):
        """Crear todos los índices definidos en el documento"""
        conn = self.connect()
        cursor = conn.cursor()
        
        print("\n🔨 Creando índices optimizados...")
        
        index_definitions = self.get_index_definitions()
        created_indexes = []
        
        for group_name, indexes in index_definitions.items():
            print(f"\n📁 Creando índices para {group_name}:")
            
            for index_sql in indexes:
                try:
                    cursor.execute(index_sql)
                    created_indexes.append(index_sql)
                    print(f"  ✅ {index_sql}")
                except Exception as e:
                    print(f"  ❌ Error creando índice: {index_sql}")
                    print(f"     Error: {e}")
        
        cursor.close()
        conn.close()
        
        print(f"\n🎉 Se crearon {len(created_indexes)} índices exitosamente")
        return created_indexes
    
    def drop_indexes(self):
        """Eliminar todos los índices personalizados para medición sin índices"""
        conn = self.connect()
        cursor = conn.cursor()
        
        print("\n🗑️  Eliminando índices personalizados...")
        
        # Obtener lista de índices personalizados (excluyendo los del sistema)
        cursor.execute("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND indexname LIKE 'idx_%'
        """)
        
        indexes_to_drop = cursor.fetchall()
        
        for (index_name,) in indexes_to_drop:
            try:
                cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
                print(f"  🗑️  Eliminado: {index_name}")
            except Exception as e:
                print(f"  ⚠️  Error eliminando {index_name}: {e}")
        
        cursor.close()
        conn.close()
    
    def check_data_volume(self):
        """Verificar volumen de datos disponible en cada tabla"""
        conn = self.connect()
        cursor = conn.cursor()
        
        tables = ['Usuario', 'Cliente', 'Pedido', 'Menu', 'Plato', 'Pertenece', 
                 'Tiene', 'Hace', 'ZonaEntrega', 'Cubre', 'Vive']
        
        print("\n📊 Verificando volumen de datos por tabla:")
        total_records = 0
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count:,} registros")
                total_records += count
            except Exception as e:
                print(f"  ❌ Error consultando {table}: {e}")
        
        cursor.close()
        conn.close()
        
        print(f"\n📈 Total de registros en el sistema: {total_records:,}")
        return total_records
    
    def estimate_data_scale(self, total_records):
        """Estimar escala de datos basada en total de registros"""
        if total_records < 5000:
            return "1K"
        elif total_records < 50000:
            return "10K" 
        elif total_records < 500000:
            return "100K"
        else:
            return "1M"
    
    def run_full_performance_test(self):
        """Ejecutar test completo de rendimiento siguiendo la metodología"""
        print("🚀 INICIANDO TEST COMPLETO DE RENDIMIENTO")
        print("=" * 60)
        
        # Verificar datos disponibles
        total_records = self.check_data_volume()
        data_scale = self.estimate_data_scale(total_records)
        
        if total_records < 1000:
            print("⚠️  ADVERTENCIA: Volumen de datos muy bajo para mediciones significativas")
            print("   Ejecute: python main.py 1000 para generar más datos")
            response = input("¿Continuar de todas formas? (y/N): ")
            if response.lower() != 'y':
                return
        
        print(f"\n📏 Escala de datos detectada: {data_scale} ({total_records:,} registros)")
        
        # Obtener definiciones de consultas
        queries = self.get_query_definitions()
        
        # Fase 1: Medición SIN índices
        print("\n" + "="*60)
        print("📊 FASE 1: MEDICIÓN SIN ÍNDICES")
        print("="*60)
        
        self.drop_indexes()  # Asegurar que no hay índices personalizados
        results_without_indexes = self.measure_query_performance(
            queries, data_scale, with_indexes=False
        )
        
        # Fase 2: Crear índices y medir CON índices
        print("\n" + "="*60)
        print("📊 FASE 2: MEDICIÓN CON ÍNDICES")
        print("="*60)
        
        self.create_indexes()
        results_with_indexes = self.measure_query_performance(
            queries, data_scale, with_indexes=True
        )
        
        # Almacenar resultados
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'data_scale': data_scale,
            'total_records': total_records,
            'without_indexes': results_without_indexes,
            'with_indexes': results_with_indexes
        }
        
        # Generar reportes
        self.generate_reports()
        
        print("\n🎉 TEST DE RENDIMIENTO COMPLETADO")
        print(f"📁 Resultados guardados en: performance_results_{data_scale}.json")
        
    def calculate_improvements(self):
        """Calcular mejoras de rendimiento con índices"""
        improvements = {}
        
        if 'without_indexes' not in self.results or 'with_indexes' not in self.results:
            return improvements
        
        for query_id in self.results['without_indexes'].keys():
            if query_id in self.results['with_indexes']:
                time_without = self.results['without_indexes'][query_id]['average']
                time_with = self.results['with_indexes'][query_id]['average']
                
                if time_without > 0:
                    improvement_percent = ((time_without - time_with) / time_without) * 100
                    speedup_factor = time_without / time_with if time_with > 0 else float('inf')
                    
                    improvements[query_id] = {
                        'time_without': time_without,
                        'time_with': time_with,
                        'improvement_percent': improvement_percent,
                        'speedup_factor': speedup_factor
                    }
        
        return improvements
    
    def generate_latex_table(self, data_scale):
        """Generar código LaTeX para las tablas del documento"""
        if not self.results:
            return ""
        
        improvements = self.calculate_improvements()
        
        latex_code = f"""
% Tablas generadas automáticamente - {datetime.now().strftime('%Y-%m-%d %H:%M')}
% Escala de datos: {data_scale}

% Tabla: Tiempos sin índices
\\begin{{table}}[h!]
\\centering
\\begin{{tabular}}{{|l|c|}}
\\hline
\\textbf{{Consulta}} & \\textbf{{{data_scale} (ms)}} \\\\
\\hline
"""
        
        # Agregar datos sin índices
        if 'without_indexes' in self.results:
            for i, (query_id, data) in enumerate(self.results['without_indexes'].items(), 1):
                avg_time = data['average']
                latex_code += f"Consulta {i} & {avg_time:.1f} \\\\\n"
        
        latex_code += """\\hline
\\end{tabular}
\\caption{Tiempos de ejecución sin índices (promedio de 10 ejecuciones)}
\\label{table:sin_indices_""" + data_scale.lower() + """}
\\end{table}

% Tabla: Tiempos con índices
\\begin{table}[h!]
\\centering
\\begin{tabular}{|l|c|}
\\hline
\\textbf{Consulta} & \\textbf{""" + data_scale + """ (ms)} \\\\
\\hline
"""
        
        # Agregar datos con índices
        if 'with_indexes' in self.results:
            for i, (query_id, data) in enumerate(self.results['with_indexes'].items(), 1):
                avg_time = data['average']
                latex_code += f"Consulta {i} & {avg_time:.1f} \\\\\n"
        
        latex_code += """\\hline
\\end{tabular}
\\caption{Tiempos de ejecución con índices (promedio de 10 ejecuciones)}
\\label{table:con_indices_""" + data_scale.lower() + """}
\\end{table}

% Mejoras de rendimiento
\\subsection{Resultados para """ + data_scale + """}

"""
        
        # Agregar análisis de mejoras
        for i, (query_id, improvement) in enumerate(improvements.items(), 1):
            improvement_percent = improvement['improvement_percent']
            latex_code += f"\\subsubsection{{Consulta {i}}}\n"
            latex_code += f"Mejora de rendimiento: {improvement_percent:.1f}\\% más rápida\\\\\n"
            latex_code += f"Tiempo sin índices: {improvement['time_without']:.1f} ms\\\\\n"
            latex_code += f"Tiempo con índices: {improvement['time_with']:.1f} ms\\\\\n\n"
        
        return latex_code
    
    def generate_reports(self):
        """Generar reportes en JSON y LaTeX"""
        if not self.results:
            print("❌ No hay resultados para generar reportes")
            return
        
        data_scale = self.results['data_scale']
        
        # Guardar resultados detallados en JSON
        json_filename = f"performance_results_{data_scale}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Generar código LaTeX
        latex_code = self.generate_latex_table(data_scale)
        latex_filename = f"performance_tables_{data_scale}.tex"
        
        with open(latex_filename, 'w', encoding='utf-8') as f:
            f.write(latex_code)
        
        # Mostrar resumen en consola
        print("\n" + "="*60)
        print("📊 RESUMEN DE RESULTADOS")
        print("="*60)
        
        improvements = self.calculate_improvements()
        
        for i, (query_id, improvement) in enumerate(improvements.items(), 1):
            print(f"\n📈 Consulta {i}:")
            print(f"  Sin índices: {improvement['time_without']:.1f} ms")
            print(f"  Con índices: {improvement['time_with']:.1f} ms") 
            print(f"  Mejora: {improvement['improvement_percent']:.1f}% más rápida")
            print(f"  Factor: {improvement['speedup_factor']:.1f}x más rápida")
        
        print(f"\n📁 Archivos generados:")
        print(f"  • {json_filename} - Datos completos en JSON")
        print(f"  • {latex_filename} - Tablas para LaTeX")


def main():
    """Función principal"""
    print("🎯 SCRIPT DE MEDICIÓN DE RENDIMIENTO - Fredys Food Database")
    print("🔬 Implementa metodología experimental del documento académico")
    print("-" * 60)
    
    # Crear instancia del tester
    tester = DatabasePerformanceTester()
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("""
Uso: python measure_performance.py [opciones]

Opciones:
  -h, --help     Mostrar esta ayuda
  --check-data   Solo verificar volumen de datos
  --create-indexes Solo crear índices
  --drop-indexes Solo eliminar índices
  
Sin argumentos: Ejecutar test completo de rendimiento

Requisitos:
  1. PostgreSQL ejecutándose
  2. Base de datos 'final_project' creada
  3. Esquema creado con create_schema.sql
  4. Datos generados con main.py
  
Ejemplo de uso completo:
  python create_schema.sql  # Crear esquema
  python main.py 10000      # Generar 10K registros
  python measure_performance.py  # Medir rendimiento
            """)
            return
        elif sys.argv[1] == '--check-data':
            tester.check_data_volume()
            return
        elif sys.argv[1] == '--create-indexes':
            tester.create_indexes()
            return
        elif sys.argv[1] == '--drop-indexes':
            tester.drop_indexes()
            return
    
    # Ejecutar test completo
    try:
        tester.run_full_performance_test()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
