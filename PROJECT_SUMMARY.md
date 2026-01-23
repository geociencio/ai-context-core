# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-22 23:05:16
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 11
- **Lines of Code**: 2,932
- **Total Size**: 0.5 MB
- **Average Complexity**: 29.4
- **Docstring Coverage**: 98.2%
- **Quality Score**: 70.0/100
- **Test Files**: 4

## 📁 STRUCTURE
- **Python Files**: 26
- **Total Files**: 82
- **Primary File Types**: .py, .pyc, .md, .txt, .sample

## 🚨 CRITICAL ISSUES

### 🔒 Security Issues:
- **src/ai_context_core/analyzer/fs_utils.py**: 1 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/engine.py**: 1 issues (Max: MEDIUM)
- **src/ai_context_core/context/manager.py**: 1 issues (Max: MEDIUM)

### 🏗️ Critical Technical Debt:
- **src/ai_context_core/analyzer/dependencies.py**: 3 issues (Score: 5)


## 💡 MAIN RECOMMENDATIONS

### src/ai_context_core/analyzer/metrics.py
- Very long functions (average 67.7 lines/function).

### src/ai_context_core/analyzer/ast_utils.py
- High complexity (51) with several functions. Consider breaking down large logic.

### src/ai_context_core/analyzer/dependencies.py
- High complexity (44) with several functions. Consider breaking down large logic.

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 1 modules (9.1%)
- medium (6-15): 1 modules (9.1%)
- high (16-30): 4 modules (36.4%)
- very_high (31+): 5 modules (45.5%)