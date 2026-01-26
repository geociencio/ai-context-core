import cProfile
import pstats
import time
from io import StringIO
from ai_context_core.cli import analyze


def run_benchmark():
    print("🚀 Starting benchmark for ai-context-core...")

    # Setup cProfile
    pr = cProfile.Profile()
    pr.enable()

    start_time = time.time()

    # Run analysis on the current directory (simulating self-analysis)
    try:
        # Assuming analyze is a click command, we might need to invoke it directly or simulate context
        # But looking at cli.py, it likely uses click. Let's try wrapping the core engine logic directly if possible,
        # or just invoking the cli function catch-all.
        # Ideally we want to profile the `analyze` command execution.
        from click.testing import CliRunner

        runner = CliRunner()
        result = runner.invoke(analyze, [])
        if result.exit_code != 0:
            print(f"❌ Analysis failed: {result.output}")
            return

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        return

    end_time = time.time()
    pr.disable()

    duration = end_time - start_time
    print(f"✅ Benchmark completed in {duration:.4f} seconds")

    # Save stats
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(30)  # Print top 30 cumulative time

    print("\n--- Top 30 Functions by Cumulative Time ---")
    print(s.getvalue())

    # Also dump to file for visualization like snakeviz if needed
    pr.dump_stats(".agent/scripts/profile_stats.prof")
    print("💾 Profile stats saved to .agent/scripts/profile_stats.prof")


if __name__ == "__main__":
    run_benchmark()
