"""Main :class:`Report` class for composing HolySheet dashboards.

Example::

    from holysheet import Report, KPI, LineChart

    report = Report(title="Q4 Summary", theme="dark")
    report.add(KPI(label="Revenue", value="$1.2M", delta="+12.3%", status="positive"))
    report.add(LineChart(title="Trend", data=df, x="date", y="revenue"))
    report.export_html("report.html")
"""

from __future__ import annotations

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
        theme: Theme name (``'light'``, ``'dark'``, or ``'executive'``).
        logo_url: Optional URL for a logo image.
        author: Optional report author name.
        report_version: Optional report version string.
        footer: Optional custom footer text.
    """

    def __init__(
        self,
        title: str = "Untitled Report",
        subtitle: str | None = None,
        theme: str = "light",
        logo_url: str | None = None,
        author: str | None = None,
        report_version: str | None = None,
        footer: str | None = None,
    ) -> None:
        validate_theme(theme)
        self.title = title
        self.subtitle = subtitle
        self.theme = theme
        self.logo_url = logo_url
        self.author = author
        self.report_version = report_version
        self.footer = footer
        self._blocks: list[Block] = []
        self._counter: int = 0

        logger.debug("Report created: title={!r}, theme={!r}", title, theme)

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

    def to_schema(self) -> ReportSchema:
        """Build a :class:`~holysheet.schema.ReportSchema` from this report.

        Returns:
            A fully populated schema instance.
        """
        serialised_blocks = self._serialise_blocks()
        return ReportSchema(
            title=self.title,
            subtitle=self.subtitle,
            theme=self.theme,
            logo_url=self.logo_url,
            author=self.author,
            report_version=self.report_version,
            footer=self.footer,
            blocks=serialised_blocks,
        )

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
        return export_standalone_html(schema, path)

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

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Report(title={self.title!r}, theme={self.theme!r}, blocks={len(self._blocks)})"
