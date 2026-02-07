# Memorias y Lecciones Aprendidas (Agent Semantic Memory)

Este documento registra preferencias del usuario, reglas de diseño implícitas y lecciones aprendidas que no son detectables solo por análisis de código AST.

## Preferencias del Usuario
- **Idioma**: La documentación y comunicación debe ser en **Español**.
- **Commits**: Los mensajes de commit siempre en **Inglés**.
- **Herramientas**: Preferencia por `uv` y `black`.
- **UI**: Desarrollo programático (no `.ui` de Qt Designer por ahora).
- **Estándares**: Respeto total a Conventional Commits.

## Lecciones Técnicas Aprendidas
- **Pathlib**: Nunca usar `os.path` salvo que sea estrictamente necesario para compatibilidad externa (y convertir a `str` inmediatamente).
- **Workflows**: Los workflows de sesión (`inicia-sesion`, `cierra-sesion`) son sagrados para no perder el hilo entre sesiones.
- **Ruta de Artefactos**: Siempre usar rutas absolutas para evitar ambigüedad en el agente.

## Reglas de Arquitectura Implícitas
- El archivo `AI_CONTEXT.md` es generado por la CLI; no debe ser editado manualmente para añadir documentación contextual (usar este archivo o `docs/` en su lugar).
- Cada nueva funcionalidad debe ser verificada en Docker (`make docker-test`) para garantizar consistencia con CI.
