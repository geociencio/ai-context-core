# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-25 23:38:37
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 17
- **Lines of Code**: 5,051
- **Total Size**: 0.8 MB
- **Average Complexity**: 38.3
- **Avg Maintenance Index**: 23.3
- **Docstring Coverage**: 95.2%
- **Quality Score**: 67.9/100
- **Test Files**: 15

## 📁 STRUCTURE
- **Python Files**: 32
- **Total Files**: 129
- **Primary File Types**: .md, .py, .yaml, .json, .yml

## 🚨 CRITICAL ISSUES

### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 3 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/reporting.py**: 1 issues (Max: MEDIUM)
- **src/ai_context_core/context/manager.py**: 3 issues (Max: MEDIUM)

### 🏗️ Critical Technical Debt:
- **src/ai_context_core/analyzer/fs_utils.py**: 3 issues (Score: 6)
- **.agent/scripts/skill_sync.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/dependencies.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/issues.py**: 2 issues (Score: 5)
- **src/ai_context_core/analyzer/reporting.py**: 2 issues (Score: 4)


## 💡 MAIN RECOMMENDATIONS

### .agent/scripts/skill_sync.py
- Very long functions (average 70.5 lines/function).

### src/ai_context_core/analyzer/ast_utils.py
- High complexity (96) with several functions. Consider breaking down large logic.
- Module is quite large (469 lines)

### src/ai_context_core/analyzer/dependencies.py
- High complexity (52) with several functions. Consider breaking down large logic.

## 🏗️ DESIGN PATTERNS

### Factory
- **AIContextManager** in `src/ai_context_core/context/manager.py` (Confidence: 70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 310
- **Additions**: +21656
- **Deletions**: -6225
- **Total Churn**: 27881

### 🔥 Hotspots (Frequently Changed Files)
- `src/ai_context_core/analyzer/engine.py`: 13 commits
- `src/ai_context_core/analyzer/reporting.py`: 13 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 11 commits
- `src/ai_context_core/analyzer/dependencies.py`: 9 commits
- `src/ai_context_core/analyzer/issues.py`: 9 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 2 modules (11.8%)
- medium (6-15): 2 modules (11.8%)
- high (16-30): 5 modules (29.4%)
- very_high (31+): 8 modules (47.1%)