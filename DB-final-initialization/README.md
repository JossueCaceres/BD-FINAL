# 🔬 Fredys Food Database - Motor de Medición Experimental

## Sistema de Análisis de Rendimiento PostgreSQL - Resultados REALES

Este directorio contiene la implementación completa del sistema de medición de rendimiento para el análisis experimental de consultas SQL con y sin índices. **SISTEMA VALIDADO Y FUNCIONAL**.

---

## 🚀 EJECUCIÓN INMEDIATA

### Para Desarrollo/Pruebas (Ya completado ✅)
```bash
python main.py 10000
python measure_performance.py
```

### Para Análisis Completo Multi-Escala ⚡
```bash
# EJECUTAR EN COMPUTADORA POTENTE (2-3 horas)
python multi_scale_test.py
```

---

## � RESULTADOS ACTUALES VALIDADOS

### ✅ Escala 10K Registros (COMPLETADO)

| Consulta | Sin Índices | Con Índices | Mejora | Factor |
|----------|-------------|-------------|---------|---------|
| **Consulta 1** | 83.5 ms | 9.8 ms | **88.2%** | **8.5x** |
| **Consulta 2** | 159.9 ms | 113.0 ms | **29.3%** | **1.4x** |
| **Consulta 3** | 133.0 ms | 108.6 ms | **18.4%** | **1.2x** |
| **Consulta 4** | 17.7 ms | 6.6 ms | **62.7%** | **2.7x** |

**Archivos generados:**
- ✅ `performance_results_10K.json`
- ✅ `performance_tables_10K.tex`

---

## 🎯 PRÓXIMA EJECUCIÓN CRÍTICA

### Script Multi-Escala: `python multi_scale_test.py`

**Genera automáticamente:**
1. **1K registros** → Datos + tablas LaTeX
2. **10K registros** → Datos + tablas LaTeX  
3. **100K registros** → Datos + tablas LaTeX
4. **1M registros** → Datos + tablas LaTeX
5. **Reporte comparativo** → Análisis multi-escala completo

### ⚠️ IMPORTANCIA CRÍTICA

**¿Por qué es ESENCIAL ejecutar el análisis completo?**

1. **Validación científica** - Reproducibilidad estadística
2. **Comportamiento no-lineal** - Los índices cambian dramáticamente por escala
3. **Requisitos académicos** - Datos experimentales REALES vs simulados
4. **Diferenciación del proyecto** - Análisis profundo vs básico

### Impacto Esperado por Escala

```
1K    → Overhead de índices, mejoras moderadas
10K   → Balance óptimo, mejoras significativas ✅ COMPLETADO  
100K  → Diferencias dramáticas, crítico para JOINs
1M    → Imposible sin índices, mejoras de 100x+
```

- ✅ Medición controlada de tiempos con y sin índices
- ✅ 10 ejecuciones por consulta para promedios estadísticamente válidos  
- ✅ Limpieza de caché entre ejecuciones (VACUUM FULL)
- ✅ Configuración controlada de PostgreSQL
- ✅ Generación automática de tablas LaTeX para el documento

---

### � Instalación y Configuración

#### Opción 1: Configuración Automática (Recomendada)
```bash
# Clonar el repositorio
git clone https://github.com/jossalgon/BD-final-initialization
cd BD-final-initialization

# Ejecutar configuración automática
./setup_performance_test.sh
```

#### Opción 2: Configuración Manual
```bash
# 1. Instalar dependencias
pip3 install -r requirements.txt

# 2. Crear base de datos PostgreSQL
psql -U postgres -c "CREATE DATABASE final_project;"

# 3. Crear esquema
psql -U postgres -d final_project -f create_schema.sql

# 4. Generar datos de prueba
python3 main.py 10000  # Para 10K registros
```

---

### ⚙️ Configuración de Credenciales

Edite las credenciales de PostgreSQL en los archivos según su configuración:

**main.py** y **measure_performance.py**:
```python
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="final_project", 
        user="postgres",
        password="password123"  # ← Cambie aquí
    )
```

---

### � Uso del Sistema de Medición

#### 1. Generar Datos de Prueba

```bash
# Escalas recomendadas para diferentes tipos de prueba
python3 main.py 1000     # 1K - Pruebas rápidas
python3 main.py 10000    # 10K - Pruebas estándar  
python3 main.py 100000   # 100K - Pruebas completas
python3 main.py 1000000  # 1M - Escala empresarial
```

#### 2. Ejecutar Medición de Rendimiento

```bash
# Ejecutar test completo (SIN índices → CON índices)
python3 measure_performance.py

# Opciones adicionales
python3 measure_performance.py --check-data    # Solo verificar datos
python3 measure_performance.py --create-indexes # Solo crear índices
python3 measure_performance.py --drop-indexes   # Solo eliminar índices
python3 measure_performance.py --help          # Mostrar ayuda
```

#### 3. Resultados Generados

El script genera automáticamente:

- `performance_results_[escala].json` - Datos completos de medición
- `performance_tables_[escala].tex` - Tablas LaTeX para el documento

---

### 🔬 Metodología Implementada

El script `measure_performance.py` implementa exactamente la metodología descrita en el documento académico:

#### Configuración Controlada de PostgreSQL
```sql
SET enable_mergejoin = OFF;
SET enable_hashjoin = OFF; 
SET enable_bitmapscan = OFF;
SET enable_sort = OFF;
SET random_page_cost = 4.0;
SET effective_cache_size = '1GB';
```

#### Protocolo de Medición
1. **Preparación**: VACUUM FULL para limpiar caché
2. **Medición**: EXPLAIN ANALYZE para tiempos reales
3. **Repeticiones**: 10 ejecuciones + 1 warm-up (descartada)
4. **Aislamiento**: Limpieza entre ejecuciones
5. **Documentación**: Registro de estadísticas completas

#### Consultas Experimentales
Las 4 consultas del documento están implementadas exactamente:
1. Platos populares con información del administrador
2. Rendimiento de entregas por zona 
3. Repartidores con mejor desempeño
4. Clientes más activos y patrones de consumo

#### Índices Optimizados
Los índices corresponden exactamente a los del documento corregido:
- Índices simples en columnas clave
- Índices compuestos para JOINs
- Sin complejidad innecesaria (sin INCLUDE, WHERE complejos)

---

### 📈 Interpretación de Resultados

#### Archivo JSON (Datos Completos)
```json
{
  "timestamp": "2025-07-02T...",
  "data_scale": "10K", 
  "total_records": 45234,
  "without_indexes": {
    "consulta_1": {
      "average": 156.8,
      "std_dev": 12.3,
      "times": [...]
    }
  },
  "with_indexes": { ... }
}
```

#### Archivo LaTeX (Para Documento)
```latex
\begin{table}[h!]
\centering
\begin{tabular}{|l|c|}
\hline
\textbf{Consulta} & \textbf{10K (ms)} \\
\hline
Consulta 1 & 156.8 \\
...
```

#### Métricas Calculadas
- **Tiempo promedio**: Media de 10 ejecuciones
- **Desviación estándar**: Consistencia de mediciones
- **Porcentaje de mejora**: ((Sin índices - Con índices) / Sin índices) × 100
- **Factor de aceleración**: Tiempo sin índices / Tiempo con índices

---

### 🔍 Factores que Pueden Afectar los Resultados

#### ✅ Factores Controlados por el Script
- **Caché de PostgreSQL**: VACUUM FULL entre ejecuciones
- **Configuración del motor**: Parámetros controlados
- **Warm-up**: Primera ejecución descartada
- **Estadísticas**: ANALYZE actualizado
- **Repeticiones**: 10 mediciones para promedio válido

#### ⚠️ Factores Externos a Considerar
- **Hardware**: CPU, RAM, SSD vs HDD
- **Sistema operativo**: Otros procesos ejecutándose
- **Versión PostgreSQL**: Diferentes optimizadores
- **Volumen de datos**: Más datos = diferencias más marcadas
- **Red**: Solo aplica si PostgreSQL es remoto

#### 🎯 Recomendaciones para Resultados Consistentes
1. **Cerrar aplicaciones innecesarias** durante la medición
2. **Usar escalas de datos >= 10K** para diferencias significativas
3. **Ejecutar múltiples veces** el test completo
4. **Documentar especificaciones** del hardware usado

---

### � Casos de Uso

#### Para el Documento Académico
```bash
# Generar datos según volumen deseado
python3 main.py 100000

# Ejecutar medición
python3 measure_performance.py

# Copiar tablas LaTeX generadas al documento
```

#### Para Análisis Detallado
```bash
# Analizar resultados JSON para insights adicionales
import json
with open('performance_results_100K.json') as f:
    data = json.load(f)
    
# Extraer métricas específicas
for query, metrics in data['without_indexes'].items():
    print(f"{query}: {metrics['average']:.1f}ms ±{metrics['std_dev']:.1f}")
```

---

### 🐛 Solución de Problemas

#### Error de Conexión a PostgreSQL
```bash
# Verificar que PostgreSQL esté ejecutándose
sudo service postgresql status

# Verificar credenciales
psql -U postgres -d final_project -c "SELECT 1;"
```

#### Error "Base de datos no existe"
```bash
# Crear base de datos
psql -U postgres -c "CREATE DATABASE final_project;"
```

#### Error "Tabla no existe"
```bash
# Crear esquema
psql -U postgres -d final_project -f create_schema.sql
```

#### Sin datos para medir
```bash
# Generar datos
python3 main.py 10000
```

---

### 📚 Archivos Técnicos

#### create_schema.sql
- Definición completa DDL del esquema
- Relaciones y constrains correctos
- Índices básicos del sistema

#### measure_performance.py  
- Clase `DatabasePerformanceTester`
- Implementación de metodología experimental
- Generación automática de reportes

#### main.py
- Generador de datos realistas con Faker
- Distribución proporcional de registros
- Datos coherentes entre tablas relacionadas

---

### 🎉 Contribuciones

Este proyecto implementa las especificaciones exactas del documento académico "Optimización de Consultas en PostgreSQL para Sistema de Delivery - Fredys Food".

**Autores**: Proyecto BD Final  
**Universidad**: Universidad de Ingeniería y Tecnología (UTEC)  
**Curso**: Base de Datos  
**Fecha**: Julio 2025

---

### 📞 Soporte

Para preguntas sobre el uso del sistema:

1. **Verificar configuración**: `./setup_performance_test.sh`
2. **Revisar logs**: Los errores se muestran en consola
3. **Validar datos**: `python3 measure_performance.py --check-data`
4. **Ayuda integrada**: `python3 measure_performance.py --help`

Ejemplo:

```bash
python main.py 1000
```

Esto:

- Generará 1 000 usuarios.
- Creará clientes y trabajadores a partir de la mitad de esos usuarios.
- Tendrás 250 repartidores y 125 administradores.
- Sembrará 1 000 menús y 1 000 platos.
- Insertará 1 000 pedidos y sus relaciones.

---

### 🔧 Personalización

- **Proveedores de datos**: Faker y faker-food ofrecen muchos métodos. Puedes cambiar:
  - `fake.dish()` por otros sabores o ingredientes.
  - `fake.company()`, `fake.address()`, etc.
- **Proporciones**: Ajusta en `main.py` el número de repartidores (`n//4`), administradores (`n//8`) o relaciones.
- **Tablas adicionales**: Añade funciones nuevas siguiendo el patrón.

---

### 📖 Estructura del proyecto

```
├── main.py
└── README.md
```

---

### ❓ Preguntas

Si encuentras errores o tienes sugerencias, abre un *issue* o contáctame por correo.

