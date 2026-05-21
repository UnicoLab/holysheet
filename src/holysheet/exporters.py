"""Export functions for HolySheet reports.

Three export modes are supported:

1. **Standalone HTML** — a single ``.html`` file with CSS, JS, and JSON
   spec embedded inline.
2. **Folder** — a directory with ``index.html``, ``assets/``, and
   ``report.json``.
3. **JSON** — just the raw JSON spec file.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import jinja2
from loguru import logger

from holysheet.exceptions import ExportError, RendererAssetError

if TYPE_CHECKING:
    from holysheet.schema import ReportSchema

# ---------------------------------------------------------------------------
# Renderer asset paths
# ---------------------------------------------------------------------------

_PACKAGE_DIR = Path(__file__).resolve().parent
_RENDERER_DIR = _PACKAGE_DIR / "renderer"
_ASSETS_DIR = _RENDERER_DIR / "assets"
_TEMPLATE_DIR = _PACKAGE_DIR / "templates"


def _read_asset(filename: str) -> str:
    """Read a renderer asset file and return its contents.

    Args:
        filename: Asset file name inside ``renderer/assets/``.

    Returns:
        File contents as a string.

    Raises:
        RendererAssetError: If the asset file does not exist.
    """
    asset_path = _ASSETS_DIR / filename
    if not asset_path.exists():
        raise RendererAssetError(
            f"Renderer asset not found: {asset_path}. "
            "Run 'make frontend-build' to generate the frontend bundle.",
            asset_path=str(asset_path),
        )
    return asset_path.read_text(encoding="utf-8")


def _get_template() -> jinja2.Template:
    """Load the standalone HTML Jinja2 template.

    Returns:
        Compiled Jinja2 :class:`~jinja2.Template`.

    Raises:
        ExportError: If the template file is missing.
    """
    template_path = _TEMPLATE_DIR / "standalone.html.j2"
    if not template_path.exists():
        raise ExportError(
            f"Template not found: {template_path}",
            path=str(template_path),
        )
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(_TEMPLATE_DIR)),
        autoescape=False,  # We control the content; no HTML escaping needed
    )
    return env.get_template("standalone.html.j2")


# ---------------------------------------------------------------------------
# Public export functions
# ---------------------------------------------------------------------------


def export_standalone_html(schema: ReportSchema, output_path: str | Path) -> Path:
    """Export a report as a single self-contained HTML file.

    The HTML file embeds all CSS, JavaScript, and the report JSON spec
    inline so it can be opened directly in a browser with no server.

    Args:
        schema: The report schema to export.
        output_path: Destination file path (e.g. ``"report.html"``).

    Returns:
        Resolved :class:`~pathlib.Path` of the written file.

    Raises:
        RendererAssetError: If renderer JS/CSS assets are missing.
        ExportError: If writing the file fails.
    """
    output_path = Path(output_path).resolve()
    logger.info("Exporting standalone HTML to {}", output_path)

    try:
        css_content = _read_asset("app.css")
        js_content = _read_asset("app.js")
        json_spec = schema.to_json(pretty=False)

        template = _get_template()
        html = template.render(
            title=schema.title,
            css_content=css_content,
            js_content=js_content,
            json_spec=json_spec,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        logger.info("Standalone HTML written ({:,} bytes)", len(html))
        return output_path

    except (RendererAssetError, ExportError):
        raise
    except Exception as exc:
        raise ExportError(
            f"Failed to export standalone HTML: {exc}",
            path=str(output_path),
        ) from exc


def export_folder(schema: ReportSchema, output_dir: str | Path) -> Path:
    """Export a report as a folder with ``index.html``, assets, and JSON.

    The folder structure is::

        output_dir/
        ├── index.html
        ├── report.json
        └── assets/
            ├── app.js
            └── app.css

    Args:
        schema: The report schema to export.
        output_dir: Target directory path.

    Returns:
        Resolved :class:`~pathlib.Path` of the output directory.

    Raises:
        RendererAssetError: If renderer assets are missing.
        ExportError: If creating the folder or writing files fails.
    """
    output_dir = Path(output_dir).resolve()
    logger.info("Exporting folder to {}", output_dir)

    try:
        # Validate assets exist
        if not _ASSETS_DIR.exists():
            raise RendererAssetError(
                f"Renderer assets directory not found: {_ASSETS_DIR}. "
                "Run 'make frontend-build' to generate the frontend bundle.",
                asset_path=str(_ASSETS_DIR),
            )

        # Create directory structure
        output_dir.mkdir(parents=True, exist_ok=True)
        assets_out = output_dir / "assets"
        assets_out.mkdir(exist_ok=True)

        # Copy renderer files
        renderer_index = _RENDERER_DIR / "index.html"
        if renderer_index.exists():
            shutil.copy2(renderer_index, output_dir / "index.html")
        else:
            # Generate a minimal index.html that loads assets and spec
            index_html = _generate_folder_index(schema.title)
            (output_dir / "index.html").write_text(index_html, encoding="utf-8")

        # Copy assets
        for asset_file in _ASSETS_DIR.iterdir():
            if asset_file.is_file():
                shutil.copy2(asset_file, assets_out / asset_file.name)

        # Write the JSON spec
        json_path = output_dir / "report.json"
        json_path.write_bytes(schema.to_json_bytes())

        # Also write a loader script that sets window.__HOLYSHEET_SPEC__
        _write_spec_loader(output_dir, schema)

        logger.info("Folder export complete: {}", output_dir)
        return output_dir

    except (RendererAssetError, ExportError):
        raise
    except Exception as exc:
        raise ExportError(
            f"Failed to export folder: {exc}",
            path=str(output_dir),
        ) from exc


def export_json(schema: ReportSchema, output_path: str | Path) -> Path:
    """Export only the JSON spec file.

    Args:
        schema: The report schema to export.
        output_path: Destination file path (e.g. ``"report.json"``).

    Returns:
        Resolved :class:`~pathlib.Path` of the written file.

    Raises:
        ExportError: If writing the file fails.
    """
    output_path = Path(output_path).resolve()
    logger.info("Exporting JSON to {}", output_path)

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        json_bytes = schema.to_json_bytes()
        output_path.write_bytes(json_bytes)
        logger.info("JSON written ({:,} bytes)", len(json_bytes))
        return output_path

    except Exception as exc:
        raise ExportError(
            f"Failed to export JSON: {exc}",
            path=str(output_path),
        ) from exc


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _generate_folder_index(title: str) -> str:
    """Generate a minimal ``index.html`` for folder exports.

    Args:
        title: Page title.

    Returns:
        HTML string.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="stylesheet" href="assets/app.css" />
</head>
<body>
    <div id="root"></div>
    <script src="spec-loader.js"></script>
    <script src="assets/app.js"></script>
</body>
</html>"""


def _write_spec_loader(output_dir: Path, schema: ReportSchema) -> None:
    """Write a ``spec-loader.js`` that sets ``window.__HOLYSHEET_SPEC__``.

    For folder exports we fetch ``report.json`` synchronously so the spec
    is available before the app bundle runs.

    Args:
        output_dir: Target directory.
        schema: The report schema (used for inline fallback).
    """
    loader_js = (
        "// HolySheet spec loader — auto-generated\n"
        "(function() {\n"
        "    var xhr = new XMLHttpRequest();\n"
        '    xhr.open("GET", "report.json", false);\n'  # synchronous
        "    xhr.send();\n"
        "    if (xhr.status === 200) {\n"
        "        window.__HOLYSHEET_SPEC__ = JSON.parse(xhr.responseText);\n"
        "    } else {\n"
        '        console.error("Failed to load report.json:", xhr.status);\n'
        "    }\n"
        "})();\n"
    )
    (output_dir / "spec-loader.js").write_text(loader_js, encoding="utf-8")
