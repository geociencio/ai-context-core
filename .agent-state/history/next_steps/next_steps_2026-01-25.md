# Next Steps: AI Context Core

## 🚀 Immediate Priorities (Next Session)

- [ ] **Fase 5: Security Hardening**
  - Implementar escaneo de secretos con `trufflehog` o similar.
  - Reforzar detección de inyecciones SQL en `issues.py`.
- [ ] **Fase 6: Performance Profiling**
  - Analizar cuellos de botella reales con `cProfile`.
  - Optimizar `git_analysis.py` para repositorios gigantes.

## 🐛 Known Issues / Technical Debt

- La cobertura de `context/manager.py` es baja (34%). Necesita tests dedicados.
- `git_analysis.py` falla silenciosamente si no hay repo git (manejado, pero podría ser más explícito).

## 💡 Future Ideas

- **Integración con LLMs**: Usar la API de Gemini para generar resúmenes semánticos en lugar de solo contar líneas.
- **Plugin de VS Code**: Exponer el análisis directamente en el editor.

## 🔄 Resume Command

Para retomar el trabajo en la siguiente sesión:

```bash
/inicia-sesion
```
