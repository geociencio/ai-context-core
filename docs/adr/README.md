# Architecture Decision Records (ADR)

Este directorio contiene los registros de decisiones arquitectónicas (ADR) para `ai-context-core`.

## ¿Qué es un ADR?

Un Architecture Decision Record (ADR) es un documento que captura una decisión arquitectónica importante junto con su contexto y consecuencias.

## Formato

Seguimos el formato [MADR](https://adr.github.io/madr/) (Markdown Architecture Decision Records) con la siguiente estructura:

- **Título**: Breve descripción de la decisión
- **Estado**: Propuesto | Aceptado | Rechazado | Deprecado | Reemplazado
- **Contexto**: Situación que motivó la decisión
- **Decisión**: La decisión tomada
- **Consecuencias**: Impactos positivos y negativos

## Convención de Nombres

Los ADRs se numeran secuencialmente:

```
NNNN-titulo-descriptivo.md
```

Ejemplos:
- `0001-use-markdown-for-adr.md`
- `0002-implement-pattern-detection.md`
- `0003-adopt-multi-framework-support.md`

## ADRs Existentes

| # | Título | Estado | Fecha |
|:--|:-------|:-------|:------|
| [0001](0001-use-adr-for-architecture-decisions.md) | Usar ADR para Decisiones Arquitectónicas | Aceptado | 2026-01-25 |
| [0002](0002-implement-13-improvements-roadmap.md) | Implementar Roadmap de 13 Mejoras | Aceptado | 2026-01-25 |

## Crear un Nuevo ADR

1. Copia el template: `cp template.md NNNN-titulo.md`
2. Incrementa el número secuencial
3. Completa todas las secciones
4. Actualiza este README con el nuevo ADR
5. Commitea el ADR junto con los cambios relacionados

## Template

Ver [template.md](template.md) para el formato estándar.

## Referencias

- [ADR GitHub Organization](https://adr.github.io/)
- [MADR Template](https://adr.github.io/madr/)
- [When to write an ADR](https://github.com/joelparkerhenderson/architecture-decision-record#when-to-write-an-adr)

## Cuándo Crear un ADR

Crea un ADR cuando:

- ✅ Eliges una tecnología o framework importante
- ✅ Cambias la estructura del proyecto significativamente
- ✅ Adoptas un nuevo patrón de diseño
- ✅ Modificas la API pública
- ✅ Tomas decisiones que afectan el rendimiento o escalabilidad
- ✅ Implementas cambios que requieren migración

No es necesario para:

- ❌ Cambios menores de implementación
- ❌ Refactorings internos sin impacto arquitectónico
- ❌ Correcciones de bugs
- ❌ Actualizaciones de documentación
