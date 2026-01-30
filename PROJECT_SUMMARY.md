# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-01-30 01:12:28
Analyzer Version: 2.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 32
- **Lines of Code**: 3,216
- **Total Size**: 0.9 MB
- **Average Complexity**: 14.4
- **Avg Maintenance Index**: 35.6
- **Docstring Coverage**: 46.2%
- **Quality Score**: 44.7/100
- **Test Files**: 19

## 📁 STRUCTURE
- **Python Files**: 51
- **Total Files**: 169
- **Primary File Types**: .md, .py, .yaml, .yml, .json

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 2 issues (Max: LOW)
- **src/ai_context_core/analyzer/fs_utils.py**: 7 issues (Max: LOW)
- **src/ai_context_core/analyzer/git_analysis.py**: 3 issues (Max: LOW)

### 🏗️ Critical Technical Debt:
- **.agent/scripts/skill_sync.py**: 2 issues (Score: 4)

## 📦 QGIS STANDARDS
- **Compliance Score**: 20.0/100
- ⚠️ **Architecture**: No Processing Algorithms found (Recommended)
- **i18n Coverage**: 0.0% (0/1173 strings)

### 🚩 Metadata Issues:
- Missing metadata.txt

## 💡 MAIN RECOMMENDATIONS
### PROJECT_WIDE
- Quality Score is low (44.7/100).
- Low documentation coverage (46.19%).
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
- **Files Changed**: 468
- **Additions**: +37316
- **Deletions**: -19233
- **Total Churn**: 56549

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 20 commits
- `src/ai_context_core/analyzer/reporting.py`: 18 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 15 commits
- `src/ai_context_core/analyzer/issues.py`: 13 commits
- `src/ai_context_core/cli.py`: 13 commits

## 📈 COMPLEXITY DISTRIBUTION
- low (0-5): 17 modules (53.1%)
- medium (6-15): 5 modules (15.6%)
- high (16-30): 5 modules (15.6%)
- very_high (31+): 5 modules (15.6%)
