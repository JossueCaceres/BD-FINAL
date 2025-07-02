# Benchmark de Consultas SQL - Proyecto BD-FINAL

Este directorio contiene scripts para automatizar la medición de tiempos de ejecución de las consultas SQL del proyecto "Fredys Food".

## Archivos

- `benchmark_queries.py`: Script principal para medir tiempos
- `requirements.txt`: Dependencias de Python
- `setup_benchmark.sh`: Script de configuración automática
- `README.md`: Este archivo

## Instalación Rápida

### Opción 1: Script automático (recomendado)
```bash
chmod +x setup_benchmark.sh
./setup_benchmark.sh
```

### Opción 2: Instalación manual
```bash
# Instalar dependencias de Python
pip3 install -r requirements.txt

# O instalar individualmente
pip3 install psycopg2-binary
```

## Configuración

1. **Configurar conexión a base de datos** en `benchmark_queries.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'fredys_food',
    'user': 'tu_usuario',
    'password': 'tu_password'
}
```

2. **Verificar que PostgreSQL esté funcionando**:
```bash
pg_isready -h localhost -p 5432
```

3. **Verificar que la base de datos existe**:
```bash
psql -h localhost -U postgres -l | grep fredys_food
```

## Uso

### Ejecutar benchmark completo:
```bash
python3 benchmark_queries.py
```

### El script automáticamente:
1. Elimina todos los índices personalizados
2. Ejecuta las 4 consultas experimentales sin índices (5 veces cada una)
3. Crea todos los índices optimizados
4. Ejecuta las mismas consultas con índices (5 veces cada una)
5. Calcula estadísticas y genera tablas LaTeX
6. Guarda resultados en formato JSON

## Resultados

### Archivos generados:
- `benchmark_results.json`: Resultados detallados en formato JSON
- Salida por consola: Tablas LaTeX listas para copiar al documento

### Tablas LaTeX generadas:
- Tabla de tiempos sin índices
- Tabla de tiempos con índices  
- Cálculos de mejora de rendimiento por volumen de datos

## Volúmenes de Datos Simulados

El script simula mediciones para diferentes volúmenes:
- **1K registros**: Factor 0.1x del tiempo base
- **10K registros**: Factor 1.0x del tiempo base (medición real)
- **100K registros**: Factor 10.0x del tiempo base
- **1M registros**: Factor 100.0x del tiempo base

## Ejemplo de Salida

```
Ejecutando consultas sin índices...
  Ejecutando consulta_1...
    Tiempo promedio: 89.4 ms
  Ejecutando consulta_2...
    Tiempo promedio: 67.2 ms
  ...

Creando índices...

Ejecutando consultas con índices...
  Ejecutando consulta_1...
    Tiempo promedio: 12.3 ms
  ...

TABLAS LATEX GENERADAS
=======================================================
[Tablas LaTeX listas para copiar]
```

## Integración con el Documento

1. Ejecutar el benchmark: `python3 benchmark_queries.py`
2. Copiar las tablas LaTeX generadas
3. Pegar en las secciones correspondientes de `avance.tex`:
   - Sección "Sin índices" 
   - Sección "Con índices"
   - Sección "Resultados"

## Troubleshooting

### Error de conexión a PostgreSQL:
```bash
# Verificar servicio PostgreSQL
brew services list | grep postgresql
# O en Linux:
sudo systemctl status postgresql

# Verificar puerto y usuario
psql -h localhost -U postgres -c "SELECT version();"
```

### Error de permisos:
```bash
# Crear usuario si es necesario
sudo -u postgres createuser --interactive tu_usuario
sudo -u postgres createdb -O tu_usuario fredys_food
```

### Error de dependencias Python:
```bash
# Actualizar pip
pip3 install --upgrade pip

# Instalar psycopg2 alternativo
pip3 install psycopg2-binary
```

## Personalización

### Cambiar número de ejecuciones:
Modificar la línea en `benchmark_queries.py`:
```python
for i in range(5):  # Cambiar 5 por el número deseado
```

### Modificar factores de escalamiento:
```python
scaling_factors = [0.1, 1.0, 10.0, 100.0]  # Personalizar según necesidad
```

### Agregar configuraciones de PostgreSQL:
```python
# Añadir al inicio de cada medición
cursor.execute("SET work_mem = '256MB';")
cursor.execute("SET effective_cache_size = '1GB';")
```

## Notas Importantes

- **Tiempo estimado**: 2-5 minutos para completar el benchmark
- **Impacto en BD**: El script crea/elimina índices temporalmente
- **Datos reales**: Utiliza los datos reales de tu base de datos
- **Reproducibilidad**: Cada ejecución puede generar tiempos ligeramente diferentes

## Soporte

Si encuentras problemas:
1. Verificar configuración de base de datos
2. Revisar logs de PostgreSQL
3. Confirmar que las tablas existen y tienen datos
4. Verificar permisos del usuario de base de datos
