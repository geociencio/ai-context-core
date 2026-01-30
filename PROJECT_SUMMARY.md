# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-30 01:25:44
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 39
- **Lines of Code**: 2,996
- **Total Size**: 0.9 MB
- **Average Complexity**: 9.3
- **Avg Maintenance Index**: 37.3
- **Docstring Coverage**: 48.2%
- **Quality Score**: 41.9/100
- **Test Files**: 19

## 📁 STRUCTURE
- **Python Files**: 59
- **Total Files**: 178
- **Primary File Types**: .md, .py, .yaml, .yml, .json

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 2 issues (Max: LOW)
- **src/ai_context_core/analyzer/engine.py**: 6 issues (Max: LOW)
- **src/ai_context_core/analyzer/git_analysis.py**: 3 issues (Max: LOW)

### 🏗️ Critical Technical Debt:
- **src/ai_context_core/analyzer/engine.py**: 2 issues (Score: 5)
- **.agent/scripts/skill_sync.py**: 2 issues (Score: 4)

## 📦 QGIS STANDARDS
- **Compliance Score**: 20.0/100
- ⚠️ **Architecture**: No Processing Algorithms found (Recommended)
- **i18n Coverage**: 0.0% (0/1223 strings)

### 🚩 Metadata Issues:
- Missing metadata.txt

## 💡 MAIN RECOMMENDATIONS
### PROJECT_WIDE
- Quality Score is low (41.9/100).
- Low documentation coverage (48.21%).
### src/ai_context_core/analyzer/antipatterns.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/engine.py
- Consider breaking down large logic
- Large module (539 lines)

## 🏗️ DESIGN PATTERNS
### Factory
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 480
- **Additions**: +38236
- **Deletions**: -20222
- **Total Churn**: 58458

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 21 commits
- `src/ai_context_core/analyzer/reporting.py`: 18 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 16 commits
- `src/ai_context_core/analyzer/issues.py`: 14 commits
- `src/ai_context_core/cli.py`: 13 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 24 modules (61.5%)
- medium (6-15): 5 modules (12.8%)
- high (16-30): 6 modules (15.4%)
- very_high (31+): 4 modules (10.3%)
