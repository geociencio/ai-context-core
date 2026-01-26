# Optimización del Workflow de Cierre de Sesión

Adaptar el workflow `/cierra-sesion` basándose en las mejores prácticas documentadas en `docs/cierra-sesion-res.md`, ajustándolo a las necesidades específicas del proyecto `ai-context-core`.

## Análisis de Diferencias

### Workflow Actual (`cierra-sesion.md`)
- ✅ Tests básicos
- ✅ Actualización de logs (Development/Maintenance)
- ✅ Regeneración de contexto IA
- ✅ Propuesta de commit
- ❌ **Falta**: Archivado de `next_steps.md`
- ❌ **Falta**: Creación de reportes de sesión
- ❌ **Falta**: Actualización de CHANGELOG
- ❌ **Falta**: Formateo de código con `black`
- ❌ **Falta**: Validación de Agent Actions

### Documento de Referencia (`cierra-sesion-res.md`)
- ✅ Proceso completo y estructurado
- ✅ Archivado histórico de `next_steps.md`
- ✅ Reportes de sesión obligatorios
- ✅ Actualización de múltiples logs
- ✅ Formateo con `black`
- ⚠️ **No aplica**: Docker tests (proyecto usa solo unittest)
- ⚠️ **No aplica**: Referencias a 361 tests (proyecto tiene 7 tests)
- ⚠️ **No aplica**: `docs/plans/implementation_plan_vX.Y.Z.md` (no existe esta estructura)

## Cambios Propuestos

### 1. **Estructura del Workflow Mejorado**

El nuevo workflow incluirá:

1. **Formateo de Código** (nuevo)
   - Ejecutar `uv run black .` antes de tests
   
2. **Verificación de Tests** (mejorado)
   - Mantener comando actual: `uv run python -m unittest discover tests`
   - Validar que los 7 tests pasen

3. **Actualización de Memoria** (expandido)
   - Identificar tema de sesión
   - Actualizar `docs/DEVELOPMENT_LOG.md` (ya existe)
   - Crear reporte de sesión: `docs/sessions/session_YYYY-MM-DD_[TEMA].md`
   - Actualizar `CHANGELOG.md` en sección `[Unreleased]`
   - Crear/actualizar `.agent/next_steps.md` con próximos pasos

4. **Archivado Histórico** (nuevo)
   - Crear directorio `.agent/history/next_steps/` si no existe
   - Copiar `.agent/next_steps.md` → `.agent/history/next_steps/next_steps_YYYY-MM-DD.md`

5. **Sincronización de Contexto** (mejorado)
   - Ejecutar: `uv run python -m ai_context_core.cli analyze`
   - Mostrar contenido de `.agent/next_steps.md`

6. **Commit de Cierre** (mejorado)
   - Formato: `chore(docs): close session [tema_descriptivo]`
   - Usar skill `commit-standards`

7. **Resumen Final** (nuevo)
   - Listar archivos actualizados
   - Estado de tests
   - Contenido de `next_steps.md`
   - Sugerencia para próxima sesión

### 2. **Archivos a Modificar**

#### `.agent/workflows/cierra-sesion.md`
- Expandir de 38 a ~90 líneas
- Agregar Agent Actions y validaciones
- Incluir todos los pasos documentados
- Adaptar comandos al proyecto (sin Docker, usar CLI correcta)

### 3. **Directorios a Crear**

- `.agent/history/next_steps/` - Para archivado histórico

## Verificación

### Tests Automáticos
```bash
# Verificar que el workflow es válido markdown
cat .agent/workflows/cierra-sesion.md

# Verificar que los directorios existen
ls -la .agent/history/next_steps/
```

### Validación Manual
1. Revisar que el workflow incluye todos los pasos críticos
2. Verificar que los comandos son correctos para este proyecto
3. Confirmar que las rutas de archivos son válidas
4. Validar que los Agent Actions están bien definidos

### Prueba de Ejecución (Simulada)
El usuario puede probar el workflow en la próxima sesión ejecutando `/cierra-sesion` y verificando que:
- Se crean todos los archivos esperados
- Los comandos se ejecutan correctamente
- El archivado funciona
- El commit se genera con el formato correcto
