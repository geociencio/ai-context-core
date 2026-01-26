# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-25 21:48:00
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 14
- **Lines of Code**: 4,183
- **Total Size**: 1.1 MB
- **Average Complexity**: 39.1
- **Docstring Coverage**: 97.0%
- **Quality Score**: 67.5/100
- **Test Files**: 11

## 📁 STRUCTURE
- **Python Files**: 35
- **Total Files**: 135
- **Primary File Types**: .py, .pyc, .md, .txt, .sample

## 🚨 CRITICAL ISSUES

### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 3 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/fs_utils.py**: 5 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/engine.py**: 4 issues (Max: MEDIUM)

### 🏗️ Critical Technical Debt:
- **.agent/scripts/skill_sync.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/dependencies.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/issues.py**: 2 issues (Score: 5)


## 💡 MAIN RECOMMENDATIONS

### .agent/scripts/skill_sync.py
- Very long functions (average 70.5 lines/function).

### src/ai_context_core/analyzer/metrics.py
- Very long functions (average 73.3 lines/function).

### src/ai_context_core/analyzer/dependencies.py
- High complexity (52) with several functions. Consider breaking down large logic.

## 🏗️ DESIGN PATTERNS

### Factory
- **AIContextManager** in `src/ai_context_core/context/manager.py` (Confidence: 70%)

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 1 modules (7.1%)
- medium (6-15): 1 modules (7.1%)
- high (16-30): 5 modules (35.7%)
- very_high (31+): 7 modules (50.0%)