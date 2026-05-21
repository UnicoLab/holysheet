"""HolySheet CLI.

Provides command-line utilities for validating and serving reports.

Usage::

    holysheet validate report.json
    holysheet serve report.json
    holysheet version
"""

from __future__ import annotations

import http.server
import json
import shutil
import socketserver
import sys
import tempfile
import webbrowser
from pathlib import Path

import click
from loguru import logger

from holysheet import __version__
from holysheet.exceptions import ExportError, HolySheetError, SchemaValidationError

# ---------------------------------------------------------------------------
# CLI group
# ---------------------------------------------------------------------------


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
def cli(verbose: bool) -> None:
    """HolySheet — Python-first report compiler for interactive dashboards."""
    # Configure loguru
    logger.remove()  # Remove default handler
    level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | {message}",
    )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@cli.command()
@click.argument("report_json", type=click.Path(exists=True, dir_okay=False))
def validate(report_json: str) -> None:
    """Validate a HolySheet JSON spec file.

    REPORT_JSON is the path to the JSON spec file to validate.
    """
    from holysheet.schema import ReportSchema

    path = Path(report_json)
    click.echo(f"Validating {path.name}...")

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        schema = ReportSchema.model_validate(data)

        click.echo(click.style("✓ Valid HolySheet spec", fg="green"))
        click.echo(f"  Title:          {schema.title}")
        click.echo(f"  Schema version: {schema.schema_version}")
        click.echo(f"  Theme:          {schema.theme}")
        click.echo(f"  Blocks:         {len(schema.blocks)}")
        click.echo(f"  Created at:     {schema.created_at}")

    except json.JSONDecodeError as exc:
        raise click.ClickException(f"Invalid JSON: {exc}") from exc
    except SchemaValidationError as exc:
        raise click.ClickException(f"Schema validation failed: {exc.message}") from exc
    except Exception as exc:
        raise click.ClickException(f"Validation error: {exc}") from exc


@cli.command()
@click.argument("report_json", type=click.Path(exists=True, dir_okay=False))
@click.option("--port", "-p", default=8765, type=int, help="Port to serve on.")
@click.option("--no-open", is_flag=True, help="Don't auto-open browser.")
def serve(report_json: str, port: int, no_open: bool) -> None:
    """Start a local HTTP server and open the report in a browser.

    REPORT_JSON is the path to the JSON spec file to serve.
    """
    from holysheet.exporters import export_folder
    from holysheet.schema import ReportSchema

    path = Path(report_json)

    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        schema = ReportSchema.model_validate(data)
    except Exception as exc:
        raise click.ClickException(f"Failed to load spec: {exc}") from exc

    # Export to a temp folder
    tmp_dir = Path(tempfile.mkdtemp(prefix="holysheet_"))
    try:
        export_folder(schema, tmp_dir)
    except (ExportError, HolySheetError) as exc:
        raise click.ClickException(f"Export failed: {exc.message}") from exc

    # Serve
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            super().__init__(*args, directory=str(tmp_dir), **kwargs)

        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            logger.debug(format, *args)

    url = f"http://localhost:{port}"
    click.echo(f"Serving {path.name} at {click.style(url, fg='cyan', bold=True)}")
    click.echo("Press Ctrl+C to stop.")

    if not no_open:
        webbrowser.open(url)

    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


@cli.command()
def version() -> None:
    """Show the HolySheet version."""
    click.echo(f"holysheet {__version__}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cli()
