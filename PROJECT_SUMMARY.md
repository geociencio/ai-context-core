# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-26 00:14:22
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 18
- **Lines of Code**: 4,746
- **Total Size**: 0.9 MB
- **Average Complexity**: 34.7
- **Avg Maintenance Index**: 24.5
- **Docstring Coverage**: 71.0%
- **Quality Score**: 68.9/100
- **Test Files**: 16

## 📁 STRUCTURE
- **Python Files**: 34
- **Total Files**: 135
- **Primary File Types**: .md, .py, .yaml, .json, .yml

## 🚨 CRITICAL ISSUES

### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 3 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/reporting.py**: 1 issues (Max: MEDIUM)
- **src/ai_context_core/context/manager.py**: 3 issues (Max: MEDIUM)

### 🏗️ Critical Technical Debt:
- **src/ai_context_core/analyzer/reporting.py**: 3 issues (Score: 6)
- **.agent/scripts/skill_sync.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/dependencies.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/issues.py**: 2 issues (Score: 5)
- **src/ai_context_core/analyzer/ast_utils.py**: 2 issues (Score: 4)


## 💡 MAIN RECOMMENDATIONS

### PROJECT_WIDE
- Project Quality Score (68.9/100) has room for improvement. Target complexity reduction.

### .agent/scripts/benchmark.py
- Very long functions (average 57.0 lines/function).
- Low docstring coverage (0/1 functions).

### .agent/scripts/skill_sync.py
- Very long functions (average 70.5 lines/function).

## 🏗️ DESIGN PATTERNS

### Factory
- **AIContextManager** in `src/ai_context_core/context/manager.py` (Confidence: 70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 346
- **Additions**: +25110
- **Deletions**: -8160
- **Total Churn**: 33270

### 🔥 Hotspots (Frequently Changed Files)
- `src/ai_context_core/analyzer/engine.py`: 15 commits
- `src/ai_context_core/analyzer/reporting.py`: 14 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 11 commits
- `src/ai_context_core/analyzer/dependencies.py`: 10 commits
- `src/ai_context_core/analyzer/issues.py`: 10 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 2 modules (11.1%)
- medium (6-15): 3 modules (16.7%)
- high (16-30): 5 modules (27.8%)
- very_high (31+): 8 modules (44.4%)