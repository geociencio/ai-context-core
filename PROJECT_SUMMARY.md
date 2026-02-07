# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-02-07 17:05:10
Analyzer Version: 3.1.1 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 107
- **Source Lines (SLOC)**: 4,351
- **Total Physical Lines**: 6,916
- **Total Size**: 2.0 MB
- **Average Complexity**: 7.2
- **Avg Maintenance Index**: 55.0
- **Docstring Coverage**: 98.1%
- **Quality Score**: 88.0/100
- **Test Files**: 0

## 📁 STRUCTURE
- **Python Files**: 230
- **Total Files**: 462
- **Primary File Types**: .py, .md, .json, .yaml, .yml

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 2 issues (Max: HIGH)
- **src/ai_context_core/analyzer/ast_metrics_components/sloc.py**: 1 issues (Max: HIGH)
- **src/ai_context_core/analyzer/dependencies.py**: 2 issues (Max: HIGH)

## 💡 MAIN RECOMMENDATIONS
### src/ai_context_core/analyzer/engine.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/patterns_detectors/observer_rules.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/security_checkers/injection.py
- Consider breaking down large logic

## 🏗️ DESIGN PATTERNS
### Factory
- **DependencyAnalyzer** in `src/ai_context_core/analyzer/dependencies.py` (70%)
- **IssuesSummarizer** in `src/ai_context_core/analyzer/summarizers/issues.py` (70%)
- **IssuesSummarizer** in `src/ai_context_core/analyzer/summarizers/issues.py` (70%)
- **MetricsSummarizer** in `src/ai_context_core/analyzer/summarizers/metrics.py` (70%)
- **SummaryGenerator** in `src/ai_context_core/analyzer/summary_generator.py` (70%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 1132
- **Additions**: +91136
- **Deletions**: -56423
- **Total Churn**: 147559

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 26 commits
- `src/ai_context_core/analyzer/fs_utils.py`: 23 commits
- `src/ai_context_core/analyzer/issues.py`: 21 commits
- `src/ai_context_core/analyzer/reporting.py`: 21 commits
- `src/ai_context_core/cli.py`: 20 commits
