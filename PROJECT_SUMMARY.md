# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-26 00:51:43
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 18
- **Lines of Code**: 3,810
- **Total Size**: 0.8 MB
- **Average Complexity**: 31.8
- **Avg Maintenance Index**: 27.1
- **Docstring Coverage**: 45.6%
- **Quality Score**: 71.1/100
- **Test Files**: 16

## 📁 STRUCTURE
- **Python Files**: 34
- **Total Files**: 136
- **Primary File Types**: .md, .py, .yaml, .json, .yml

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **src/ai_context_core/analyzer/issues.py**: 3 issues (Max: HIGH)
- **.agent/scripts/benchmark.py**: 1 issues (Max: LOW)
- **.agent/scripts/skill_sync.py**: 2 issues (Max: LOW)

### 🏗️ Critical Technical Debt:
- **.agent/scripts/skill_sync.py**: 2 issues (Score: 4)
- **src/ai_context_core/analyzer/dependencies.py**: 2 issues (Score: 4)

## 💡 MAIN RECOMMENDATIONS
### PROJECT_WIDE
- Low documentation coverage (45.6%).
### src/ai_context_core/analyzer/antipatterns.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/ast_utils.py
- Consider breaking down large logic
- Large module (475 lines)

## 🏗️ DESIGN PATTERNS
### Factory
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 378
- **Additions**: +29776
- **Deletions**: -14739
- **Total Churn**: 44515

### 🔥 Hotspots
- `src/ai_context_core/analyzer/reporting.py`: 16 commits
- `src/ai_context_core/analyzer/engine.py`: 16 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 12 commits
- `src/ai_context_core/analyzer/issues.py`: 11 commits
- `src/ai_context_core/analyzer/dependencies.py`: 11 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 2 modules (11.1%)
- medium (6-15): 4 modules (22.2%)
- high (16-30): 5 modules (27.8%)
- very_high (31+): 7 modules (38.9%)
