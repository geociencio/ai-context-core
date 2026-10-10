# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-10-09 20:50:47
Analyzer Version: 4.1.1 (Ai-Context-Core)

## 📊 KEY METRICS
- **ai-ctx Quality Score**: 97.7/100
- **Source Lines (SLOC)**: 3,950
- **Total Physical Lines**: 6,405
- **Maintainability**: 56.8
- **Test Files**: 40 test files
- _Note: the ai-ctx Quality Score is a heuristic, non-canonical metric._

**Score Breakdown**:
- Base: 100
- Maintainability: -12.3
- Tests: +10.0

## 📁 STRUCTURE
**Total Modules**: 111

```tree
./
    .ai_context_cache.json
    .analyzerignore
    .coverage
    .dockerignore
    .gitignore
    .gitmodules
    .pre-commit-config.yaml
    ... (+25 more)
    dist/
        ai_context_core-4.1.1-py3-none-any.whl
        ai_context_core-4.1.1.tar.gz
    docs/
        AGENTIC_FORGE_ADOPTION.md
        AGENTIC_IMPLEMENTATION_GUIDE.md
        AGENTIC_STANDARDS_AND_SOURCES.md
        ARCHITECTURAL_ANALYSIS.md
        ARCHITECTURE.md
        AiContextCore_Analysis_Report.md
        CHANGELOG.md
        ... (+19 more)
        adr/
            0001-use-adr-for-architecture-decisions.md
            0002-implement-13-improvements-roadmap.md
            0003-pattern-detection-scoring-strategy.md
            0004-multi-framework-entry-point-detection.md
            0005-optimization-refactoring-strategy.md
            0006-elimination-of-root-facades-and-enforcement-of-strict-modularity.md
            0007-scoped-i18n-analysis-for-qgis-plugins.md
            ... (+2 more)
        development/
            ARCHITECTURE.md
            phases/
                phase8_implementation_plan.md
                phase8_task.md
                phase8_walkaround.md
        maintenance/
            analysis_report.md
            bug_report_v320.md
            bug_report_v321_aggregation.md
            corrections_implementation_plan.md
            dev_feedback.md
            developer_recommendations.md
            i18n_improvement_guide.md
            ... (+11 more)
            v321_fix/
                implementation_plan.md
                walkthrough.md
        plans/
            implementation_plan_ai_context_core_context_only_v5.md
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
                ... (+13 more)
            walkthroughs/
                v3.1.0-walkthrough.md
        reports/
            initial_extraction.md
        research/
        reviews/
            ia_critic_implementation_plan_context_only_v5.md
        secinterp/
            .ai_context_cache.json
            AI_CONTEXT.md
            PROJECT_SUMMARY.md
            ai_ctx_bug_report.md
            metadata.txt
            project_context.json
        sessions/
            session_2026-01-22_fix_config_release.md
            session_2026-01-25_analysis_planning.md
            session_2026-01-25_complete_workflows_summary.md
            session_2026-01-25_docker_integration.md
            session_2026-01-25_modularization_cycle.md
            session_2026-01-25_optimization_quality.md
            session_2026-01-25_phase1_completion.md
            ... (+10 more)
        user_guide/
            PROFILES_GUIDE.md
            QUICK_START.md
    scripts/
        sync_metrics.py
    src/
        __init__.py
        ai_context_core/
            __init__.py
            deprecations.py
            analyzer/
                __init__.py
                constants.py
                engine.py
                registry.py
                builders/
                    __init__.py
                    aggregator.py
                    ai_context_generator.py
                    algorithms.py
                    builder.py
                    builder_components.py
                    builders_base.py
                    ... (+17 more)
                providers/
                    __init__.py
                    analyzer.py
                    compiler.py
                    config_loader.py
                    context_fields.py
                    fs_cache.py
                    fs_helpers.py
                    ... (+10 more)
                visitors/
                    __init__.py
                    ast_entry_points.py
                    ast_metrics.py
                    ast_utils.py
                    ast_visitors.py
                    checker_base.py
                    classes.py
                    ... (+12 more)
            cli/
                .ai_context_cache.json
                AI_CONTEXT.md
                PROJECT_SUMMARY.md
                __init__.py
                __main__.py
                project_context.json
                commands/
                    __init__.py
                    analysis.py
                    analyze.py
                    base.py
                    clean.py
                    compare.py
                    deprecated.py
                    ... (+9 more)
            config/
                defaults.toml
                loader.py
                profiles/
            context/
                manager.py
                components/
                    __init__.py
                    builders.py
                    extractor.py
                    store.py
            model/
                __init__.py
                analysis_result.py
            sources/
                __init__.py
                base.py
                pipeline.py
                builtin/
                    __init__.py
                    engine_source.py
                external/
                    __init__.py
                    qgis_analyzer.py
            templates/
                initial_prompt.md
                prompts/
                workflows/
                    create-commit.md
                    end-session.md
                    start-session.md
        ai_context_core.egg-info/
            PKG-INFO
            SOURCES.txt
            dependency_links.txt
            entry_points.txt
            requires.txt
            top_level.txt
    test_project/
        .ai-context-updates.yaml
        project_context.json
        test.py
    tests/
        __init__.py
        test_ast_extended.py
        test_ast_metrics_compatibility.py
        test_ast_utils.py
        test_cache_integration.py
        test_cli.py
        test_cli_error_coverage.py
        ... (+25 more)
        fixtures/
            false_positives.py
            golden_expected/
                AI_CONTEXT.md
                PROJECT_SUMMARY.md
            golden_plugin/
                metadata.txt
                plugin.py
                core/
                    __init__.py
                    logic.py
                tests/
                    check_logic.py
```

## 🚨 CRITICAL ISSUES

### 🔄 Circular Dependencies:
- src/ai_context_core/analyzer/builders/aggregator.py -> src/ai_context_core/analyzer/builders/dependencies.py -> src/ai_context_core/analyzer/builders/reporting.py -> src/ai_context_core/analyzer/builders/ai_context_generator.py -> src/ai_context_core/analyzer/builders/__init__.py
- src/ai_context_core/analyzer/builders/dependencies.py -> src/ai_context_core/analyzer/builders/reporting.py -> src/ai_context_core/analyzer/builders/ai_context_generator.py -> src/ai_context_core/analyzer/builders/__init__.py
- src/ai_context_core/analyzer/builders/reporting.py -> src/ai_context_core/analyzer/builders/ai_context_generator.py -> src/ai_context_core/analyzer/builders/__init__.py -> src/ai_context_core/analyzer/builders/summary_generator.py

## 💡 MAIN RECOMMENDATIONS
### src/ai_context_core/analyzer/builders/algorithms.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/builders/calculator.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/builders/reporting.py
- Consider breaking down large logic

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 210
- **Additions**: +62304
- **Deletions**: -66706
- **Total Churn**: 129010

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 35 commits
- `src/ai_context_core/analyzer/issues.py`: 24 commits
- `src/ai_context_core/analyzer/fs_utils.py`: 24 commits
- `src/ai_context_core/analyzer/reporting.py`: 23 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 21 commits

## 📈 COMPLEXITY DISTRIBUTION
- **Avg Cyclomatic Complexity**: 6.05
- **Max Complexity**: 23
