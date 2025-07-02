# Fredys Food Database Performance Analysis

## Análisis de Rendimiento SQL con y sin Índices

Sistema automatizado para medir el rendimiento de consultas SQL en PostgreSQL, comparando tiempos con y sin índices en diferentes escalas de datos (1K, 10K, 100K, 1M registros).

## ¿Qué hace?

- Genera datos sintéticos de un sistema de delivery de comida
- Mide tiempos de 4 consultas SQL complejas con y sin índices
- Ejecuta pruebas en múltiples escalas (1K a 1M registros)
- Genera reportes automáticos en JSON y LaTeX

## Requisitos

- PostgreSQL 14+ (puerto 5433, password: password123)
- Python 3.8+
- 4GB RAM (para escalas grandes)

## Instalación Rápida

```bash
git clone https://github.com/JossueCaceres/BD-FINAL.git
cd BD-FINAL/DB-final-initialization
pip install -r requirements.txt
python verify_system.py
```

## Configuración PostgreSQL

```bash
# Usuario: postgres
# Password: password123  
# Puerto: 5433
# Database: final_project
```

## Cómo Ejecutar

### Prueba Rápida (20 minutos)
```bash
python test_multi_scale.py  # Solo 1K y 10K registros
```

### Análisis Completo (2-3 horas)
```bash
python multi_scale_test.py  # 1K, 10K, 100K, 1M registros
```

### Escala Específica
```bash
python run_schema.py
python main.py 100000       # Generar 100K registros
python measure_performance.py
```

## Resultados (Ejemplo con 10K registros)

| Consulta | Sin Índices | Con Índices | Mejora |
|----------|-------------|-------------|--------|
| Consulta 1 | 83.5 ms | 9.8 ms | **88.2%** |
| Consulta 2 | 159.9 ms | 113.0 ms | **29.3%** |
| Consulta 3 | 133.0 ms | 108.6 ms | **18.4%** |
| Consulta 4 | 17.7 ms | 6.6 ms | **62.7%** |

## Archivos Generados

- `performance_results_[ESCALA].json` - Datos detallados
- `performance_tables_[ESCALA].tex` - Tablas para LaTeX
- `multi_scale_summary_YYYYMMDD_HHMM.json` - Resumen comparativo

## Para Computadora Potente

```bash
# Configurar PostgreSQL para máximo rendimiento
./setup_performance_test.sh

# Ejecutar análisis completo
python multi_scale_test.py

# Monitorear progreso
tail -f multi_scale_test.log
```

## ¿Por Qué Es Importante Correr Todo?

- **Datos reales vs simulados**: Necesitas resultados experimentales auténticos
- **Escalabilidad**: El comportamiento cambia dramáticamente con más datos
- **Validación académica**: Los resultados deben ser reproducibles
- **Análisis completo**: 1M registros muestra el verdadero impacto de los índices

Los índices pueden ser **hasta 10x más rápidos** en escalas grandes, pero solo lo sabrás ejecutando las pruebas completas.
