# Guía de Configuración

`ai-context-core` permite una configuración flexible mediante archivos TOML, siguiendo una política de "Zero External Dependencies" para la carga de configuración.

## Jerarquía de Configuración

La herramienta carga la configuración en el siguiente orden de prioridad (de menor a mayor):

1.  **Defaults del Sistema**: Valores por defecto compilados en `src/ai_context_core/config/defaults.toml`.
2.  **Configuración del Proyecto**: Archivo `.ai-context/config.toml` en la raíz de tu proyecto.
3.  **Configuración de Perfil**: Archivos `.yaml` en `.ai-context/config.yaml` (Legacy/Transición).

> [!TIP]
> Se recomienda usar `.ai-context/config.toml` para todas las nuevas configuraciones.

## Opciones Disponibles

### 1. Umbrales de Calidad (`quality_thresholds`)

Definen los límites para considerar métricas como advertencias o errores.

```toml
[quality_thresholds.complexity]
warning = 10  # Alerta si complejidad ciclomática > 10
error = 15    # Falla si complejidad > 15

[quality_thresholds.maintainability]
warning = 65  # Alerta si MI < 65
error = 50    # Falla si MI < 50

[quality_thresholds.lines]
warning = 400 # Alerta si archivo > 400 líneas
error = 800   # Falla si archivo > 800 líneas
```

### 2. Pesos de Puntuación (`quality_weights`)

Determinan cómo se calcula el "Quality Score" final (0-100). La suma debe ser 1.0 (aprox).

```toml
[quality_weights]
complexity = 0.25       # 25% Complejidad Ciclomática
maintainability = 0.20  # 20% Índice de Mantenibilidad
test_coverage = 0.15    # 15% Cobertura de Tests
documentation = 0.15    # 15% Calidad de Docstrings
security = 0.25         # 25% Ausencia de Vuln. de Seguridad
```

### 3. Patrones de Seguridad (`security_patterns`)

Define qué funciones y módulos son considerados peligrosos por el escáner AST.

```toml
[security_patterns]
# Funciones que ejecutan código dinámico o comandos del sistema
dangerous_functions = ["exec", "eval", "__import__", "input"]

# Módulos conocidos por deserialización insegura o protocolos vulnerables
dangerous_modules = ["pickle", "marshal", "telnetlib"]

# Patrones de string que sugieren SQL Injection
sql_injection_indicators = ["execute(", "executemany("]
```

### 4. Configuración de Análisis (`analysis`)

Parámetros técnicos del motor de análisis.

```toml
[analysis]
parallel_workers = "auto"  # "auto" usa CPU count * 2, o un entero específico
cache_enabled = true       # Usa caché incremental en .ai-context/cache
max_file_size_mb = 10      # Ignora archivos mayores a este tamaño
```

## Ejemplo de Personalización

Crea un archivo `.ai-context/config.toml` para hacer el análisis más estricto:

```toml
# .ai-context/config.toml

[quality_thresholds.complexity]
warning = 5  # Demasiado estricto, alerta con cualquier lógica compleja
error = 10

[quality_weights]
# Priorizar seguridad sobre todo lo demás
security = 0.50
complexity = 0.20
maintainability = 0.10
documentation = 0.10
test_coverage = 0.10

[analysis]
parallel_workers = 4
```
