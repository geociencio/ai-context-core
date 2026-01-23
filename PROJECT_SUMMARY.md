# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-23 00:42:06
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 12
- **Lines of Code**: 3,075
- **Total Size**: 0.7 MB
- **Average Complexity**: 28.7
- **Docstring Coverage**: 96.5%
- **Quality Score**: 67.5/100
- **Test Files**: 4

## 📁 STRUCTURE
- **Python Files**: 26
- **Total Files**: 89
- **Primary File Types**: .py, .pyc, .md, .txt, .sample

## 🚨 CRITICAL ISSUES

### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 1 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/engine.py**: 1 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/fs_utils.py**: 1 issues (Max: MEDIUM)

### 🏗️ Critical Technical Debt:
- **.agent/scripts/skill_sync.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/dependencies.py**: 3 issues (Score: 5)


## 💡 MAIN RECOMMENDATIONS

### .agent/scripts/skill_sync.py
- Very long functions (average 71.5 lines/function).

### src/ai_context_core/analyzer/metrics.py
- Very long functions (average 67.7 lines/function).

### src/ai_context_core/analyzer/engine.py
- High complexity (18) with several functions. Consider breaking down large logic.

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 1 modules (8.3%)
- medium (6-15): 1 modules (8.3%)
- high (16-30): 5 modules (41.7%)
- very_high (31+): 5 modules (41.7%)