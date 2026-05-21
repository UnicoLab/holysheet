"""HolySheet CLI.

Provides command-line utilities for validating, serving, linting, and
comparing reports.

Usage::

    holysheet validate report.json
    holysheet serve report.json
    holysheet dev my_report.py
    holysheet lint my_report.py
    holysheet diff spec_a.json spec_b.json
    holysheet version
"""

from __future__ import annotations

import http.server
import json
import os
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any, ClassVar

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


# ---------------------------------------------------------------------------
# dev — Hot Reload Dev Server
# ---------------------------------------------------------------------------

# Auto-reload JavaScript snippet injected into served HTML files.
# Polls /api/version every second and reloads when the version changes.
_AUTO_RELOAD_JS = """\
<script>
(function() {
    var currentVersion = null;
    function poll() {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/version", true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var v = xhr.responseText.trim();
                if (currentVersion === null) {
                    currentVersion = v;
                } else if (v !== currentVersion) {
                    location.reload();
                }
            }
        };
        xhr.send();
    }
    setInterval(poll, 1000);
})();
</script>
"""


def _run_script(script_path: Path, output_dir: Path) -> bool:
    """Execute a Python report script via subprocess.

    The script is expected to call ``report.export_html()`` or similar.
    We set the ``HOLYSHEET_DEV_OUTPUT`` environment variable so scripts
    can detect dev-mode and write to the expected location.

    Args:
        script_path: Absolute path to the Python script.
        output_dir: Directory where the script should write output.

    Returns:
        ``True`` if the script exited successfully, ``False`` otherwise.
    """
    env = os.environ.copy()
    env["HOLYSHEET_DEV_OUTPUT"] = str(output_dir)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(script_path.parent),
        env=env,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        click.echo(click.style("✗ Script error:", fg="red"))
        if result.stderr:
            for line in result.stderr.strip().splitlines()[-10:]:
                click.echo(f"  {line}")
        return False

    if result.stdout:
        logger.debug("Script stdout: {}", result.stdout.strip())
    return True


def _inject_reload_snippet(output_dir: Path) -> None:
    """Inject the auto-reload JS snippet into all HTML files in *output_dir*.

    The snippet is inserted just before ``</body>`` (or appended at the end
    if ``</body>`` is not found).

    Args:
        output_dir: Directory containing HTML files to patch.
    """
    for html_file in output_dir.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if "/api/version" in content:
            continue  # already injected
        if "</body>" in content:
            content = content.replace("</body>", f"{_AUTO_RELOAD_JS}</body>")
        else:
            content += _AUTO_RELOAD_JS
        html_file.write_text(content, encoding="utf-8")


def _find_html_output(output_dir: Path, script_path: Path) -> Path | None:
    """Attempt to locate the generated HTML file.

    Looks in *output_dir* first, then in the script's directory for any
    ``.html`` file that was recently modified.

    Args:
        output_dir: The dev output directory.
        script_path: The source script path.

    Returns:
        Path to the HTML file, or ``None`` if not found.
    """
    # Check output_dir for any .html files
    for html_file in output_dir.rglob("*.html"):
        return html_file

    # Fallback: look in script's directory for recently-created HTML files
    script_dir = script_path.parent
    html_files = sorted(script_dir.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    if html_files:
        # Copy the most recent HTML file into output_dir
        target = output_dir / html_files[0].name
        shutil.copy2(html_files[0], target)
        return target

    return None


@cli.command()
@click.argument("script", type=click.Path(exists=True, dir_okay=False))
@click.option("--port", "-p", default=8000, type=int, help="Port to serve on.")
@click.option("--no-open", is_flag=True, help="Don't auto-open browser.")
def dev(script: str, port: int, no_open: bool) -> None:
    """Start a hot-reload dev server for a report script.

    SCRIPT is the path to a Python script that generates a HolySheet report.
    The script is re-executed automatically when the file changes, and the
    browser reloads to show the updated report.
    """
    script_path = Path(script).resolve()
    output_dir = Path(tempfile.mkdtemp(prefix="holysheet_dev_"))

    # Mutable state shared between the watcher thread and the HTTP handler.
    build_version = {"value": 0}
    build_lock = threading.Lock()

    def rebuild() -> bool:
        """Run the script, inject the reload snippet, and bump the version."""
        # Clean output directory (except don't remove the dir itself)
        for child in output_dir.iterdir():
            if child.is_dir():
                shutil.rmtree(child, ignore_errors=True)
            else:
                child.unlink(missing_ok=True)

        click.echo(f"  Building from {script_path.name}...")
        success = _run_script(script_path, output_dir)

        if success:
            # Try to find the generated HTML
            html = _find_html_output(output_dir, script_path)
            if html is None:
                click.echo(click.style("  ⚠ No HTML output found", fg="yellow"))
                return False
            # Ensure the HTML is named index.html for the server
            if html.name != "index.html":
                target = output_dir / "index.html"
                if target.exists():
                    target.unlink()
                shutil.copy2(html, target)
            _inject_reload_snippet(output_dir)
            with build_lock:
                build_version["value"] += 1
            click.echo(click.style(f"  ✓ Build #{build_version['value']} ready", fg="green"))
            return True
        return False

    # Initial build
    if not rebuild():
        click.echo(click.style("Initial build failed. Watching for changes...", fg="yellow"))

    # --- File watcher (polling with os.stat) ---

    def watcher() -> None:
        """Poll the script file's mtime and trigger rebuilds on change."""
        last_mtime = os.stat(str(script_path)).st_mtime
        while True:
            time.sleep(0.5)
            try:
                current_mtime = os.stat(str(script_path)).st_mtime
            except OSError:
                continue
            if current_mtime != last_mtime:
                last_mtime = current_mtime
                click.echo(
                    click.style(f"\n↻ Change detected in {script_path.name}", fg="cyan", bold=True)
                )
                rebuild()

    watcher_thread = threading.Thread(target=watcher, daemon=True)
    watcher_thread.start()

    # --- HTTP server with /api/version endpoint ---

    class DevHandler(http.server.SimpleHTTPRequestHandler):
        """HTTP handler that serves static files and the version API."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(output_dir), **kwargs)

        def do_GET(self) -> None:
            if self.path == "/api/version":
                with build_lock:
                    ver = str(build_version["value"])
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Cache-Control", "no-cache, no-store")
                self.end_headers()
                self.wfile.write(ver.encode())
            else:
                super().do_GET()

        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            # Suppress noisy version-poll logs
            if len(args) >= 1 and isinstance(args[0], str) and "/api/version" in args[0]:
                return
            logger.debug(format, *args)

    url = f"http://localhost:{port}"
    click.echo("\n🔥 HolySheet Dev Server")
    click.echo(f"   Watching: {click.style(str(script_path), fg='cyan')}")
    click.echo(f"   Serving:  {click.style(url, fg='cyan', bold=True)}")
    click.echo("   Press Ctrl+C to stop.\n")

    if not no_open:
        webbrowser.open(url)

    try:
        with socketserver.TCPServer(("", port), DevHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        click.echo("\nDev server stopped.")
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# lint — Report Linting
# ---------------------------------------------------------------------------

# Chart block types that should have a title
_CHART_TYPES = frozenset(
    {
        "line_chart",
        "area_chart",
        "bar_chart",
        "pie_chart",
        "scatter_chart",
        "radar_chart",
        "gauge",
        "funnel_chart",
        "treemap_chart",
        "heatmap_chart",
        "sankey_chart",
        "candlestick_chart",
        "waterfall_chart",
        "box_plot_chart",
        "map_chart",
    }
)

# Chart types that carry a data field
_DATA_CHART_TYPES = frozenset(
    {
        "line_chart",
        "area_chart",
        "bar_chart",
        "pie_chart",
        "scatter_chart",
        "radar_chart",
        "funnel_chart",
        "treemap_chart",
        "heatmap_chart",
        "sankey_chart",
        "candlestick_chart",
        "waterfall_chart",
        "box_plot_chart",
        "map_chart",
    }
)


class _LintIssue:
    """A single lint finding."""

    __slots__ = ("block_id", "block_type", "level", "message")

    def __init__(
        self,
        level: str,
        message: str,
        block_id: str | None = None,
        block_type: str | None = None,
    ) -> None:
        self.level = level  # error | warning | suggestion | info
        self.message = message
        self.block_id = block_id
        self.block_type = block_type

    _ICONS: ClassVar[dict[str, str]] = {
        "error": "❌",
        "warning": "⚠️ ",
        "suggestion": "💡",
        "info": "✅",
    }
    _COLORS: ClassVar[dict[str, str]] = {
        "error": "red",
        "warning": "yellow",
        "suggestion": "cyan",
        "info": "green",
    }

    def format(self) -> str:
        icon = self._ICONS.get(self.level, "•")
        color = self._COLORS.get(self.level, "white")
        loc = ""
        if self.block_id:
            loc = f" [{self.block_id}]"
        elif self.block_type:
            loc = f" [{self.block_type}]"
        label = click.style(f"{icon} {self.level.upper()}", fg=color)
        return f"  {label}{loc}: {self.message}"


def _collect_blocks_flat(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Recursively flatten all blocks (including children inside sections, columns, tabs).

    Args:
        blocks: List of serialised block dicts.

    Returns:
        Flat list of all block dicts encountered.
    """
    result: list[dict[str, Any]] = []
    for block in blocks:
        result.append(block)
        props = block.get("props", {})
        # Section / Columns children
        children = props.get("children", [])
        if isinstance(children, list):
            result.extend(_collect_blocks_flat(children))
        # Tabs
        tabs = props.get("tabs", [])
        if isinstance(tabs, list):
            for tab in tabs:
                tab_children = tab.get("children", []) if isinstance(tab, dict) else []
                result.extend(_collect_blocks_flat(tab_children))
        # Accordion panels
        panels = props.get("panels", [])
        if isinstance(panels, list):
            for panel in panels:
                panel_children = panel.get("children", []) if isinstance(panel, dict) else []
                result.extend(_collect_blocks_flat(panel_children))
    return result


def _lint_report(spec: dict[str, Any]) -> list[_LintIssue]:
    """Run all lint checks against a report spec dict.

    Args:
        spec: Parsed JSON report spec.

    Returns:
        List of :class:`_LintIssue` findings.
    """
    issues: list[_LintIssue] = []
    top_blocks = spec.get("blocks", [])
    all_blocks = _collect_blocks_flat(top_blocks)

    # --- 1. KPIs without delta ---
    for b in all_blocks:
        if b.get("type") == "kpi":
            props = b.get("props", {})
            if not props.get("delta"):
                issues.append(
                    _LintIssue(
                        "suggestion",
                        "KPI has no delta — consider adding a change indicator for context.",
                        block_id=b.get("id"),
                        block_type="kpi",
                    )
                )

    # --- 2. Sections with >8 children ---
    for b in all_blocks:
        if b.get("type") == "section":
            children = b.get("props", {}).get("children", [])
            if len(children) > 8:
                issues.append(
                    _LintIssue(
                        "suggestion",
                        f"Section has {len(children)} children — consider using Tabs to "
                        f"organise content (recommended max: 8).",
                        block_id=b.get("id"),
                        block_type="section",
                    )
                )

    # --- 3. Charts without titles ---
    for b in all_blocks:
        btype = b.get("type", "")
        if btype in _CHART_TYPES:
            props = b.get("props", {})
            title = props.get("title")
            if not title or (isinstance(title, str) and not title.strip()):
                issues.append(
                    _LintIssue(
                        "warning",
                        f"Chart ({btype}) has no title — add a descriptive title for clarity.",
                        block_id=b.get("id"),
                        block_type=btype,
                    )
                )

    # --- 4. DataTables without explicit columns ---
    for b in all_blocks:
        if b.get("type") == "data_table":
            props = b.get("props", {})
            if not props.get("columns"):
                issues.append(
                    _LintIssue(
                        "info",
                        "DataTable has no explicit columns — columns will be auto-inferred "
                        "from data. Define columns explicitly for stable output.",
                        block_id=b.get("id"),
                        block_type="data_table",
                    )
                )

    # --- 5. Empty data in charts ---
    for b in all_blocks:
        btype = b.get("type", "")
        if btype in _DATA_CHART_TYPES:
            props = b.get("props", {})
            data = props.get("data")
            if data is not None and isinstance(data, list) and len(data) == 0:
                issues.append(
                    _LintIssue(
                        "error",
                        f"Chart ({btype}) has empty data — the chart will render blank.",
                        block_id=b.get("id"),
                        block_type=btype,
                    )
                )

    # --- 6. Missing theme ---
    theme = spec.get("theme")
    if not theme:
        issues.append(
            _LintIssue(
                "info",
                'No theme specified — defaulting to "light". '
                'Set theme explicitly (e.g. "dark", "executive").',
            )
        )

    # --- 7. Duplicate block types in sequence (suggest Columns) ---
    for b in all_blocks:
        btype = b.get("type", "")
        if btype in ("section", "columns", "tabs"):
            children = b.get("props", {}).get("children", [])
            if len(children) >= 2:
                for i in range(len(children) - 1):
                    t1 = children[i].get("type", "")
                    t2 = children[i + 1].get("type", "")
                    if t1 == t2 and t1 not in ("section", "columns", "tabs", "divider"):
                        issues.append(
                            _LintIssue(
                                "suggestion",
                                f"Consecutive {t1} blocks detected — consider wrapping "
                                f"them in a Columns layout for side-by-side display.",
                                block_id=b.get("id"),
                                block_type=btype,
                            )
                        )
                        break  # one suggestion per container

    return issues


def _load_spec_from_source(source: str) -> dict[str, Any]:
    """Load a report spec from a Python script or JSON file.

    For Python scripts, the script is executed via subprocess and its stdout
    is expected to be a JSON spec. If that fails, we look for a recently
    generated ``.json`` file in the script's directory.

    Args:
        source: Path to a ``.py`` or ``.json`` file.

    Returns:
        Parsed spec dict.

    Raises:
        click.ClickException: If loading/parsing fails.
    """
    path = Path(source).resolve()

    if path.suffix == ".json":
        try:
            raw = path.read_text(encoding="utf-8")
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise click.ClickException(f"Invalid JSON in {path.name}: {exc}") from exc

    if path.suffix == ".py":
        # Run the script and attempt to capture a JSON spec
        tmp_json = Path(tempfile.mktemp(suffix=".json", prefix="holysheet_lint_"))
        env = os.environ.copy()
        env["HOLYSHEET_LINT_OUTPUT"] = str(tmp_json)

        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(path.parent),
            env=env,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise click.ClickException(f"Script {path.name} failed:\n{result.stderr.strip()}")

        # Try the lint-output file
        if tmp_json.exists():
            try:
                raw = tmp_json.read_text(encoding="utf-8")
                return json.loads(raw)
            except json.JSONDecodeError:
                pass
            finally:
                tmp_json.unlink(missing_ok=True)

        # Try stdout
        if result.stdout.strip():
            try:
                return json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                pass

        # Fallback: look for a JSON file produced by the script
        json_files = sorted(
            path.parent.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for jf in json_files:
            try:
                raw = jf.read_text(encoding="utf-8")
                data = json.loads(raw)
                if "blocks" in data:
                    return data
            except (json.JSONDecodeError, OSError):
                continue

        raise click.ClickException(
            f"Could not find report output from {path.name}. "
            "Ensure the script exports a JSON spec (via export_json or to stdout)."
        )

    raise click.ClickException(f"Unsupported file type: {path.suffix} (expected .py or .json)")


@cli.command()
@click.argument("source", type=click.Path(exists=True, dir_okay=False))
@click.option("--strict", is_flag=True, help="Treat warnings as errors.")
def lint(source: str, strict: bool) -> None:
    """Lint a HolySheet report for common issues.

    SOURCE is the path to a Python report script or JSON spec file. The
    linter checks for missing deltas, oversized sections, untitled charts,
    empty data, and other patterns that may indicate problems.
    """
    spec = _load_spec_from_source(source)

    click.echo(f"Linting {click.style(Path(source).name, bold=True)}...")
    click.echo()

    issues = _lint_report(spec)

    if not issues:
        click.echo(click.style("  ✅ No issues found — report looks great!", fg="green"))
        raise SystemExit(0)

    # Sort: errors first, then warnings, suggestions, info
    priority = {"error": 0, "warning": 1, "suggestion": 2, "info": 3}
    issues.sort(key=lambda i: priority.get(i.level, 99))

    for issue in issues:
        click.echo(issue.format())

    # Summary
    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue.level] = counts.get(issue.level, 0) + 1

    click.echo()
    parts = []
    for level in ("error", "warning", "suggestion", "info"):
        if level in counts:
            color = _LintIssue._COLORS[level]
            parts.append(click.style(f"{counts[level]} {level}(s)", fg=color))
    click.echo(f"  Found {', '.join(parts)}")

    # Exit code
    has_errors = counts.get("error", 0) > 0
    has_warnings = counts.get("warning", 0) > 0

    if has_errors or (strict and has_warnings):
        raise SystemExit(1)
    raise SystemExit(0)


# ---------------------------------------------------------------------------
# diff — Report Comparison
# ---------------------------------------------------------------------------


def _diff_metadata(spec_a: dict[str, Any], spec_b: dict[str, Any]) -> list[str]:
    """Compare report-level metadata between two specs.

    Args:
        spec_a: First spec dict.
        spec_b: Second spec dict.

    Returns:
        List of human-readable difference descriptions.
    """
    diffs: list[str] = []
    meta_keys = [
        "title",
        "subtitle",
        "theme",
        "logo_url",
        "author",
        "report_version",
        "footer",
        "schema_version",
    ]

    for key in meta_keys:
        val_a = spec_a.get(key)
        val_b = spec_b.get(key)
        if val_a != val_b:
            diffs.append(
                f"  {click.style(key, bold=True)}: "
                f"{click.style(repr(val_a), fg='red')} → "
                f"{click.style(repr(val_b), fg='green')}"
            )
    return diffs


def _block_summary(block: dict[str, Any]) -> str:
    """Generate a short summary string for a block.

    Args:
        block: Serialised block dict.

    Returns:
        Summary string like ``'kpi (block_001) "Revenue"'``.
    """
    btype = block.get("type", "unknown")
    bid = block.get("id", "?")
    props = block.get("props", {})
    title = props.get("title") or props.get("label") or props.get("content", "")
    if isinstance(title, str) and len(title) > 40:
        title = title[:37] + "..."
    if title:
        return f'{btype} ({bid}) "{title}"'
    return f"{btype} ({bid})"


def _diff_blocks(
    blocks_a: list[dict[str, Any]], blocks_b: list[dict[str, Any]]
) -> tuple[list[str], list[str], list[str]]:
    """Compare top-level blocks between two specs.

    Uses block IDs for matching. Reports added, removed, and changed blocks.

    Args:
        blocks_a: Blocks from spec A.
        blocks_b: Blocks from spec B.

    Returns:
        Tuple of (added, removed, changed) description lists.
    """
    index_a = {b.get("id", f"_a_{i}"): b for i, b in enumerate(blocks_a)}
    index_b = {b.get("id", f"_b_{i}"): b for i, b in enumerate(blocks_b)}

    ids_a = set(index_a.keys())
    ids_b = set(index_b.keys())

    added: list[str] = []
    removed: list[str] = []
    changed: list[str] = []

    for bid in sorted(ids_b - ids_a):
        added.append(f"  {click.style('+', fg='green')} {_block_summary(index_b[bid])}")

    for bid in sorted(ids_a - ids_b):
        removed.append(f"  {click.style('-', fg='red')} {_block_summary(index_a[bid])}")

    for bid in sorted(ids_a & ids_b):
        ba = index_a[bid]
        bb = index_b[bid]
        if ba.get("type") != bb.get("type"):
            changed.append(
                f"  {click.style('~', fg='yellow')} {bid}: type "
                f"{click.style(ba.get('type', '?'), fg='red')} → "
                f"{click.style(bb.get('type', '?'), fg='green')}"
            )
        else:
            props_a = ba.get("props", {})
            props_b = bb.get("props", {})
            if props_a != props_b:
                diff_keys = [
                    k
                    for k in set(list(props_a.keys()) + list(props_b.keys()))
                    if props_a.get(k) != props_b.get(k)
                ]
                diff_keys.sort()
                keys_str = ", ".join(diff_keys[:5])
                if len(diff_keys) > 5:
                    keys_str += f" (+{len(diff_keys) - 5} more)"
                changed.append(
                    f"  {click.style('~', fg='yellow')} "
                    f"{_block_summary(ba)}: props changed [{keys_str}]"
                )

    return added, removed, changed


@cli.command()
@click.argument("file_a", type=click.Path(exists=True, dir_okay=False))
@click.argument("file_b", type=click.Path(exists=True, dir_okay=False))
def diff(file_a: str, file_b: str) -> None:
    """Compare two HolySheet JSON spec files.

    FILE_A and FILE_B are paths to JSON report spec files. The command shows
    differences in metadata, added/removed blocks, and changed block props.
    """
    path_a = Path(file_a)
    path_b = Path(file_b)

    try:
        spec_a = json.loads(path_a.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"Invalid JSON in {path_a.name}: {exc}") from exc

    try:
        spec_b = json.loads(path_b.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"Invalid JSON in {path_b.name}: {exc}") from exc

    click.echo(
        f"Comparing {click.style(path_a.name, bold=True)} ↔ {click.style(path_b.name, bold=True)}"
    )
    click.echo()

    has_diffs = False

    # --- Metadata ---
    meta_diffs = _diff_metadata(spec_a, spec_b)
    if meta_diffs:
        has_diffs = True
        click.echo(click.style("Metadata changes:", bold=True))
        for line in meta_diffs:
            click.echo(line)
        click.echo()

    # --- Blocks ---
    blocks_a = spec_a.get("blocks", [])
    blocks_b = spec_b.get("blocks", [])

    added, removed, changed = _diff_blocks(blocks_a, blocks_b)

    if removed:
        has_diffs = True
        click.echo(click.style(f"Removed blocks ({len(removed)}):", fg="red", bold=True))
        for line in removed:
            click.echo(line)
        click.echo()

    if added:
        has_diffs = True
        click.echo(click.style(f"Added blocks ({len(added)}):", fg="green", bold=True))
        for line in added:
            click.echo(line)
        click.echo()

    if changed:
        has_diffs = True
        click.echo(click.style(f"Changed blocks ({len(changed)}):", fg="yellow", bold=True))
        for line in changed:
            click.echo(line)
        click.echo()

    # --- Summary ---
    if not has_diffs:
        click.echo(click.style("  ✓ No differences found", fg="green"))
    else:
        total_a = len(blocks_a)
        total_b = len(blocks_b)
        click.echo(
            f"Summary: {click.style(str(len(removed)), fg='red')} removed, "
            f"{click.style(str(len(added)), fg='green')} added, "
            f"{click.style(str(len(changed)), fg='yellow')} changed "
            f"(A: {total_a} blocks → B: {total_b} blocks)"
        )


# ---------------------------------------------------------------------------
# version
# ---------------------------------------------------------------------------


@cli.command()
def version() -> None:
    """Show the HolySheet version."""
    click.echo(f"holysheet {__version__}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cli()
