# 0003. Detección de Patrones mediante Puntuación Bayesiana de Evidencias

**Estado**: Aceptado

**Fecha**: 2026-01-25

**Autores**: Equipo ai-context-core

**Decisores**: Equipo de desarrollo

---

## Contexto y Problema

La detección de patrones de diseño mediante análisis estático de código (AST) es inherentemente ambigua. Un Singleton puede implementarse mediante `__new__`, un decorador de clase, un metaclass o simplemente una convención de nomenclatura. Forzar una detección binaria (Sí/No) genera falsos positivos o negativos que reducen la utilidad del contexto para las IAs.

## Factores de Decisión

- **Confianza**: Necesitamos comunicar qué tan seguros estamos de un patrón detectado.
- **Flexibilidad**: La detección debe permitir múltiples formas de implementar el mismo patrón.
- **Accionabilidad**: El reporte debe incluir *por qué* se detectó el patrón (evidencias).

## Opciones Consideradas

### Opción 1: Análisis Binario Basado en Reglas Estrictas
**Descripción**: Detectar solo implementaciones estándar (ej: herencia de una clase `Singleton`).
- **Pros**: Muy preciso para casos estándar.
- **Contras**: Falla en implementaciones "Pythonic" o personalizadas.

### Opción 2: Puntuación Heurística Acumulativa (Elegida)
**Descripción**: Cada patrón tiene una lista de "evidencias" (ej: nombre de clase, métodos específicos, uso de decoradores) con pesos asignados. El score final determina la confianza reportada.
- **Pros**: Robusto ante variaciones, permite reportar confianza gradual (50-100%), facilita la depuración mediante la lista de evidencias.
- **Contras**: Requiere calibración manual de los pesos de cada evidencia.

## Decisión

Adoptar un sistema de scoring acumulativo donde:
1. Las evidencias estructurales fuertes (ej: `__new__`) tienen pesos altos (60+).
2. Las convenciones de nombres tienen pesos medios (30-40).
3. Se requiere un umbral mínimo (normalmente 50-60%) para reportar el patrón.

## Consecuencias

### Positivas
- ✅ **Contexto Enriquecido**: Las IAs ven no solo el patrón, sino la evidencia técnica.
- ✅ **Menos Ruido**: Se filtran detecciones accidentales por nombre que no tienen estructura de soporte.
- ✅ **Extensibilidad**: Fácil añadir nuevas evidencias a patrones existentes.

### Negativas
- ❌ **Subjetividad**: Los pesos de las evidencias son estimaciones educadas del equipo.
- ❌ **Complejidad de Código**: El módulo `patterns.py` es más complejo que un simple buscador de strings.
