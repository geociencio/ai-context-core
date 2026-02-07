# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-02-07 16:25:56
Analyzer Version: 3.1.1 (Ai-Context-Core)

## 📊 KEY METRICS
- **Total Modules**: 93
- **Source Lines (SLOC)**: 3,575
- **Total Physical Lines**: 5,738
- **Total Size**: 1.6 MB
- **Average Complexity**: 6.9
- **Avg Maintenance Index**: 56.8
- **Docstring Coverage**: 97.8%
- **Quality Score**: 88.5/100
- **Test Files**: 0

## 📁 STRUCTURE
- **Python Files**: 219
- **Total Files**: 420
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
- **Files Changed**: 1121
- **Additions**: +83250
- **Deletions**: -54160
- **Total Churn**: 137410

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 26 commits
- `src/ai_context_core/analyzer/fs_utils.py`: 22 commits
- `src/ai_context_core/analyzer/issues.py`: 21 commits
- `src/ai_context_core/analyzer/reporting.py`: 21 commits
- `src/ai_context_core/cli.py`: 20 commits
