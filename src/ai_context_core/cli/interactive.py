"""Interactive mode for ai-context-core CLI."""

import click
import sys

try:
    from rich.console import Console
    from rich.prompt import Prompt, FloatPrompt, Confirm
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    # Fallback if rich is not installed, though it's a dependency
    sys.exit("Rich is required for interactive mode. Please install it.")


from .commands import analyze

console = Console()


@click.command(name="interactive")
def interactive_cmd():
    """Launches the interactive mode."""
    show_welcome()

    while True:
        choice = main_menu()

        if choice == "analyze":
            run_analyze_flow()
        elif choice == "audit":
            run_audit_flow()
        elif choice == "patterns":
            run_patterns_flow()
        elif choice == "qgis":
            run_qgis_flow()
        elif choice == "exit":
            console.print("[bold green]Goodbye![/bold green] 👋")
            break


def show_welcome():
    """Displays the welcome banner."""
    title = Text("Ai-Context-Core Interactive", style="bold magenta")
    subtitle = Text("Guided context management and analysis", style="italic")
    panel = Panel(Text.assemble(title, "\n", subtitle), border_style="cyan")
    console.print(panel)


def main_menu() -> str:
    """Displays the main menu and returns selection."""
    console.print("\n[bold cyan]Main Menu[/bold cyan]")
    options = {
        "1": ("Analyze Project", "analyze"),
        "2": ("Audit Quality", "audit"),
        "3": ("Detect Patterns", "patterns"),
        "4": ("QGIS Compliance", "qgis"),
        "0": ("Exit", "exit"),
    }

    for key, (label, _) in options.items():
        console.print(f"[{key}] {label}")

    choice = Prompt.ask("Select an option", choices=list(options.keys()), default="1")
    return options[choice][1]


def run_analyze_flow():
    """Guided flow for project analysis."""
    console.print("\n[bold]running Analysis...[/bold]")
    path = Prompt.ask("Project path", default=".")
    fmt = Prompt.ask("Output format", choices=["markdown", "html"], default="markdown")
    workers_str = Prompt.ask("Parallel workers (empty for auto)", default="")
    workers = int(workers_str) if workers_str.isdigit() else None
    no_cache = Confirm.ask("Force full scan (ignore cache)?", default=False)

    with console.status("[bold green]Analyzing...[/bold green]"):
        try:
            analyze.run_analysis(path, workers, fmt, no_cache)
            console.print("[bold green]Analysis Complete! ✅[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")


def run_audit_flow():
    """Guided flow for quality audit."""
    console.print("\n[bold]Running Quality Audit...[/bold]")
    path = Prompt.ask("Project path", default=".")
    threshold = FloatPrompt.ask("Quality Threshold", default=80.0)

    try:
        analyze.run_audit(path, threshold)
    except SystemExit as e:
        if e.code == 0:
            console.print("[bold green]Audit Passed! 🛡️[/bold green]")
        else:
            console.print("[bold red]Audit Failed! ❌[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


def run_patterns_flow():
    """Guided flow for pattern detection."""
    console.print("\n[bold]Detecting Design Patterns...[/bold]")
    Prompt.ask("Project path", default=".")

    # Needs implementation in commands/patterns.py or exposed logic
    # checking if we can import a run_patterns function, reusing logic similar to cli
    # For now, we simulate calling the core logic directly via engine or shell
    # But best to use the existing command logic if possible.
    # Since we can't easily import the click command as a function without context,
    # we might need to expose a python API for patterns.
    # Assuming analyze.run_analysis covers general, but specific patterns might be separate.

    # As a simple implementation for now, we warn it's part of analysis usually
    console.print(
        "[yellow]Note: Patterns are typically part of the full analysis.[/yellow]"
    )
    if Confirm.ask("Run specialized pattern scan?"):
        # Placeholder for specialized pattern run if we had a dedicated python API exposed
        # Currently patterns are integrated in analysis engine.
        pass


def run_qgis_flow():
    """Guided flow for QGIS compliance."""
    console.print("\n[bold]Checking QGIS Compliance...[/bold]")
    path = Prompt.ask("Project path", default=".")

    # Similar to patterns, would call into qgis logic.
    # To be implemented fully when python API is exposed.
    console.print("[italic]Launching QGIS compliance check...[/italic]")
    try:
        from .commands import qgis

        qgis.check_compliance(path, 70.0)  # Default threshold
    except ImportError:
        console.print("[red]QGIS command module not found.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
