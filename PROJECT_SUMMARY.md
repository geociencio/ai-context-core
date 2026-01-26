# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-25 23:10:02
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 15
- **Lines of Code**: 4,623
- **Total Size**: 1.1 MB
- **Average Complexity**: 40.4
- **Avg Maintenance Index**: 22.1
- **Docstring Coverage**: 96.9%
- **Quality Score**: 66.7/100
- **Test Files**: 14

## 📁 STRUCTURE
- **Python Files**: 39
- **Total Files**: 155
- **Primary File Types**: .py, .pyc, .md, .txt, .sample

## 🚨 CRITICAL ISSUES

### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 3 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/fs_utils.py**: 8 issues (Max: MEDIUM)
- **src/ai_context_core/context/manager.py**: 3 issues (Max: MEDIUM)

### 🏗️ Critical Technical Debt:
- **.agent/scripts/skill_sync.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/dependencies.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/issues.py**: 2 issues (Score: 5)
- **src/ai_context_core/analyzer/fs_utils.py**: 2 issues (Score: 5)
- **src/ai_context_core/analyzer/reporting.py**: 2 issues (Score: 4)


## 💡 MAIN RECOMMENDATIONS

### .agent/scripts/skill_sync.py
- Very long functions (average 70.5 lines/function).

### src/ai_context_core/analyzer/dependencies.py
- High complexity (52) with several functions. Consider breaking down large logic.

### src/ai_context_core/analyzer/metrics.py
- Very long functions (average 65.8 lines/function).

## 🏗️ DESIGN PATTERNS

### Factory
- **AIContextManager** in `src/ai_context_core/context/manager.py` (Confidence: 70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 289
- **Additions**: +20148
- **Deletions**: -4867
- **Total Churn**: 25015

### 🔥 Hotspots (Frequently Changed Files)
- `src/ai_context_core/analyzer/engine.py`: 12 commits
- `src/ai_context_core/analyzer/reporting.py`: 12 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 10 commits
- `src/ai_context_core/analyzer/dependencies.py`: 8 commits
- `src/ai_context_core/analyzer/issues.py`: 8 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 1 modules (6.7%)
- medium (6-15): 1 modules (6.7%)
- high (16-30): 5 modules (33.3%)
- very_high (31+): 8 modules (53.3%)