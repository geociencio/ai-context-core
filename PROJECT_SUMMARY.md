# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-25 22:37:56
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 15
- **Lines of Code**: 4,370
- **Total Size**: 1.1 MB
- **Average Complexity**: 39.5
- **Avg Maintenance Index**: 22.6
- **Docstring Coverage**: 96.8%
- **Quality Score**: 67.3/100
- **Test Files**: 13

## 📁 STRUCTURE
- **Python Files**: 38
- **Total Files**: 146
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
- **src/ai_context_core/analyzer/reporting.py**: 2 issues (Score: 4)


## 💡 MAIN RECOMMENDATIONS

### .agent/scripts/skill_sync.py
- Very long functions (average 67.5 lines/function).

### src/ai_context_core/analyzer/metrics.py
- Very long functions (average 62.8 lines/function).

### src/ai_context_core/analyzer/dependencies.py
- High complexity (52) with several functions. Consider breaking down large logic.

## 🏗️ DESIGN PATTERNS

### Factory
- **AIContextManager** in `src/ai_context_core/context/manager.py` (Confidence: 70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 281
- **Additions**: +19842
- **Deletions**: -4776
- **Total Churn**: 24618

### 🔥 Hotspots (Frequently Changed Files)
- `src/ai_context_core/analyzer/reporting.py`: 12 commits
- `src/ai_context_core/analyzer/engine.py`: 11 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 9 commits
- `src/ai_context_core/analyzer/dependencies.py`: 8 commits
- `src/ai_context_core/analyzer/issues.py`: 8 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 1 modules (6.7%)
- medium (6-15): 1 modules (6.7%)
- high (16-30): 6 modules (40.0%)
- very_high (31+): 7 modules (46.7%)