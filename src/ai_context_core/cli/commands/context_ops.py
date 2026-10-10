"""Context operations: verify, symbols, health (v5.0.0 F4)."""

import pathlib
import sys

import click


@click.command(name="verify")
@click.option("--path", default=".", help="Project path")
def verify_cmd(path: str):
    """Exit 1 when context artifacts are stale relative to the sources."""
    from ai_context_core.context.verify import verify_context

    report = verify_context(pathlib.Path(path))
    if report["fresh"]:
        click.echo("Context is fresh.")
        return
    click.secho(f"Context is stale: {report['reason']}", fg="red", err=True)
    sys.exit(1)


@click.command(name="symbols")
@click.option("--path", default=".", help="Project path")
@click.option("--grep", default=None, help="Filter definitions/references by substring")
def symbols_cmd(path: str, grep: str):
    """Build symbols.json; with --grep print matching file:line entries."""
    from ai_context_core.context.symbol_index import (
        build_symbol_index,
        search_symbols,
        write_symbol_index,
    )

    proj = pathlib.Path(path).resolve()
    index = build_symbol_index(proj)
    write_symbol_index(proj, index)

    if grep:
        matches = search_symbols(index, grep)
        for line in matches:
            click.echo(line)
        if not matches:
            sys.exit(1)
        return

    click.echo(
        f"symbols.json written: {len(index['symbols'])} definitions, "
        f"{len(index['references'])} references"
    )


@click.command(name="health")
@click.option("--path", default=".", help="Project path")
def health_cmd(path: str):
    """Show context health (freshness, tokens, symbols, provenance)."""
    from ai_context_core.context.health import compute_health

    report = compute_health(pathlib.Path(path))
    click.secho("CONTEXT HEALTH", fg="cyan", bold=True)
    reason = "" if report["fresh"] else f" ({report['reason']})"
    click.echo(f"- Fresh: {report['fresh']}{reason}")

    tokens = report["tokens"]
    if tokens["total"] is not None:
        budget = f" / {tokens['budget']}" if tokens["budget"] else ""
        click.echo(f"- Tokens: {tokens['total']}{budget} (truncated: {tokens['truncated']})")

    symbols = report["symbols"]
    click.echo(
        f"- Symbols: {symbols['definitions']} definitions, {symbols['references']} references"
    )

    provenance = report["provenance"]
    if provenance:
        click.echo(f"- Provenance: {provenance.get('source')} v{provenance.get('tool_version')}")

    if not report["fresh"]:
        sys.exit(1)
