"""Main :class:`Report` class for composing HolySheet dashboards.

Example::

    from holysheet import Report, KPI, LineChart

    report = Report(title="Q4 Summary", theme="dark")
    report.add(KPI(label="Revenue", value="$1.2M", delta="+12.3%", status="positive"))
    report.add(LineChart(title="Trend", data=df, x="date", y="revenue"))
    report.export_html("report.html")
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from loguru import logger

from holysheet.blocks import Block, Columns, Section, Tabs
from holysheet.exporters import export_folder, export_json, export_standalone_html
from holysheet.schema import ReportSchema
from holysheet.themes import validate_theme


class Report:
    """A composable report that holds blocks and can be exported.

    Block IDs are generated sequentially per instance (``block_001``,
    ``block_002``, …) for deterministic, stable output.

    Args:
        title: Report title.
        subtitle: Optional subtitle.
        theme: Theme name (``'light'``, ``'dark'``, or ``'executive'``)
               or a custom :class:`~holysheet.themes.Theme` instance.
        logo_url: Optional URL for a logo image.
        author: Optional report author name.
        report_version: Optional report version string.
        footer: Optional custom footer text.
        theme_switch: Allow viewers to toggle dark/light mode.
        presentation_mode: Enable presentation (slideshow) mode.
        download_buttons: Show CSV download buttons on tables/charts.
        password: Password-protect the exported HTML (client-side AES).
        expires: ISO-8601 date string after which the report shows expired.
        compress: Gzip-compress the embedded JSON data.
    """

    def __init__(
        self,
        title: str = "Untitled Report",
        subtitle: str | None = None,
        theme: str | Any = "light",
        logo_url: str | None = None,
        author: str | None = None,
        report_version: str | None = None,
        footer: str | None = None,
        # ── Feature flags ────────────────────────────────
        theme_switch: bool = False,
        presentation_mode: bool = False,
        download_buttons: bool = False,
        password: str | None = None,
        expires: str | None = None,
        compress: bool = False,
    ) -> None:
        # Handle custom Theme objects
        from holysheet.themes import Theme

        self._custom_theme: dict[str, Any] | None = None
        if isinstance(theme, Theme):
            self._custom_theme = theme.to_dict()
            theme_name = theme.name
        else:
            validate_theme(theme)
            theme_name = theme

        self.title = title
        self.subtitle = subtitle
        self.theme = theme_name
        self.logo_url = logo_url
        self.author = author
        self.report_version = report_version
        self.footer = footer
        self._blocks: list[Block] = []
        self._pages: list[dict[str, Any]] = []
        self._counter: int = 0

        # Feature flags
        self._features: dict[str, Any] = {
            "theme_switch": theme_switch,
            "presentation_mode": presentation_mode,
            "download_buttons": download_buttons,
        }
        self._password = password
        self._expires = expires
        self._compress = compress

        logger.debug("Report created: title={!r}, theme={!r}", title, theme_name)

    # ------------------------------------------------------------------
    # Block management
    # ------------------------------------------------------------------

    def add(self, block: Block) -> Report:
        """Append a block to the report.

        Args:
            block: Any :class:`~holysheet.blocks.Block` subclass instance.

        Returns:
            ``self`` for method chaining.
        """
        self._blocks.append(block)
        logger.debug("Added {} block (total: {})", block.type, len(self._blocks))
        return self

    @property
    def blocks(self) -> list[Block]:
        """Read-only view of the current block list.

        Returns:
            List of block instances.
        """
        return list(self._blocks)

    def __len__(self) -> int:
        return len(self._blocks)

    # ------------------------------------------------------------------
    # Multi-page support
    # ------------------------------------------------------------------

    def add_page(self, label: str, children: list[Block] | None = None) -> Report:
        """Add a named page to the report.

        When pages are used, the report renders with a sidebar/tab navigation.

        Args:
            label: Page label for navigation.
            children: List of blocks for this page.

        Returns:
            ``self`` for method chaining.
        """
        self._pages.append(
            {
                "label": label,
                "children": children or [],
            }
        )
        logger.debug("Added page {!r} (total: {})", label, len(self._pages))
        return self

    # ------------------------------------------------------------------
    # Global filters
    # ------------------------------------------------------------------

    def add_filter(
        self,
        key: str,
        *,
        type: str = "dropdown",  # noqa: A002
        label: str | None = None,
        options: list[Any] | None = None,
        default: Any = None,
    ) -> Report:
        """Add a global filter to the report header.

        Filters affect all blocks that reference the same ``key``.

        Args:
            key: Filter identifier used in block ``filters`` prop.
            type: Filter type: ``'dropdown'``, ``'date_range'``, ``'text'``.
            label: Display label.
            options: Available options for dropdown type.
            default: Default selected value.

        Returns:
            ``self`` for method chaining.
        """
        if "filters" not in self._features:
            self._features["filters"] = []
        self._features["filters"].append(
            {
                "key": key,
                "type": type,
                "label": label or key.replace("_", " ").title(),
                "options": options or [],
                "default": default,
            }
        )
        return self

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def _count_children(self, block: Block) -> int:
        """Recursively count how many child IDs a block will consume.

        Args:
            block: A block instance.

        Returns:
            Total child count (not counting the block itself).
        """
        if isinstance(block, Section):
            total = len(block.children)
            for child in block.children:
                total += self._count_children(child)
            return total
        if isinstance(block, Columns):
            total = len(block.children)
            for child in block.children:
                total += self._count_children(child)
            return total
        if isinstance(block, Tabs):
            total = 0
            for tab in block.tabs:
                children = tab.get("children", [])
                total += len(children)
                for child in children:
                    if isinstance(child, Block):
                        total += self._count_children(child)
            return total
        return 0

    def _serialise_blocks(self) -> list[dict[str, Any]]:
        """Serialise all blocks, assigning sequential IDs.

        Returns:
            List of serialised block dicts.
        """
        serialised: list[dict[str, Any]] = []
        counter = 0

        for block in self._blocks:
            counter += 1
            block_id = f"block_{counter:03d}"

            if isinstance(block, (Section, Columns, Tabs)):
                child_count = self._count_children(block)
                serialised.append(block.serialize(block_id, counter=counter))
                counter += child_count
            else:
                serialised.append(block.serialize(block_id))

        return serialised

    def _serialise_pages(self) -> list[dict[str, Any]]:
        """Serialise pages and their child blocks."""
        pages: list[dict[str, Any]] = []
        counter = 0

        for page in self._pages:
            page_blocks: list[dict[str, Any]] = []
            for block in page.get("children", []):
                counter += 1
                block_id = f"block_{counter:03d}"
                if isinstance(block, (Section, Columns, Tabs)):
                    child_count = self._count_children(block)
                    page_blocks.append(block.serialize(block_id, counter=counter))
                    counter += child_count
                else:
                    page_blocks.append(block.serialize(block_id))

            pages.append(
                {
                    "label": page["label"],
                    "blocks": page_blocks,
                }
            )

        return pages

    def to_schema(self) -> ReportSchema:
        """Build a :class:`~holysheet.schema.ReportSchema` from this report.

        Returns:
            A fully populated schema instance.
        """
        if self._pages:
            serialised_blocks = self._serialise_pages()
            self._features["multi_page"] = True
        else:
            serialised_blocks = self._serialise_blocks()

        schema_kwargs: dict[str, Any] = {
            "title": self.title,
            "subtitle": self.subtitle,
            "theme": self.theme,
            "logo_url": self.logo_url,
            "author": self.author,
            "report_version": self.report_version,
            "footer": self.footer,
            "blocks": serialised_blocks,
            "features": self._features if any(v for v in self._features.values()) else None,
        }

        if self._custom_theme:
            schema_kwargs["custom_theme"] = self._custom_theme

        if self._expires:
            schema_kwargs["expires"] = self._expires

        return ReportSchema(**schema_kwargs)

    def to_json(self, *, pretty: bool = False) -> str:
        """Serialise the report to a JSON string.

        Args:
            pretty: If ``True``, indent the JSON for readability.

        Returns:
            JSON string.
        """
        return self.to_schema().to_json(pretty=pretty)

    # ------------------------------------------------------------------
    # Export shortcuts
    # ------------------------------------------------------------------

    def export_html(self, path: str | Path) -> Path:
        """Export as a standalone HTML file.

        Args:
            path: Output file path.

        Returns:
            Resolved path of the written file.
        """
        schema = self.to_schema()
        result = export_standalone_html(
            schema,
            path,
            password=self._password,
            compress=self._compress,
        )
        return result

    def export_folder(self, path: str | Path) -> Path:
        """Export as a folder with index.html, assets, and report.json.

        Args:
            path: Output directory path.

        Returns:
            Resolved path of the output directory.
        """
        schema = self.to_schema()
        return export_folder(schema, path)

    def export_json(self, path: str | Path) -> Path:
        """Export just the JSON spec file.

        Args:
            path: Output file path.

        Returns:
            Resolved path of the written file.
        """
        schema = self.to_schema()
        return export_json(schema, path)

    def export_widget(
        self,
        path: str | Path,
        block_ids: list[str] | None = None,
    ) -> Path:
        """Export a lightweight embeddable widget with a subset of blocks.

        Args:
            path: Output HTML file path.
            block_ids: Optional list of block IDs to include. If None,
                       includes all blocks.

        Returns:
            Resolved path of the written file.
        """
        schema = self.to_schema()
        if block_ids:
            schema.blocks = [b for b in schema.blocks if b.get("id") in block_ids]
        schema.features = schema.features or {}
        schema.features["widget_mode"] = True
        return export_standalone_html(schema, path)

    # ------------------------------------------------------------------
    # Jupyter integration
    # ------------------------------------------------------------------

    def _repr_html_(self) -> str:
        """Render the report inline in Jupyter / IPython notebooks.

        Returns:
            HTML string for notebook display.
        """
        schema = self.to_schema()
        from holysheet.exporters import _get_template, _read_asset

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
            # Wrap in an iframe for isolation in notebooks
            import base64
            import html as html_lib

            encoded = base64.b64encode(html.encode("utf-8")).decode("utf-8")
            return (
                f'<iframe srcdoc="" style="width:100%;height:800px;border:none;" '
                f"onload=\"this.srcdoc=atob('{encoded}')\"></iframe>"
            )
        except Exception as exc:
            return f"<pre>HolySheet render error: {html_lib.escape(str(exc))}</pre>"

    def show(self, height: int = 800) -> Any:
        """Display the report in a Jupyter notebook.

        Args:
            height: iframe height in pixels.

        Returns:
            IPython HTML display object.
        """
        try:
            from IPython.display import HTML

            return HTML(self._repr_html_())
        except ImportError:
            logger.warning("IPython not available. Use export_html() instead.")
            return None

    # ------------------------------------------------------------------
    # PDF export
    # ------------------------------------------------------------------

    def export_pdf(
        self,
        path: str | Path,
        *,
        width: str = "A4",
        landscape: bool = False,
        margin: str = "1cm",
    ) -> Path:
        """Export the report as a PDF file.

        Requires ``playwright`` to be installed::

            pip install playwright && playwright install chromium

        Args:
            path: Output PDF file path.
            width: Paper format (``A4``, ``Letter``, etc.).
            landscape: Landscape orientation.
            margin: Page margins (e.g. ``1cm``, ``0.5in``).

        Returns:
            Resolved path to the generated PDF.

        Raises:
            RuntimeError: If no headless browser is available.
        """
        import subprocess
        import tempfile

        out_path = Path(path).resolve()

        # Generate HTML to a temp file first
        tmp_html = Path(tempfile.mktemp(suffix=".html", prefix="holysheet_pdf_"))
        try:
            self.export_html(tmp_html)

            # Try Playwright first
            try:
                import playwright  # noqa: F401

                cmd = [
                    sys.executable,
                    "-c",
                    (
                        "from playwright.sync_api import sync_playwright; "
                        "p = sync_playwright().start(); "
                        f"b = p.chromium.launch(); pg = b.new_page(); "
                        f"pg.goto('file://{tmp_html}'); "
                        f"pg.pdf(path='{out_path}', "
                        f"format='{width}', "
                        f"landscape={landscape}, "
                        f"margin={{'top': '{margin}', 'right': '{margin}', "
                        f"'bottom': '{margin}', 'left': '{margin}'}}); "
                        "b.close(); p.stop()"
                    ),
                ]
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                logger.info("PDF exported via Playwright → {}", out_path)
                return out_path
            except ImportError:
                pass

            # Fallback: headless Chrome
            chrome_candidates = [
                "google-chrome",
                "chromium-browser",
                "chromium",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            ]
            for chrome in chrome_candidates:
                try:
                    subprocess.run(
                        [
                            chrome,
                            "--headless",
                            "--disable-gpu",
                            f"--print-to-pdf={out_path}",
                            "--print-to-pdf-no-header",
                            str(tmp_html),
                        ],
                        check=True,
                        capture_output=True,
                    )
                    logger.info("PDF exported via Chrome → {}", out_path)
                    return out_path
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue

            msg = (
                "PDF export requires a headless browser.\n"
                "Install Playwright:  pip install playwright && playwright install chromium\n"
                "Or install Chrome/Chromium system-wide."
            )
            raise RuntimeError(msg)
        finally:
            tmp_html.unlink(missing_ok=True)

    # ------------------------------------------------------------------
    # Auto-narration
    # ------------------------------------------------------------------

    def auto_narrate(self) -> str:
        """Generate narration text from KPIs and chart titles.

        Creates a human-readable summary of all KPI values and chart titles
        in the report — useful for accessibility or voice readback.

        Returns:
            Plain text narration string.
        """
        from holysheet.blocks import KPI

        parts: list[str] = [f"Report: {self.title}."]
        blocks = self._blocks
        if self._pages:
            for page in self._pages:
                blocks = [*blocks, *page.get("blocks", [])]

        for block in blocks:
            if isinstance(block, KPI):
                part = f"{block.label} is {block.value}"
                if block.unit:
                    part += f" {block.unit}"
                if block.delta:
                    part += f", with a change of {block.delta}"
                parts.append(part + ".")
            elif hasattr(block, "title") and block.title:
                parts.append(f"{block.title}.")

        return " ".join(parts)

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        if self._pages:
            return f"Report(title={self.title!r}, theme={self.theme!r}, pages={len(self._pages)})"
        return f"Report(title={self.title!r}, theme={self.theme!r}, blocks={len(self._blocks)})"
