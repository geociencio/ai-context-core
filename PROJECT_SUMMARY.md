# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-10-08 17:58:58
Analyzer Version: 3.5.0 (Ai-Context-Core)

## 📊 KEY METRICS
- **ai-ctx Quality Score**: 100.0/100
- **Source Lines (SLOC)**: 6,362
- **Total Physical Lines**: 10,135
- **Maintainability**: 60.0
- **Test Files**: 74 test files
- _Note: the ai-ctx Quality Score is a heuristic, non-canonical metric._

**Score Breakdown**:
- Base: 100
- Maintainability: -7.5
- Tests: +10.0

## 📁 STRUCTURE
**Total Modules**: 189

```tree
./
    .ai_context_cache.json
    .analyzerignore
    .coverage
    .dockerignore
    .gitignore
    .pre-commit-config.yaml
    AGENTS.md
    ... (+25 more)
    src/
        __init__.py
        ai_context_core/
            __init__.py
            deprecations.py
            analyzer/
                __init__.py
                constants.py
                engine.py
                pattern_base.py
                registry.py
                visitors/
                    __init__.py
                    antipattern_base.py
                    antipatterns.py
                    ast_entry_points.py
                    ast_metrics.py
                    ast_qgis.py
                    ast_security.py
                    ... (+54 more)
                builders/
                    __init__.py
                    aggregator.py
                    aggregator_qgis.py
                    ai_context_generator.py
                    ai_recommendations.py
                    algorithms.py
                    builder.py
                    ... (+23 more)
                providers/
                    __init__.py
                    analyzer.py
                    compiler.py
                    config_loader.py
                    fs_cache.py
                    fs_helpers.py
                    fs_scanner.py
                    ... (+9 more)
                summarizers/
                    __init__.py
                    base.py
                    git_patterns.py
                    issues.py
                    qgis.py
                context_builders/
                    dependencies.py
                    patterns.py
                    structure.py
                checkers/
                    __init__.py
                    optimization_checker.py
                    security_checker.py
                    tech_debt_checker.py
                patterns_detectors/
                    __init__.py
                    base.py
                    decorator.py
                    decorator_rules.py
                    factory.py
                    observer.py
                    observer_rules.py
                    ... (+3 more)
                graph/
                    __init__.py
                    builder.py
                qgis_checkers/
                    base.py
                    frameworks.py
                entry_point_detectors/
                    framework_rules.py
                security_checkers/
                    base.py
            context/
                manager.py
                components/
                    __init__.py
                    builders.py
                    extractor.py
                    store.py
            config/
                defaults.toml
                loader.py
                profiles/
                    qgis.toml
            templates/
                initial_prompt.md
                workflows/
                    create-commit.md
                    end-session.md
                    start-session.md
                prompts/
            cli/
                .ai_context_cache.json
                AI_CONTEXT.md
                PROJECT_SUMMARY.md
                __init__.py
                __main__.py
                interactive.py
                project_context.json
                commands/
                    __init__.py
                    analysis.py
                    analyze.py
                    base.py
                    clean.py
                    compare.py
                    deps.py
                    ... (+15 more)
            commands/
                __init__.py
                clean.py
                report.py
            cli_groups/
                __init__.py
                specialized.py
                workflows.py
        ai_context_core.egg-info/
            PKG-INFO
            SOURCES.txt
            dependency_links.txt
            entry_points.txt
            requires.txt
            top_level.txt
    docs/
        AGENTIC_IMPLEMENTATION_GUIDE.md
        AGENTIC_STANDARDS_AND_SOURCES.md
        ARCHITECTURAL_ANALYSIS.md
        ARCHITECTURE.md
        AiContextCore_Analysis_Report.md
        CHANGELOG.md
        COMMIT_GUIDELINES.md
        ... (+18 more)
        development/
            ARCHITECTURE.md
            phases/
                phase8_implementation_plan.md
                phase8_task.md
                phase8_walkaround.md
        releases/
            github/
            notes/
                v1.0.0.md
                v1.0.1.md
                v2.1.1.md
                v2.5.0.md
                v2.5.1.md
                v2.5.2.md
                v3.0.0.md
                ... (+10 more)
            walkthroughs/
                v3.1.0-walkthrough.md
        reports/
            initial_extraction.md
        research/
        user_guide/
            PROFILES_GUIDE.md
            QUICK_START.md
        sessions/
            session_2026-01-22_fix_config_release.md
            session_2026-01-25_analysis_planning.md
            session_2026-01-25_complete_workflows_summary.md
            session_2026-01-25_docker_integration.md
            session_2026-01-25_modularization_cycle.md
            session_2026-01-25_optimization_quality.md
            session_2026-01-25_phase1_completion.md
            ... (+9 more)
        adr/
            0001-use-adr-for-architecture-decisions.md
            0002-implement-13-improvements-roadmap.md
            0003-pattern-detection-scoring-strategy.md
            0004-multi-framework-entry-point-detection.md
            0005-optimization-refactoring-strategy.md
            0006-elimination-of-root-facades-and-enforcement-of-strict-modularity.md
            0007-scoped-i18n-analysis-for-qgis-plugins.md
            ... (+1 more)
        secinterp/
            .ai_context_cache.json
            AI_CONTEXT.md
            PROJECT_SUMMARY.md
            ai_ctx_bug_report.md
            metadata.txt
            project_context.json
        maintenance/
            analysis_report.md
            bug_report_v320.md
            bug_report_v321_aggregation.md
            corrections_implementation_plan.md
            dev_feedback.md
            developer_recommendations.md
            i18n_improvement_guide.md
            ... (+4 more)
            v321_fix/
                implementation_plan.md
                walkthrough.md
    tests/
        __init__.py
        test_absolute_final.py
        test_aggregator_extended.py
        test_antipatterns.py
        test_ast_extended.py
        test_ast_metrics_compatibility.py
        test_ast_security_extended.py
        ... (+59 more)
        fixtures/
            false_positives.py
            golden_plugin/
                metadata.txt
                plugin.py
                core/
                    __init__.py
                    logic.py
                tests/
                    check_logic.py
            golden_expected/
                AI_CONTEXT.md
                PROJECT_SUMMARY.md
    test_project/
        .ai-context-updates.yaml
        project_context.json
        test.py
    scripts/
        memory_prune.py
        sync_metrics.py
        validate_agent_system.py
    dist/
        ai_context_core-3.5.0-py3-none-any.whl
        ai_context_core-3.5.0.tar.gz
```

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **check_docs.py**: 1 issues (Max: HIGH)
- **src/ai_context_core/analyzer/builders/dependencies.py**: 2 issues (Max: HIGH)
- **src/ai_context_core/analyzer/builders/parser.py**: 1 issues (Max: HIGH)

## 💡 MAIN RECOMMENDATIONS
### src/ai_context_core/analyzer/builders/aggregator.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/builders/algorithms.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/builders/calculator.py
- Consider breaking down large logic

## 🏗️ DESIGN PATTERNS
### Factory
- **DependencyAnalyzer** in `src/ai_context_core/analyzer/builders/dependencies.py` (70%)
- **GitPatternsSummarizer** in `src/ai_context_core/analyzer/builders/git_patterns.py` (70%)
- **GitPatternsSummarizer** in `src/ai_context_core/analyzer/builders/git_patterns.py` (70%)
- **IssuesSummarizer** in `src/ai_context_core/analyzer/builders/issues.py` (70%)
- **IssuesSummarizer** in `src/ai_context_core/analyzer/builders/issues.py` (70%)
### Decorator
- **register_detector** in `src/ai_context_core/analyzer/registry.py` (50%)
### Strategy
- **Context** in `test_strategy.py` (100%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 258
- **Additions**: +16878
- **Deletions**: -23308
- **Total Churn**: 40186

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 30 commits
- `src/ai_context_core/analyzer/issues.py`: 24 commits
- `src/ai_context_core/analyzer/fs_utils.py`: 24 commits
- `src/ai_context_core/analyzer/reporting.py`: 23 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 21 commits

## 📈 COMPLEXITY DISTRIBUTION
- **Avg Cyclomatic Complexity**: 6.37
- **Max Complexity**: 24
