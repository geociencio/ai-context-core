# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-25 22:21:36
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 15
- **Lines of Code**: 4,502
- **Total Size**: 1.1 MB
- **Average Complexity**: 39.5
- **Avg Maintenance Index**: 22.4
- **Docstring Coverage**: 97.1%
- **Quality Score**: 67.3/100
- **Test Files**: 13

## 📁 STRUCTURE
- **Python Files**: 38
- **Total Files**: 146
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

### src/ai_context_core/analyzer/dependencies.py
- High complexity (52) with several functions. Consider breaking down large logic.

### src/ai_context_core/analyzer/fs_utils.py
- High complexity (52) with several functions. Consider breaking down large logic.
- Module is quite large (462 lines)

## 🏗️ DESIGN PATTERNS

### Factory
- **AIContextManager** in `src/ai_context_core/context/manager.py` (Confidence: 70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 249
- **Additions**: +18189
- **Deletions**: -3517
- **Total Churn**: 21706

### 🔥 Hotspots (Frequently Changed Files)
- `src/ai_context_core/analyzer/reporting.py`: 9 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 8 commits
- `src/ai_context_core/analyzer/engine.py`: 8 commits
- `src/ai_context_core/analyzer/dependencies.py`: 7 commits
- `src/ai_context_core/analyzer/issues.py`: 7 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 1 modules (6.7%)
- medium (6-15): 1 modules (6.7%)
- high (16-30): 5 modules (33.3%)
- very_high (31+): 8 modules (53.3%)