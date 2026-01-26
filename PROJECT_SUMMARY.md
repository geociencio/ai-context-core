# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-26 00:22:54
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 18
- **Lines of Code**: 4,623
- **Total Size**: 0.9 MB
- **Average Complexity**: 33.3
- **Avg Maintenance Index**: 24.7
- **Docstring Coverage**: 59.9%
- **Quality Score**: 69.4/100
- **Test Files**: 16

## 📁 STRUCTURE
- **Python Files**: 34
- **Total Files**: 135
- **Primary File Types**: .md, .py, .yaml, .json, .yml

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 3 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/engine.py**: 4 issues (Max: MEDIUM)
- **src/ai_context_core/analyzer/fs_utils.py**: 7 issues (Max: MEDIUM)

### 🏗️ Critical Technical Debt:
- **.agent/scripts/skill_sync.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/dependencies.py**: 3 issues (Score: 5)
- **src/ai_context_core/analyzer/issues.py**: 2 issues (Score: 5)
- **src/ai_context_core/analyzer/ast_utils.py**: 2 issues (Score: 4)
- **src/ai_context_core/analyzer/engine.py**: 2 issues (Score: 4)

## 💡 MAIN RECOMMENDATIONS
### PROJECT_WIDE
- Project Quality Score (69.4/100) has room for improvement. Target complexity reduction.
### .agent/scripts/benchmark.py
- Very long functions (average 55.0 lines/function).
- Low docstring coverage (0/1 functions).
### .agent/scripts/skill_sync.py
- Very long functions (average 70.5 lines/function).

## 🏗️ DESIGN PATTERNS
### Factory
- **AIContextManager** in `src/ai_context_core/context/manager.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 358
- **Additions**: +26789
- **Deletions**: -10382
- **Total Churn**: 37171

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 16 commits
- `src/ai_context_core/analyzer/reporting.py`: 15 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 12 commits
- `src/ai_context_core/analyzer/dependencies.py`: 11 commits
- `src/ai_context_core/analyzer/fs_utils.py`: 10 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 2 modules (11.1%)
- medium (6-15): 3 modules (16.7%)
- high (16-30): 5 modules (27.8%)
- very_high (31+): 8 modules (44.4%)
