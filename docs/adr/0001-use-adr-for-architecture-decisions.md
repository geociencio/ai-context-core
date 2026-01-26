# 0001. Usar ADR para Decisiones Arquitectónicas

**Estado**: Aceptado

**Fecha**: 2026-01-25

**Autores**: Equipo ai-context-core

**Decisores**: Equipo de desarrollo

---

## Contexto y Problema

A medida que `ai-context-core` crece y evoluciona, necesitamos una forma sistemática de documentar decisiones arquitectónicas importantes. Sin un registro formal:

- Las razones detrás de decisiones pasadas se pierden con el tiempo
- Nuevos contribuidores no entienden por qué se tomaron ciertas decisiones
- Es difícil evaluar si una decisión antigua sigue siendo válida
- No hay un proceso claro para proponer y discutir cambios arquitectónicos

## Factores de Decisión

- **Mantenibilidad**: Facilidad para mantener la documentación actualizada
- **Accesibilidad**: Fácil de encontrar y leer para todos los miembros del equipo
- **Versionado**: Debe estar bajo control de versiones junto con el código
- **Simplicidad**: No debe agregar overhead significativo al proceso de desarrollo
- **Estándar**: Preferiblemente seguir un estándar reconocido en la industria

## Opciones Consideradas

### Opción 1: No documentar decisiones formalmente

**Descripción**: Continuar sin un sistema formal, documentando decisiones ad-hoc en commits, issues o comentarios de código.

**Pros**:
- ✅ Sin overhead adicional
- ✅ Sin proceso nuevo que aprender

**Contras**:
- ❌ Conocimiento disperso y difícil de encontrar
- ❌ Decisiones no documentadas se olvidan
- ❌ Dificulta onboarding de nuevos contribuidores
- ❌ No hay proceso para revisar decisiones pasadas

### Opción 2: Wiki o documentación externa

**Descripción**: Usar una wiki (GitHub Wiki, Confluence, etc.) para documentar decisiones.

**Pros**:
- ✅ Interfaz web amigable
- ✅ Fácil de editar
- ✅ Búsqueda integrada

**Contras**:
- ❌ No versionado junto con el código
- ❌ Puede quedar desactualizado
- ❌ Requiere acceso separado
- ❌ No se revisa en pull requests

### Opción 3: Architecture Decision Records (ADR) en Markdown

**Descripción**: Usar ADRs en formato Markdown dentro del repositorio, siguiendo el estándar MADR.

**Pros**:
- ✅ Versionado junto con el código
- ✅ Revisable en pull requests
- ✅ Formato simple (Markdown)
- ✅ Estándar de industria reconocido
- ✅ Fácil de buscar con grep/find
- ✅ No requiere herramientas externas

**Contras**:
- ❌ Requiere disciplina para mantener actualizado
- ❌ Proceso adicional en el workflow

## Decisión

**Opción elegida**: Architecture Decision Records (ADR) en Markdown

**Justificación**: 

Los ADRs proporcionan el mejor balance entre formalidad y simplicidad. Al estar en el repositorio:
- Se versionan junto con el código que implementa las decisiones
- Se revisan en pull requests, asegurando calidad
- Son accesibles para cualquiera con acceso al repo
- No requieren herramientas adicionales

El formato MADR es ampliamente adoptado y proporciona una estructura clara sin ser excesivamente prescriptivo.

## Consecuencias

### Positivas

- ✅ **Transparencia**: Todas las decisiones arquitectónicas están documentadas y accesibles
- ✅ **Contexto histórico**: Podemos entender por qué se tomaron decisiones en el pasado
- ✅ **Mejor onboarding**: Nuevos contribuidores pueden entender la arquitectura rápidamente
- ✅ **Revisión de decisiones**: Podemos evaluar si decisiones antiguas siguen siendo válidas
- ✅ **Proceso de propuesta**: Proponer cambios arquitectónicos tiene un proceso claro

### Negativas

- ❌ **Overhead inicial**: Requiere tiempo para crear ADRs
- ❌ **Disciplina requerida**: El equipo debe recordar crear ADRs para decisiones importantes

### Neutrales

- ℹ️ **Curva de aprendizaje**: El equipo necesita aprender el formato ADR (mínima)
- ℹ️ **Mantenimiento**: Los ADRs necesitan actualizarse si las decisiones cambian

## Implementación

- [x] Crear directorio `docs/adr/`
- [x] Crear `README.md` explicando el proceso
- [x] Crear `template.md` con formato estándar
- [x] Crear este ADR como ejemplo
- [ ] Agregar ADRs para decisiones arquitectónicas existentes
- [ ] Incluir creación de ADRs en el workflow de desarrollo

## Validación

- **Métrica 1**: Número de ADRs creados en los próximos 3 meses (objetivo: >5)
- **Métrica 2**: Feedback del equipo sobre utilidad de ADRs
- **Métrica 3**: Referencias a ADRs en pull requests y discusiones

## Referencias

- [ADR GitHub Organization](https://adr.github.io/)
- [MADR Template](https://adr.github.io/madr/)
- [Documenting Architecture Decisions - Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [When to write an ADR](https://github.com/joelparkerhenderson/architecture-decision-record)

## Notas

Este ADR establece el proceso para futuros ADRs. Decisiones arquitectónicas importantes tomadas antes de este ADR deberían documentarse retroactivamente cuando sea relevante.
