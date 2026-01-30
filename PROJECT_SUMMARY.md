# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-30 00:31:04
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 33
- **Lines of Code**: 5,033
- **Total Size**: 0.9 MB
- **Average Complexity**: 22.5
- **Avg Maintenance Index**: 34.7
- **Docstring Coverage**: 55.9%
- **Quality Score**: 54.9/100
- **Test Files**: 18

## 📁 STRUCTURE
- **Python Files**: 51
- **Total Files**: 164
- **Primary File Types**: .md, .py, .yaml, .json, .yml

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 2 issues (Max: LOW)
- **src/ai_context_core/analyzer/fs_utils.py**: 7 issues (Max: LOW)
- **src/ai_context_core/analyzer/git_analysis.py**: 3 issues (Max: LOW)

### 🏗️ Critical Technical Debt:
- **src/ai_context_core/analyzer/engine.py**: 2 issues (Score: 5)
- **.agent/scripts/skill_sync.py**: 2 issues (Score: 4)
- **src/ai_context_core/analyzer/ast_qgis.py**: 2 issues (Score: 4)

## 📦 QGIS STANDARDS
- **Compliance Score**: 20.0/100
- ⚠️ **Architecture**: No Processing Algorithms found (Recommended)
- **i18n Coverage**: 0.0% (0/1893 strings)

### 🚩 Metadata Issues:
- Missing metadata.txt

## 💡 MAIN RECOMMENDATIONS
### PROJECT_WIDE
- Quality Score (54.9/100) has room for improvement.
### src/ai_context_core/analyzer/antipatterns.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/fs_utils.py
- Consider breaking down large logic
- Large module (447 lines)

## 🏗️ DESIGN PATTERNS
### Factory
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 431
- **Additions**: +33496
- **Deletions**: -17208
- **Total Churn**: 50704

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 19 commits
- `src/ai_context_core/analyzer/reporting.py`: 18 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 14 commits
- `src/ai_context_core/cli.py`: 13 commits
- `src/ai_context_core/analyzer/fs_utils.py`: 12 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 10 modules (30.3%)
- medium (6-15): 8 modules (24.2%)
- high (16-30): 6 modules (18.2%)
- very_high (31+): 9 modules (27.3%)
