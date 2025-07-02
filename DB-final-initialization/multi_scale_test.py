#!/usr/bin/env python3
"""
Script de Pruebas de Rendimiento Multi-Escala
Proyecto: Fredys Food Database Performance Analysis

Este script ejecuta pruebas de rendimiento automáticamente con diferentes escalas de datos:
- 1,000 registros (1K)
- 10,000 registros (10K) 
- 100,000 registros (100K)
- 1,000,000 registros (1M)

Genera reportes comparativos para analizar el comportamiento de los índices
en diferentes volúmenes de datos.
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime

class MultiScalePerformanceTester:
    def __init__(self):
        self.scales = [1000, 10000, 100000, 1000000]
        self.scale_names = ["1K", "10K", "100K", "1M"]
        self.results = {}
        
    def run_command(self, command, description):
        """Ejecutar comando del sistema con manejo de errores"""
        print(f"🔄 {description}...")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description} completado")
                return True, result.stdout
            else:
                print(f"❌ Error en {description}: {result.stderr}")
                return False, result.stderr
        except Exception as e:
            print(f"❌ Excepción ejecutando {description}: {e}")
            return False, str(e)
    
    def clean_and_recreate_schema(self):
        """Limpiar y recrear el esquema de base de datos"""
        print("\n🗑️  Limpiando esquema anterior...")
        success, _ = self.run_command("python run_schema.py", "Recreando esquema")
        return success
    
    def generate_data(self, scale):
        """Generar datos para la escala especificada"""
        scale_name = self.scale_names[self.scales.index(scale)]
        print(f"\n📊 Generando {scale:,} registros ({scale_name})...")
        
        success, output = self.run_command(f"python main.py {scale}", f"Generación de datos {scale_name}")
        if success:
            print(f"✅ {scale:,} registros generados exitosamente")
        return success
    
    def run_performance_test(self, scale):
        """Ejecutar test de rendimiento para la escala actual"""
        scale_name = self.scale_names[self.scales.index(scale)]
        print(f"\n🚀 Ejecutando pruebas de rendimiento para {scale_name} ({scale:,} registros)...")
        
        success, output = self.run_command("python measure_performance.py", f"Pruebas de rendimiento {scale_name}")
        
        if success:
            # Leer resultados del archivo JSON generado
            try:
                json_file = f"performance_results_{scale_name}.json"
                if os.path.exists(json_file):
                    with open(json_file, 'r', encoding='utf-8') as f:
                        self.results[scale_name] = json.load(f)
                    print(f"✅ Resultados {scale_name} guardados")
                    return True
                else:
                    print(f"⚠️  Archivo de resultados {json_file} no encontrado")
                    return False
            except Exception as e:
                print(f"❌ Error leyendo resultados {scale_name}: {e}")
                return False
        return False
    
    def estimate_time(self, scale):
        """Estimar tiempo necesario para una escala"""
        if scale <= 1000:
            return "2-3 minutos"
        elif scale <= 10000:
            return "5-8 minutos"
        elif scale <= 100000:
            return "15-25 minutos"
        else:
            return "45-90 minutos"
    
    def run_full_multi_scale_test(self):
        """Ejecutar test completo multi-escala"""
        print("🎯 SCRIPT DE PRUEBAS MULTI-ESCALA - Fredys Food Database")
        print("🔬 Análisis de rendimiento en diferentes volúmenes de datos")
        print("=" * 70)
        
        total_estimated_time = "2-3 horas"
        print(f"⏱️  Tiempo estimado total: {total_estimated_time}")
        print("📊 Escalas a probar: 1K, 10K, 100K, 1M registros")
        
        # Confirmación del usuario
        response = input("\n¿Desea continuar con todas las escalas? (y/N): ")
        if response.lower() != 'y':
            print("❌ Pruebas canceladas por el usuario")
            return
        
        start_time = datetime.now()
        successful_tests = 0
        
        for i, scale in enumerate(self.scales):
            scale_name = self.scale_names[i]
            estimated_time = self.estimate_time(scale)
            
            print(f"\n" + "="*70)
            print(f"📊 ESCALA {i+1}/4: {scale_name} ({scale:,} registros)")
            print(f"⏱️  Tiempo estimado: {estimated_time}")
            print("="*70)
            
            # Paso 1: Limpiar y recrear esquema
            if not self.clean_and_recreate_schema():
                print(f"❌ Error recreando esquema para {scale_name}")
                continue
            
            # Paso 2: Generar datos
            if not self.generate_data(scale):
                print(f"❌ Error generando datos para {scale_name}")
                continue
            
            # Paso 3: Ejecutar pruebas de rendimiento
            if not self.run_performance_test(scale):
                print(f"❌ Error en pruebas de rendimiento para {scale_name}")
                continue
            
            successful_tests += 1
            print(f"🎉 Escala {scale_name} completada exitosamente!")
            
            # Mostrar progreso
            elapsed = datetime.now() - start_time
            print(f"⏱️  Tiempo transcurrido: {elapsed}")
            
            if i < len(self.scales) - 1:
                print(f"📊 Progreso: {i+1}/{len(self.scales)} escalas completadas")
                time.sleep(2)  # Pausa breve entre escalas
        
        # Resumen final
        end_time = datetime.now()
        total_time = end_time - start_time
        
        print(f"\n" + "="*70)
        print("🎉 PRUEBAS MULTI-ESCALA COMPLETADAS")
        print("="*70)
        print(f"✅ Escalas exitosas: {successful_tests}/{len(self.scales)}")
        print(f"⏱️  Tiempo total: {total_time}")
        
        if successful_tests > 0:
            self.generate_comparative_report()
    
    def generate_comparative_report(self):
        """Generar reporte comparativo de todas las escalas"""
        print("\n📊 Generando reporte comparativo...")
        
        if not self.results:
            print("❌ No hay resultados para generar reporte")
            return
        
        # Generar archivo de resumen
        summary = {
            'timestamp': datetime.now().isoformat(),
            'scales_tested': list(self.results.keys()),
            'summary': {},
            'detailed_results': self.results
        }
        
        # Calcular resumen por consulta
        for scale_name, scale_data in self.results.items():
            if 'without_indexes' in scale_data and 'with_indexes' in scale_data:
                summary['summary'][scale_name] = {}
                
                for query_id in scale_data['without_indexes'].keys():
                    if query_id in scale_data['with_indexes']:
                        time_without = scale_data['without_indexes'][query_id]['average']
                        time_with = scale_data['with_indexes'][query_id]['average']
                        
                        if time_without > 0:
                            improvement = ((time_without - time_with) / time_without) * 100
                            speedup = time_without / time_with if time_with > 0 else float('inf')
                            
                            summary['summary'][scale_name][query_id] = {
                                'time_without_ms': time_without,
                                'time_with_ms': time_with,
                                'improvement_percent': improvement,
                                'speedup_factor': speedup
                            }
        
        # Guardar resumen
        summary_file = f"multi_scale_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Generar reporte LaTeX comparativo
        self.generate_comparative_latex()
        
        print(f"✅ Reporte comparativo guardado en: {summary_file}")
        print("📁 Archivos generados:")
        print(f"  • {summary_file} - Resumen completo")
        print("  • multi_scale_comparative.tex - Tablas LaTeX comparativas")
        
        # Mostrar resumen en consola
        self.print_console_summary()
    
    def generate_comparative_latex(self):
        """Generar tablas LaTeX comparativas"""
        latex_content = f"""
% Reporte Comparativo Multi-Escala - {datetime.now().strftime('%Y-%m-%d %H:%M')}
% Análisis de rendimiento con y sin índices en diferentes volúmenes de datos

\\section{{Resultados Comparativos por Escala de Datos}}

% Tabla comparativa: Tiempos sin índices
\\begin{{table}}[h!]
\\centering
\\begin{{tabular}}{{|l|{'c|' * len(self.results)}}}
\\hline
\\textbf{{Consulta}} & {' & '.join([f'\\textbf{{{scale}}}' for scale in self.results.keys()])} \\\\
\\hline
"""
        
        # Agregar datos sin índices
        for i in range(1, 5):  # 4 consultas
            query_id = f"consulta_{i}"
            row = [f"Consulta {i}"]
            
            for scale_name in self.results.keys():
                if ('without_indexes' in self.results[scale_name] and 
                    query_id in self.results[scale_name]['without_indexes']):
                    time_ms = self.results[scale_name]['without_indexes'][query_id]['average']
                    row.append(f"{time_ms:.1f} ms")
                else:
                    row.append("N/A")
            
            latex_content += " & ".join(row) + " \\\\\n"
        
        latex_content += """\\hline
\\end{tabular}
\\caption{Tiempos de ejecución SIN índices por escala de datos}
\\label{table:sin_indices_comparativo}
\\end{table}

% Tabla comparativa: Tiempos con índices
\\begin{table}[h!]
\\centering
\\begin{tabular}{|l|""" + 'c|' * len(self.results) + """}
\\hline
\\textbf{Consulta} & """ + ' & '.join([f'\\textbf{{{scale}}}' for scale in self.results.keys()]) + """ \\\\
\\hline
"""
        
        # Agregar datos con índices
        for i in range(1, 5):  # 4 consultas
            query_id = f"consulta_{i}"
            row = [f"Consulta {i}"]
            
            for scale_name in self.results.keys():
                if ('with_indexes' in self.results[scale_name] and 
                    query_id in self.results[scale_name]['with_indexes']):
                    time_ms = self.results[scale_name]['with_indexes'][query_id]['average']
                    row.append(f"{time_ms:.1f} ms")
                else:
                    row.append("N/A")
            
            latex_content += " & ".join(row) + " \\\\\n"
        
        latex_content += """\\hline
\\end{tabular}
\\caption{Tiempos de ejecución CON índices por escala de datos}
\\label{table:con_indices_comparativo}
\\end{table}

% Tabla de mejoras de rendimiento
\\begin{table}[h!]
\\centering
\\begin{tabular}{|l|""" + 'c|' * len(self.results) + """}
\\hline
\\textbf{Consulta} & """ + ' & '.join([f'\\textbf{{{scale}}}' for scale in self.results.keys()]) + """ \\\\
\\hline
"""
        
        # Agregar porcentajes de mejora
        for i in range(1, 5):  # 4 consultas
            query_id = f"consulta_{i}"
            row = [f"Consulta {i}"]
            
            for scale_name in self.results.keys():
                if ('without_indexes' in self.results[scale_name] and 
                    'with_indexes' in self.results[scale_name] and
                    query_id in self.results[scale_name]['without_indexes'] and
                    query_id in self.results[scale_name]['with_indexes']):
                    
                    time_without = self.results[scale_name]['without_indexes'][query_id]['average']
                    time_with = self.results[scale_name]['with_indexes'][query_id]['average']
                    
                    if time_without > 0:
                        improvement = ((time_without - time_with) / time_without) * 100
                        row.append(f"{improvement:.1f}\\%")
                    else:
                        row.append("N/A")
                else:
                    row.append("N/A")
            
            latex_content += " & ".join(row) + " \\\\\n"
        
        latex_content += """\\hline
\\end{tabular}
\\caption{Porcentaje de mejora con índices por escala de datos}
\\label{table:mejoras_comparativo}
\\end{table}
"""
        
        # Guardar archivo LaTeX
        with open('multi_scale_comparative.tex', 'w', encoding='utf-8') as f:
            f.write(latex_content)
    
    def print_console_summary(self):
        """Mostrar resumen en consola"""
        print(f"\n" + "="*70)
        print("📊 RESUMEN COMPARATIVO DE RESULTADOS")
        print("="*70)
        
        for scale_name in self.results.keys():
            if 'total_records' in self.results[scale_name]:
                total_records = self.results[scale_name]['total_records']
                print(f"\n📈 {scale_name} ({total_records:,} registros totales):")
                
                if ('without_indexes' in self.results[scale_name] and 
                    'with_indexes' in self.results[scale_name]):
                    
                    for i, query_id in enumerate(['consulta_1', 'consulta_2', 'consulta_3', 'consulta_4'], 1):
                        if (query_id in self.results[scale_name]['without_indexes'] and
                            query_id in self.results[scale_name]['with_indexes']):
                            
                            time_without = self.results[scale_name]['without_indexes'][query_id]['average']
                            time_with = self.results[scale_name]['with_indexes'][query_id]['average']
                            improvement = ((time_without - time_with) / time_without) * 100
                            speedup = time_without / time_with if time_with > 0 else float('inf')
                            
                            print(f"  Consulta {i}: {time_without:.1f}ms → {time_with:.1f}ms "
                                  f"({improvement:.1f}% mejora, {speedup:.1f}x)")


def main():
    """Función principal"""
    print("🎯 SCRIPT DE PRUEBAS MULTI-ESCALA - Fredys Food Database")
    print("🔬 Análisis completo de rendimiento en 4 escalas de datos")
    print("-" * 70)
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("""
Uso: python multi_scale_test.py [opciones]

Este script ejecuta automáticamente pruebas de rendimiento en 4 escalas:
  • 1,000 registros (1K)
  • 10,000 registros (10K) 
  • 100,000 registros (100K)
  • 1,000,000 registros (1M)

Para cada escala:
  1. Recrea el esquema de base de datos
  2. Genera los datos correspondientes
  3. Ejecuta mediciones sin índices
  4. Crea índices optimizados
  5. Ejecuta mediciones con índices
  6. Genera reportes individuales

Al final:
  • Genera reporte comparativo multi-escala
  • Crea tablas LaTeX para el documento
  • Muestra análisis de tendencias de rendimiento

Opciones:
  -h, --help     Mostrar esta ayuda

Requisitos:
  • PostgreSQL ejecutándose (puerto 5433)
  • Usuario postgres con contraseña password123
  • Suficiente espacio en disco (~2GB para 1M registros)
  • Tiempo disponible (2-3 horas para todas las escalas)

ADVERTENCIA: Este proceso tomará varias horas y regenerará 
             todos los datos en cada escala.
            """)
            return
    
    tester = MultiScalePerformanceTester()
    
    try:
        tester.run_full_multi_scale_test()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
        print("📁 Los resultados parciales se han guardado")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
