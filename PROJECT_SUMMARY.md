# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-25 21:19:16
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 13
- **Lines of Code**: 3,585
- **Total Size**: 1.0 MB
- **Average Complexity**: 30.5
- **Docstring Coverage**: 96.7%
- **Quality Score**: 67.3/100
- **Test Files**: 9

## 📁 STRUCTURE
- **Python Files**: 32
- **Total Files**: 128
- **Primary File Types**: .py, .pyc, .md, .txt, .sample

## 🚨 CRITICAL ISSUES

### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 3 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/engine.py**: 4 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/fs_utils.py**: 5 issues (Max: MEDIUM)

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
- High complexity (44) with several functions. Consider breaking down large logic.

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 1 modules (7.7%)
- medium (6-15): 1 modules (7.7%)
- high (16-30): 6 modules (46.2%)
- very_high (31+): 5 modules (38.5%)