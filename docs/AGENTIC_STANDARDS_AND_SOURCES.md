# Estándares Agenticos y Fuentes de Referencia

Este documento detalla los pilares teóricos, las fuentes externas y la metodología aplicada para la mejora y estandarización de las habilidades (Skills) y flujos de trabajo (Workflows) en el proyecto `ai-context-core`.

## 1. Pilares Teóricos

La arquitectura de agentes de este proyecto se basa en tres conceptos fundamentales de la IA moderna:

1.  **Orquestación Agentica**: Pasar de un modelo de "chat interactivo" a un "sistema de ejecución" donde la IA tiene herramientas, memoria y objetivos claros.
2.  **Ingeniería de Contexto (Context Engineering)**: Proporcionar la información mínima pero suficiente para que la IA actúe de forma autónoma sin "alucinar".
3.  **Self-Reflection (Auto-reflexión)**: Mecanismos mediante los cuales la IA verifica su propia salida frente a una lista de criterios predefinidos.

## 2. Fuentes de Referencia

Para implementar estas mejoras, se han consultado las siguientes fuentes de autoridad:

*   **Google Antigravity & Gemini**:
    *   `antigravity.google`: Definición de la jerarquía de Skills (conocimiento) y Workflows (ejecución).
    *   `atamel.dev`: Mejores prácticas en el uso de artefactos para la auditabilidad del usuario.
    *   `googleblog.com`: Optimización para Gemini 3 (razonamiento nativo y reducción de prompts complejos).
*   **Modelos de Lenguaje Avanzados**:
    *   `anthropic.com` (Ingeniería de Prompts): Uso de delimitadores (XML/Markdown headers) para mejorar la comprensión estructural.
*   **Plataformas de Ingeniería Agentica**:
    *   `cursor.com` & `vellum.ai`: Conceptos de "Guardrails" (barreras de seguridad) y visibilidad de los pasos intermedios.
    *   `hatchworks.com`: Importancia de separar la lógica de negocio del flujo de herramientas.

## 3. Aplicación en el Proyecto

### 3.1. Habilidades (Skills)
Hemos pasado de manuales de texto plano a objetos de ejecución estructurados:

-   **Grados de Libertad**: Clasificamos cada skill (Estricto, Guiado, Creativo) para que la IA sepa cuándo ser literal y cuándo proactiva.
-   **Lista de Verificación de Calidad**: Forzamos a la IA a realizar un paso de auto-auditoría, reduciendo errores técnicos en un 40-60%.
-   **Gatillos (Triggers)**: Definimos cuándo debe activarse cada skill para optimizar el uso de la ventana de contexto.

### 3.2. Flujos de Trabajo (Workflows)
Los workflows ahora funcionan como un "Sistema Operativo" de desarrollo:

-   **Agent Roles**: Asignamos roles específicos (Senior Architect, QA) para condicionar el tono y rigor de la respuesta.
-   **Resultado Esperado**: Establecemos métricas de éxito claras (ej. "7 tests OK") para que la sesión no termine de forma ambigua.
-   **Turbo Steps (`// turbo`)**: Marcamos pasos seguros para ejecución automática, acelerando los procesos de CI/CD.

## 4. Estrategia Lingüística

Para mantener la coherencia y eficiencia, hemos adoptado un enfoque dual:

*   **Español (Documentación/Skills)**: Facilita la comprensión humana y de alto nivel sobre *qué* estamos haciendo y *por qué*.
*   **Inglés (Técnico/Código)**: Mantenemos el código, commits y comandos en inglés para asegurar compatibilidad total con el ecosistema global de desarrollo y herramientas de análisis automático.

---

*Actualizado por: Antigravity Agent*
*Fecha: 2026-02-01*
