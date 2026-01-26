# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-26 02:38:43
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 17
- **Lines of Code**: 4,218
- **Total Size**: 0.8 MB
- **Average Complexity**: 39.3
- **Avg Maintenance Index**: 24.1
- **Docstring Coverage**: 47.5%
- **Quality Score**: 48.4/100
- **Test Files**: 16

## 📁 STRUCTURE
- **Python Files**: 33
- **Total Files**: 138
- **Primary File Types**: .md, .py, .yaml, .json, .yml

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **src/ai_context_core/analyzer/issues.py**: 3 issues (Max: HIGH)
- **.agent/scripts/skill_sync.py**: 2 issues (Max: LOW)
- **src/ai_context_core/analyzer/ast_utils.py**: 1 issues (Max: LOW)

### 🏗️ Critical Technical Debt:
- **src/ai_context_core/analyzer/ast_utils.py**: 2 issues (Score: 5)
- **src/ai_context_core/analyzer/reporting.py**: 2 issues (Score: 5)
- **.agent/scripts/skill_sync.py**: 2 issues (Score: 4)
- **src/ai_context_core/analyzer/dependencies.py**: 2 issues (Score: 4)

## 📦 QGIS STANDARDS
- **Compliance Score**: 20.0/100
- ⚠️ **Architecture**: No Processing Algorithms found (Recommended)
- **i18n Coverage**: 0.0% (0/1726 strings)

### 🚩 Metadata Issues:
- Missing metadata.txt

## 💡 MAIN RECOMMENDATIONS
### PROJECT_WIDE
- Quality Score is low (48.4/100).
- Low documentation coverage (47.46%).
### src/ai_context_core/analyzer/antipatterns.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/ast_utils.py
- Consider breaking down large logic
- Large module (560 lines)

## 🏗️ DESIGN PATTERNS
### Factory
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/reporting.py` (70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 388
- **Additions**: +30157
- **Deletions**: -14921
- **Total Churn**: 45078

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 17 commits
- `src/ai_context_core/analyzer/reporting.py`: 16 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 12 commits
- `src/ai_context_core/cli.py`: 11 commits
- `src/ai_context_core/analyzer/issues.py`: 11 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 1 modules (5.9%)
- medium (6-15): 3 modules (17.6%)
- high (16-30): 5 modules (29.4%)
- very_high (31+): 8 modules (47.1%)
