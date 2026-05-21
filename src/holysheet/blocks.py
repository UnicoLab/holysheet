"""Pydantic v2 block models for HolySheet reports.

Each block type produces a serialised representation that the React renderer
understands.  Block IDs are auto-generated per report instance using a
counter injected at serialisation time (see :class:`~holysheet.report.Report`).

Discriminated unions are used so the ``type`` literal field selects the
correct model during (de)serialisation.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field

from holysheet.data import to_records

# ---------------------------------------------------------------------------
# Base block
# ---------------------------------------------------------------------------


class Block(BaseModel):
    """Abstract base for all report blocks.

    Attributes:
        type: Discriminator literal set by each subclass.
    """

    type: str

    def to_props(self) -> dict[str, Any]:
        """Return a dict of props for the React renderer.

        Subclasses override this to produce the specific payload expected by
        the corresponding React component.

        Returns:
            Dict of component props.
        """
        return {}

    def serialize(self, block_id: str) -> dict[str, Any]:
        """Serialise the block into the schema-level dict.

        Args:
            block_id: Pre-assigned block ID (e.g. ``'block_001'``).

        Returns:
            Full block dict including ``id``, ``type``, and ``props``.
        """
        return {
            "id": block_id,
            "type": self.type,
            "props": self.to_props(),
        }


# ---------------------------------------------------------------------------
# KPI & Metric blocks
# ---------------------------------------------------------------------------


class KPI(Block):
    """Key Performance Indicator card.

    Attributes:
        label: Display label (e.g. "Total Revenue").
        value: The main metric value.
        unit: Optional unit suffix (e.g. "$", "%").
        delta: Optional change indicator (e.g. "+12.3%").
        status: Semantic status: ``'positive'``, ``'negative'``, or ``'neutral'``.
        description: Optional helper text below the value.
        tooltip_detail: Optional rich tooltip with breakdown items.
    """

    type: Literal["kpi"] = "kpi"
    label: str
    value: str | int | float
    unit: str | None = None
    delta: str | None = None
    status: Literal["positive", "negative", "neutral"] | None = None
    description: str | None = None
    tooltip_detail: dict[str, Any] | None = None

    def to_props(self) -> dict[str, Any]:
        """Return KPI props dict."""
        props: dict[str, Any] = {
            "label": self.label,
            "value": self.value,
            "unit": self.unit,
            "delta": self.delta,
            "status": self.status,
            "description": self.description,
        }
        if self.tooltip_detail:
            props["tooltip_detail"] = self.tooltip_detail
        return props


class Metric(Block):
    """Compact inline metric display.

    A lightweight alternative to KPI for dense metric grids.

    Attributes:
        label: Metric label.
        value: The metric value.
        unit: Optional unit suffix.
        icon: Optional icon name hint.
    """

    type: Literal["metric"] = "metric"
    label: str
    value: str | int | float
    unit: str | None = None
    icon: str | None = None

    def to_props(self) -> dict[str, Any]:
        """Return metric props dict."""
        return {
            "label": self.label,
            "value": self.value,
            "unit": self.unit,
            "icon": self.icon,
        }


# ---------------------------------------------------------------------------
# Chart blocks
# ---------------------------------------------------------------------------


class LineChart(Block):
    """Line chart block.

    Attributes:
        title: Chart title.
        data: Raw tabular data (converted via :func:`to_records` on serialisation).
        x: Column name for X axis.
        y: Column name(s) for Y axis.
        series: Optional grouping column for multi-series.
        height: Chart height in pixels.
        annotations: Optional list of annotation markers on the chart.
        downloadable: If ``True``, show a CSV download button.
    """

    type: Literal["line_chart"] = "line_chart"
    title: str
    data: Any = None
    x: str | None = None
    y: str | list[str] | None = None
    series: list[str] | None = None
    height: int = 360
    annotations: list[dict[str, Any]] | None = None
    downloadable: bool = False

    def to_props(self) -> dict[str, Any]:
        """Return line chart props with data converted to records."""
        props: dict[str, Any] = {
            "title": self.title,
            "data": to_records(self.data),
            "x": self.x,
            "y": self.y,
            "series": self.series,
            "height": self.height,
        }
        if self.annotations:
            props["annotations"] = self.annotations
        if self.downloadable:
            props["downloadable"] = True
        return props


class AreaChart(Block):
    """Area chart block (filled line chart).

    Attributes:
        title: Chart title.
        data: Raw tabular data.
        x: Column name for X axis.
        y: Column name(s) for Y axis.
        series: Optional grouping column for multi-series.
        height: Chart height in pixels.
        annotations: Optional list of annotation markers.
        downloadable: If ``True``, show a CSV download button.
    """

    type: Literal["area_chart"] = "area_chart"
    title: str
    data: Any = None
    x: str | None = None
    y: str | list[str] | None = None
    series: list[str] | None = None
    height: int = 360
    annotations: list[dict[str, Any]] | None = None
    downloadable: bool = False

    def to_props(self) -> dict[str, Any]:
        """Return area chart props with data converted to records."""
        props: dict[str, Any] = {
            "title": self.title,
            "data": to_records(self.data),
            "x": self.x,
            "y": self.y,
            "series": self.series,
            "height": self.height,
        }
        if self.annotations:
            props["annotations"] = self.annotations
        if self.downloadable:
            props["downloadable"] = True
        return props


class BarChart(Block):
    """Bar chart block.

    Attributes:
        title: Chart title.
        data: Raw tabular data.
        x: Column name for X axis (categories).
        y: Column name(s) for Y axis (values).
        series: Optional grouping column for multi-series.
        height: Chart height in pixels.
    """

    type: Literal["bar_chart"] = "bar_chart"
    title: str
    data: Any = None
    x: str | None = None
    y: str | list[str] | None = None
    series: list[str] | None = None
    height: int = 360
    annotations: list[dict[str, Any]] | None = None
    downloadable: bool = False

    def to_props(self) -> dict[str, Any]:
        """Return bar chart props with data converted to records."""
        props: dict[str, Any] = {
            "title": self.title,
            "data": to_records(self.data),
            "x": self.x,
            "y": self.y,
            "series": self.series,
            "height": self.height,
        }
        if self.annotations:
            props["annotations"] = self.annotations
        if self.downloadable:
            props["downloadable"] = True
        return props


class PieChart(Block):
    """Pie/donut chart block.

    Attributes:
        title: Chart title.
        data: Raw tabular data.
        name: Column name for slice labels.
        value: Column name for slice values.
        height: Chart height in pixels.
    """

    type: Literal["pie_chart"] = "pie_chart"
    title: str
    data: Any = None
    name: str | None = None
    value: str | None = None
    height: int = 360

    def to_props(self) -> dict[str, Any]:
        """Return pie chart props with data converted to records."""
        return {
            "title": self.title,
            "data": to_records(self.data),
            "name": self.name,
            "value": self.value,
            "height": self.height,
        }


class ScatterChart(Block):
    """Scatter plot block.

    Attributes:
        title: Chart title.
        data: Raw tabular data.
        x: Column name for X axis.
        y: Column name for Y axis.
        size: Optional column for bubble size.
        category: Optional column for point categorisation.
        height: Chart height in pixels.
    """

    type: Literal["scatter_chart"] = "scatter_chart"
    title: str
    data: Any = None
    x: str | None = None
    y: str | None = None
    size: str | None = None
    category: str | None = None
    height: int = 360
    annotations: list[dict[str, Any]] | None = None
    downloadable: bool = False

    def to_props(self) -> dict[str, Any]:
        """Return scatter chart props with data converted to records."""
        props: dict[str, Any] = {
            "title": self.title,
            "data": to_records(self.data),
            "x": self.x,
            "y": self.y,
            "size": self.size,
            "category": self.category,
            "height": self.height,
        }
        if self.annotations:
            props["annotations"] = self.annotations
        if self.downloadable:
            props["downloadable"] = True
        return props


class RadarChart(Block):
    """Radar/spider chart block.

    Attributes:
        title: Chart title.
        data: Raw tabular data where each record is one series.
        indicators: List of dimension names to display on axes.
        height: Chart height in pixels.
    """

    type: Literal["radar_chart"] = "radar_chart"
    title: str
    data: Any = None
    indicators: list[str] = Field(default_factory=list)
    height: int = 360

    def to_props(self) -> dict[str, Any]:
        """Return radar chart props with data converted to records."""
        return {
            "title": self.title,
            "data": to_records(self.data),
            "indicators": self.indicators,
            "height": self.height,
        }


class GaugeChart(Block):
    """Gauge/speedometer block for single-value visualisation.

    Attributes:
        title: Chart title.
        value: Current value to display.
        min: Minimum scale value.
        max: Maximum scale value.
        unit: Optional unit label.
        thresholds: Optional list of ``{value, color}`` dicts for color stops.
        height: Chart height in pixels.
    """

    type: Literal["gauge"] = "gauge"
    title: str
    value: int | float = 0
    min: int | float = 0
    max: int | float = 100
    unit: str | None = None
    thresholds: list[dict[str, Any]] | None = None
    height: int = 300

    def to_props(self) -> dict[str, Any]:
        """Return gauge props."""
        return {
            "title": self.title,
            "value": self.value,
            "min": self.min,
            "max": self.max,
            "unit": self.unit,
            "thresholds": self.thresholds,
            "height": self.height,
        }


class FunnelChart(Block):
    """Funnel chart block for conversion/pipeline visualisation.

    Attributes:
        title: Chart title.
        data: Raw tabular data.
        name: Column name for stage labels.
        value: Column name for stage values.
        height: Chart height in pixels.
    """

    type: Literal["funnel_chart"] = "funnel_chart"
    title: str
    data: Any = None
    name: str | None = None
    value: str | None = None
    height: int = 360

    def to_props(self) -> dict[str, Any]:
        """Return funnel chart props with data converted to records."""
        return {
            "title": self.title,
            "data": to_records(self.data),
            "name": self.name,
            "value": self.value,
            "height": self.height,
        }


class TreemapChart(Block):
    """Treemap chart block for hierarchical data visualisation.

    Attributes:
        title: Chart title.
        data: Raw tabular data.
        name: Column name for node labels.
        value: Column name for node sizes.
        category: Optional column for grouping.
        height: Chart height in pixels.
    """

    type: Literal["treemap_chart"] = "treemap_chart"
    title: str
    data: Any = None
    name: str | None = None
    value: str | None = None
    category: str | None = None
    height: int = 360

    def to_props(self) -> dict[str, Any]:
        """Return treemap chart props with data converted to records."""
        return {
            "title": self.title,
            "data": to_records(self.data),
            "name": self.name,
            "value": self.value,
            "category": self.category,
            "height": self.height,
        }


# ---------------------------------------------------------------------------
# Data blocks
# ---------------------------------------------------------------------------


class DataTable(Block):
    """Interactive data table block.

    Attributes:
        title: Table title.
        data: Raw tabular data.
        columns: Optional explicit column definitions.
        searchable: Whether the table supports text search.
        paginated: Whether the table is paginated.
        formatting: Conditional formatting rules per column.
        downloadable: If ``True``, show a CSV download button.
    """

    type: Literal["data_table"] = "data_table"
    title: str
    data: Any = None
    columns: list[str] | None = None
    searchable: bool = True
    paginated: bool = True
    formatting: dict[str, dict[str, Any]] | None = None
    downloadable: bool = False

    def to_props(self) -> dict[str, Any]:
        """Return data table props with data converted to records."""
        records = to_records(self.data)
        cols = self.columns
        if cols is None and records:
            cols = list(records[0].keys())
        props: dict[str, Any] = {
            "title": self.title,
            "data": records,
            "columns": cols,
            "searchable": self.searchable,
            "paginated": self.paginated,
        }
        if self.formatting:
            props["formatting"] = self.formatting
        if self.downloadable:
            props["downloadable"] = True
        return props


# ---------------------------------------------------------------------------
# Content blocks
# ---------------------------------------------------------------------------


class Markdown(Block):
    """Free-form Markdown content block.

    Attributes:
        content: Markdown-formatted string.
    """

    type: Literal["markdown"] = "markdown"
    content: str

    def to_props(self) -> dict[str, Any]:
        """Return markdown props."""
        return {"content": self.content}


class CodeBlock(Block):
    """Syntax-highlighted code display block.

    Attributes:
        code: The source code string.
        language: Programming language for highlighting hints.
        title: Optional title above the code block.
    """

    type: Literal["code_block"] = "code_block"
    code: str
    language: str | None = None
    title: str | None = None

    def to_props(self) -> dict[str, Any]:
        """Return code block props."""
        return {
            "code": self.code,
            "language": self.language,
            "title": self.title,
        }


class Image(Block):
    """Image display block.

    Attributes:
        src: Image URL or data URI.
        alt: Accessibility alt text.
        caption: Optional caption below the image.
        width: Optional width (CSS value or number in pixels).
        height: Optional height (CSS value or number in pixels).
    """

    type: Literal["image"] = "image"
    src: str
    alt: str | None = None
    caption: str | None = None
    width: str | int | None = None
    height: str | int | None = None

    def to_props(self) -> dict[str, Any]:
        """Return image props."""
        return {
            "src": self.src,
            "alt": self.alt,
            "caption": self.caption,
            "width": self.width,
            "height": self.height,
        }


class Alert(Block):
    """Alert/callout block.

    Attributes:
        severity: Alert level: ``'info'``, ``'warning'``, ``'error'``, or ``'success'``.
        title: Optional alert title.
        message: Alert message body.
    """

    type: Literal["alert"] = "alert"
    severity: Literal["info", "warning", "error", "success"] = "info"
    title: str | None = None
    message: str = ""

    def to_props(self) -> dict[str, Any]:
        """Return alert props."""
        return {
            "severity": self.severity,
            "title": self.title,
            "message": self.message,
        }


# ---------------------------------------------------------------------------
# Progress & Gauge UI blocks
# ---------------------------------------------------------------------------


class ProgressBar(Block):
    """Progress indicator block.

    Attributes:
        label: Progress label.
        value: Current value (0-100 by default).
        max: Maximum value (default 100).
        color: Optional CSS color for the bar.
        description: Optional helper text.
    """

    type: Literal["progress"] = "progress"
    label: str
    value: int | float = 0
    max: int | float = 100
    color: str | None = None
    description: str | None = None

    def to_props(self) -> dict[str, Any]:
        """Return progress bar props."""
        return {
            "label": self.label,
            "value": self.value,
            "max": self.max,
            "color": self.color,
            "description": self.description,
        }


# ---------------------------------------------------------------------------
# Layout blocks
# ---------------------------------------------------------------------------


class Divider(Block):
    """Visual separator block.

    Attributes:
        label: Optional centered label text.
        variant: Line style: ``'solid'``, ``'dashed'``, or ``'dotted'``.
    """

    type: Literal["divider"] = "divider"
    label: str | None = None
    variant: Literal["solid", "dashed", "dotted"] = "solid"

    def to_props(self) -> dict[str, Any]:
        """Return divider props."""
        return {
            "label": self.label,
            "variant": self.variant,
        }


class Section(Block):
    """Grouping container for other blocks.

    Sections allow hierarchical organisation of a report.

    Attributes:
        title: Section heading.
        description: Optional section description/subtitle.
        children: Ordered list of child blocks.
    """

    type: Literal["section"] = "section"
    title: str
    description: str | None = None
    children: list[AnyBlock] = Field(default_factory=list)

    def serialize(self, block_id: str, *, counter: int = 0) -> dict[str, Any]:
        """Serialise section and its children recursively.

        Args:
            block_id: This section's assigned ID.
            counter: Starting counter for child ID generation.

        Returns:
            Full section dict with nested children.
        """
        serialised_children: list[dict[str, Any]] = []
        for i, child in enumerate(self.children):
            child_id = f"block_{counter + i + 1:03d}"
            if isinstance(child, Section):
                serialised_children.append(child.serialize(child_id, counter=counter + i + 1))
            elif isinstance(child, (Columns, Tabs)):
                serialised_children.append(child.serialize(child_id, counter=counter + i + 1))
            else:
                serialised_children.append(child.serialize(child_id))
        return {
            "id": block_id,
            "type": self.type,
            "props": {
                "title": self.title,
                "description": self.description,
                "children": serialised_children,
            },
        }


class Columns(Block):
    """Multi-column layout container.

    Renders children side-by-side in a responsive grid.

    Attributes:
        children: Ordered list of child blocks (one per column).
        widths: Optional list of relative widths (must sum to 12 for MUI grid).
        layout: Layout mode: ``'equal'``, ``'bento'``, or ``'custom'``.
    """

    type: Literal["columns"] = "columns"
    children: list[AnyBlock] = Field(default_factory=list)
    widths: list[int] | None = None
    layout: Literal["equal", "bento", "custom"] = "equal"

    def serialize(self, block_id: str, *, counter: int = 0) -> dict[str, Any]:
        """Serialise columns and children.

        Args:
            block_id: This block's assigned ID.
            counter: Starting counter for child ID generation.

        Returns:
            Full block dict with serialised children.
        """
        serialised_children: list[dict[str, Any]] = []
        for i, child in enumerate(self.children):
            child_id = f"block_{counter + i + 1:03d}"
            if isinstance(child, (Section, Columns, Tabs)):
                serialised_children.append(child.serialize(child_id, counter=counter + i + 1))
            else:
                serialised_children.append(child.serialize(child_id))
        return {
            "id": block_id,
            "type": self.type,
            "props": {
                "children": serialised_children,
                "widths": self.widths,
                "layout": self.layout,
            },
        }


class Tabs(Block):
    """Tabbed content container.

    Each tab has a label and a list of child blocks.

    Attributes:
        tabs: List of tab definitions, each with ``label`` and ``children``.
    """

    type: Literal["tabs"] = "tabs"
    tabs: list[dict[str, Any]] = Field(default_factory=list)

    def serialize(self, block_id: str, *, counter: int = 0) -> dict[str, Any]:
        """Serialise tabs and their children.

        Args:
            block_id: This block's assigned ID.
            counter: Starting counter for child ID generation.

        Returns:
            Full block dict with serialised tab children.
        """
        serialised_tabs: list[dict[str, Any]] = []
        child_offset = counter
        for tab in self.tabs:
            label = tab.get("label", "Tab")
            children_raw = tab.get("children", [])
            serialised_children: list[dict[str, Any]] = []
            for i, child in enumerate(children_raw):
                child_id = f"block_{child_offset + i + 1:03d}"
                if isinstance(child, (Section, Columns, Tabs)):
                    serialised_children.append(
                        child.serialize(child_id, counter=child_offset + i + 1)
                    )
                elif isinstance(child, Block):
                    serialised_children.append(child.serialize(child_id))
                else:
                    # Already serialised dict
                    serialised_children.append(child)
            child_offset += len(children_raw)
            serialised_tabs.append({"label": label, "children": serialised_children})
        return {
            "id": block_id,
            "type": self.type,
            "props": {
                "tabs": serialised_tabs,
            },
        }


# ---------------------------------------------------------------------------
# Interactive blocks
# ---------------------------------------------------------------------------


class Slider(Block):
    """Interactive slider block.

    Attributes:
        label: Slider label.
        min: Minimum value.
        max: Maximum value.
        step: Step increment.
        default_value: Initial value (single or range tuple).
        unit: Optional unit label.
        show_value: Whether to display the current value.
    """

    type: Literal["slider"] = "slider"
    label: str
    min: int | float = 0
    max: int | float = 100
    step: int | float = 1
    default_value: int | float | list[int | float] | None = None
    unit: str | None = None
    show_value: bool = True

    def to_props(self) -> dict[str, Any]:
        """Return slider props."""
        return {
            "label": self.label,
            "min": self.min,
            "max": self.max,
            "step": self.step,
            "defaultValue": self.default_value,
            "unit": self.unit,
            "showValue": self.show_value,
        }


class NumberInput(Block):
    """Interactive number input with increment/decrement buttons.

    Attributes:
        label: Input label.
        min: Minimum value.
        max: Maximum value.
        step: Step increment.
        default_value: Initial value.
        unit: Optional unit label.
    """

    type: Literal["number_input"] = "number_input"
    label: str
    min: int | float = 0
    max: int | float = 100
    step: int | float = 1
    default_value: int | float = 0
    unit: str | None = None

    def to_props(self) -> dict[str, Any]:
        """Return number input props."""
        return {
            "label": self.label,
            "min": self.min,
            "max": self.max,
            "step": self.step,
            "defaultValue": self.default_value,
            "unit": self.unit,
        }


class Toggle(Block):
    """Interactive toggle switch block.

    Attributes:
        label: Toggle label.
        description: Optional description text.
        default_value: Initial state.
    """

    type: Literal["toggle"] = "toggle"
    label: str
    description: str | None = None
    default_value: bool = False

    def to_props(self) -> dict[str, Any]:
        """Return toggle props."""
        return {
            "label": self.label,
            "description": self.description,
            "defaultValue": self.default_value,
        }


class Accordion(Block):
    """Collapsible accordion panels.

    Attributes:
        panels: List of panel dicts with ``title``, ``subtitle``, ``children``,
                and optional ``default_expanded``.
    """

    type: Literal["accordion"] = "accordion"
    panels: list[dict[str, Any]] = Field(default_factory=list)

    def serialize(self, block_id: str, *, counter: int = 0) -> dict[str, Any]:
        """Serialise accordion and panel children.

        Args:
            block_id: This block's assigned ID.
            counter: Starting counter for child ID generation.

        Returns:
            Full block dict with serialised panel children.
        """
        serialised_panels: list[dict[str, Any]] = []
        child_offset = counter
        for panel in self.panels:
            title = panel.get("title", "Panel")
            subtitle = panel.get("subtitle")
            default_expanded = panel.get("default_expanded", False)
            children_raw = panel.get("children", [])
            serialised_children: list[dict[str, Any]] = []
            for i, child in enumerate(children_raw):
                child_id = f"block_{child_offset + i + 1:03d}"
                if isinstance(child, Block):
                    if isinstance(child, (Section, Columns, Tabs, Accordion)):
                        serialised_children.append(
                            child.serialize(child_id, counter=child_offset + i + 1)
                        )
                    else:
                        serialised_children.append(child.serialize(child_id))
                else:
                    serialised_children.append(child)
            child_offset += len(children_raw)
            serialised_panels.append(
                {
                    "title": title,
                    "subtitle": subtitle,
                    "defaultExpanded": default_expanded,
                    "children": serialised_children,
                }
            )
        return {
            "id": block_id,
            "type": self.type,
            "props": {
                "panels": serialised_panels,
            },
        }


class StatComparison(Block):
    """Side-by-side stat comparison block.

    Attributes:
        title: Block title.
        items: List of comparison dicts with ``label``, ``current``,
               ``previous``, and optional ``unit``.
    """

    type: Literal["stat_comparison"] = "stat_comparison"
    title: str
    items: list[dict[str, Any]] = Field(default_factory=list)

    def to_props(self) -> dict[str, Any]:
        """Return stat comparison props."""
        return {
            "title": self.title,
            "items": self.items,
        }


# ---------------------------------------------------------------------------
# New chart blocks (v0.3.0)
# ---------------------------------------------------------------------------


class HeatmapChart(Block):
    """2D heatmap chart.

    Attributes:
        title: Chart title.
        data: Data source (list of dicts or DataFrame).
        x: Column name for X axis.
        y: Column name for Y axis.
        value: Column name for the heat value.
        height: Chart height in pixels.
    """

    type: Literal["heatmap_chart"] = "heatmap_chart"
    title: str
    data: Any
    x: str
    y: str
    value: str
    height: int = 360

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "data": to_records(self.data),
            "x": self.x,
            "y": self.y,
            "value": self.value,
            "height": self.height,
        }


class CandlestickChart(Block):
    """Financial candlestick / OHLC chart.

    Attributes:
        title: Chart title.
        data: Data source with OHLC columns.
        x: Column for date/category axis.
        open: Column for open price.
        close: Column for close price.
        low: Column for low price.
        high: Column for high price.
        height: Chart height in pixels.
    """

    type: Literal["candlestick_chart"] = "candlestick_chart"
    title: str
    data: Any
    x: str
    open: str = "open"
    close: str = "close"
    low: str = "low"
    high: str = "high"
    height: int = 400

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "data": to_records(self.data),
            "x": self.x,
            "open": self.open,
            "close": self.close,
            "low": self.low,
            "high": self.high,
            "height": self.height,
        }


class SankeyChart(Block):
    """Sankey / flow diagram.

    Attributes:
        title: Chart title.
        nodes: List of node dicts with ``name`` key.
        links: List of link dicts with ``source``, ``target``, ``value``.
        height: Chart height in pixels.
    """

    type: Literal["sankey_chart"] = "sankey_chart"
    title: str
    nodes: list[dict[str, Any]]
    links: list[dict[str, Any]]
    height: int = 400

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "nodes": self.nodes,
            "links": self.links,
            "height": self.height,
        }


class WaterfallChart(Block):
    """Waterfall / bridge chart for financial analysis.

    Attributes:
        title: Chart title.
        data: Data source with category and value columns.
        category: Column name for categories.
        value: Column name for values.
        height: Chart height in pixels.
    """

    type: Literal["waterfall_chart"] = "waterfall_chart"
    title: str
    data: Any
    category: str
    value: str
    height: int = 360

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "data": to_records(self.data),
            "category": self.category,
            "value": self.value,
            "height": self.height,
        }


class BoxPlotChart(Block):
    """Statistical box plot chart.

    Attributes:
        title: Chart title.
        data: List of [min, Q1, median, Q3, max] arrays.
        categories: Labels for each box.
        height: Chart height in pixels.
    """

    type: Literal["box_plot_chart"] = "box_plot_chart"
    title: str
    data: list[list[float]]
    categories: list[str] | None = None
    height: int = 360

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "data": self.data,
            "categories": self.categories,
            "height": self.height,
        }


class MapChart(Block):
    """Geographical scatter chart.

    Attributes:
        title: Chart title.
        data: Data source with lat/lng/value columns.
        lat: Column name for latitude.
        lng: Column name for longitude.
        value: Column name for bubble size.
        name: Column name for point labels.
        height: Chart height in pixels.
    """

    type: Literal["map_chart"] = "map_chart"
    title: str
    data: Any
    lat: str
    lng: str
    value: str
    name: str | None = None
    height: int = 400

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "data": to_records(self.data),
            "lat": self.lat,
            "lng": self.lng,
            "value": self.value,
            "name": self.name,
            "height": self.height,
        }


# ---------------------------------------------------------------------------
# New content blocks (v0.3.0)
# ---------------------------------------------------------------------------


class Timeline(Block):
    """Vertical timeline for events/milestones.

    Attributes:
        title: Optional timeline heading.
        events: List of event dicts with ``date``, ``title``,
                and optional ``description``, ``icon``, ``color``.
    """

    type: Literal["timeline"] = "timeline"
    title: str | None = None
    events: list[dict[str, Any]] = Field(default_factory=list)

    def to_props(self) -> dict[str, Any]:
        return {"title": self.title, "events": self.events}


class Callout(Block):
    """Styled quote or highlight box.

    Attributes:
        content: The callout text.
        author: Optional attribution.
        icon: Optional emoji icon.
        variant: Style variant: ``'quote'``, ``'highlight'``, or ``'note'``.
    """

    type: Literal["callout"] = "callout"
    content: str
    author: str | None = None
    icon: str | None = None
    variant: Literal["quote", "highlight", "note"] = "quote"

    def to_props(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "author": self.author,
            "icon": self.icon,
            "variant": self.variant,
        }


class Embed(Block):
    """Iframe embed block.

    Attributes:
        url: URL to embed.
        title: Optional frame title.
        height: Frame height in pixels.
        aspect_ratio: Optional aspect ratio (e.g. ``'16/9'``).
    """

    type: Literal["embed"] = "embed"
    url: str
    title: str | None = None
    height: int = 400
    aspect_ratio: str | None = None

    def to_props(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "height": self.height,
            "aspect_ratio": self.aspect_ratio,
        }


class JsonViewer(Block):
    """Formatted JSON display.

    Attributes:
        data: Any JSON-serialisable data.
        title: Optional heading.
        collapsed_depth: Depth to collapse by default.
    """

    type: Literal["json_viewer"] = "json_viewer"
    data: Any
    title: str | None = None
    collapsed_depth: int = 2

    def to_props(self) -> dict[str, Any]:
        return {
            "data": self.data,
            "title": self.title,
            "collapsed_depth": self.collapsed_depth,
        }


class UserCard(Block):
    """Team member / person card.

    Attributes:
        name: Person's full name.
        role: Job title / role.
        avatar_url: Optional avatar image URL.
        email: Optional email address.
        stats: Optional list of ``{label, value}`` stat items.
    """

    type: Literal["user_card"] = "user_card"
    name: str
    role: str | None = None
    avatar_url: str | None = None
    email: str | None = None
    stats: list[dict[str, Any]] | None = None

    def to_props(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "avatar_url": self.avatar_url,
            "email": self.email,
            "stats": self.stats,
        }


class StatusList(Block):
    """List with status indicators (dots).

    Attributes:
        title: Optional list heading.
        items: List of ``{label, status, description?, value?}`` dicts.
               Status: ``'success'``, ``'warning'``, ``'error'``, ``'info'``, ``'pending'``.
    """

    type: Literal["status_list"] = "status_list"
    title: str | None = None
    items: list[dict[str, Any]] = Field(default_factory=list)

    def to_props(self) -> dict[str, Any]:
        return {"title": self.title, "items": self.items}


class InfoList(Block):
    """Key-value pair display.

    Attributes:
        title: Optional heading.
        items: List of ``{key, value, icon?}`` dicts.
    """

    type: Literal["info_list"] = "info_list"
    title: str | None = None
    items: list[dict[str, Any]] = Field(default_factory=list)

    def to_props(self) -> dict[str, Any]:
        return {"title": self.title, "items": self.items}


class Stepper(Block):
    """Process / wizard steps display.

    Attributes:
        title: Optional heading.
        steps: List of ``{label, description?, status?}`` dicts.
               Status: ``'complete'``, ``'active'``, ``'pending'``.
        current_step: Index of the currently active step (0-based).
    """

    type: Literal["stepper"] = "stepper"
    title: str | None = None
    steps: list[dict[str, Any]] = Field(default_factory=list)
    current_step: int | None = None

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "steps": self.steps,
            "current_step": self.current_step,
        }


# ---------------------------------------------------------------------------
# New interactive blocks (v0.3.0)
# ---------------------------------------------------------------------------


class Dropdown(Block):
    """Interactive dropdown selector.

    Attributes:
        label: Field label.
        options: List of ``{label, value}`` option dicts.
        default_value: Initial selected value.
        description: Optional helper text.
    """

    type: Literal["dropdown"] = "dropdown"
    label: str
    options: list[dict[str, Any]] = Field(default_factory=list)
    default_value: Any | None = None
    description: str | None = None

    def to_props(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "options": self.options,
            "default_value": self.default_value,
            "description": self.description,
        }


class TextInput(Block):
    """Text input field.

    Attributes:
        label: Field label.
        placeholder: Placeholder text.
        default_value: Initial value.
        multiline: If ``True``, render as textarea.
        rows: Number of rows for multiline.
        description: Optional helper text.
    """

    type: Literal["text_input"] = "text_input"
    label: str
    placeholder: str | None = None
    default_value: str | None = None
    multiline: bool = False
    rows: int = 3
    description: str | None = None

    def to_props(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "placeholder": self.placeholder,
            "default_value": self.default_value,
            "multiline": self.multiline,
            "rows": self.rows,
            "description": self.description,
        }


class CheckboxGroup(Block):
    """Multiple checkbox selection.

    Attributes:
        label: Group label.
        options: List of ``{label, value}`` option dicts.
        default_values: List of initially checked values.
        description: Optional helper text.
    """

    type: Literal["checkbox_group"] = "checkbox_group"
    label: str
    options: list[dict[str, Any]] = Field(default_factory=list)
    default_values: list[Any] | None = None
    description: str | None = None

    def to_props(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "options": self.options,
            "default_values": self.default_values,
            "description": self.description,
        }


class RadioGroup(Block):
    """Radio button selection.

    Attributes:
        label: Group label.
        options: List of ``{label, value}`` option dicts.
        default_value: Initially selected value.
        description: Optional helper text.
    """

    type: Literal["radio_group"] = "radio_group"
    label: str
    options: list[dict[str, Any]] = Field(default_factory=list)
    default_value: Any | None = None
    description: str | None = None

    def to_props(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "options": self.options,
            "default_value": self.default_value,
            "description": self.description,
        }


# ---------------------------------------------------------------------------
# New display blocks (v0.3.0)
# ---------------------------------------------------------------------------


class TagList(Block):
    """List of coloured tags / badges.

    Attributes:
        title: Optional heading.
        tags: List of ``{label, color?, variant?}`` dicts.
    """

    type: Literal["tag_list"] = "tag_list"
    title: str | None = None
    tags: list[dict[str, Any]] = Field(default_factory=list)

    def to_props(self) -> dict[str, Any]:
        return {"title": self.title, "tags": self.tags}


class Sparkline(Block):
    """Tiny inline sparkline chart.

    Attributes:
        data: List of numeric values.
        color: Line colour.
        height: Chart height in pixels.
        show_area: Whether to fill under the line.
    """

    type: Literal["sparkline"] = "sparkline"
    data: list[float | int]
    color: str | None = None
    height: int = 60
    show_area: bool = True

    def to_props(self) -> dict[str, Any]:
        return {
            "data": self.data,
            "color": self.color,
            "height": self.height,
            "show_area": self.show_area,
        }


class Video(Block):
    """Video embed block.

    Attributes:
        src: Video URL or file path.
        title: Optional video title.
        poster: Optional poster image URL.
        autoplay: Whether to autoplay.
        controls: Whether to show playback controls.
    """

    type: Literal["video"] = "video"
    src: str
    title: str | None = None
    poster: str | None = None
    autoplay: bool = False
    controls: bool = True

    def to_props(self) -> dict[str, Any]:
        return {
            "src": self.src,
            "title": self.title,
            "poster": self.poster,
            "autoplay": self.autoplay,
            "controls": self.controls,
        }


# ---------------------------------------------------------------------------
# Advanced chart blocks (v0.4.0)
# ---------------------------------------------------------------------------


class GanttChart(Block):
    """ECharts-based Gantt chart.

    Attributes:
        title: Chart title.
        tasks: List of task dicts with ``name``, ``start``, ``end``,
               and optional ``progress``, ``color``, ``group``.
        height: Chart height in pixels.
    """

    type: Literal["gantt_chart"] = "gantt_chart"
    title: str
    tasks: list[dict[str, Any]] = Field(default_factory=list)
    height: int = 400

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "tasks": self.tasks,
            "height": self.height,
        }


class DAGChart(Block):
    """Directed Acyclic Graph using ECharts graph layout.

    Attributes:
        title: Chart title.
        nodes: List of node dicts with ``id``, ``label``,
               and optional ``color``, ``icon``.
        edges: List of edge dicts with ``from``, ``to``,
               and optional ``label``.
        height: Chart height in pixels.
        layout: Graph layout algorithm: ``'force'`` or ``'circular'``.
    """

    type: Literal["dag_chart"] = "dag_chart"
    title: str
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    edges: list[dict[str, Any]] = Field(default_factory=list)
    height: int = 400
    layout: Literal["force", "circular"] = "force"

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "nodes": self.nodes,
            "edges": self.edges,
            "height": self.height,
            "layout": self.layout,
        }


class CorrelationMatrix(Block):
    """Correlation heatmap block.

    Attributes:
        title: Chart title.
        matrix: 2D array of correlation values in [-1, 1].
        labels: Column/row labels.
        height: Chart height in pixels.
    """

    type: Literal["correlation_matrix"] = "correlation_matrix"
    title: str
    matrix: list[list[float]] = Field(default_factory=list)
    labels: list[str] = Field(default_factory=list)
    height: int = 400

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "matrix": self.matrix,
            "labels": self.labels,
            "height": self.height,
        }


class Scorecard(Block):
    """Dense metric grid with conditional coloring.

    Attributes:
        title: Block title.
        data: Tabular data source.
        columns: Optional explicit column names to display.
        value_column: Column to apply threshold coloring to.
        thresholds: Dict mapping colour names to condition expressions,
                    e.g. ``{'green': '>90', 'yellow': '>70', 'red': '<=70'}``.
    """

    type: Literal["scorecard"] = "scorecard"
    title: str
    data: Any = None
    columns: list[str] | None = None
    value_column: str | None = None
    thresholds: dict[str, str] | None = None

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "data": to_records(self.data),
            "columns": self.columns,
            "value_column": self.value_column,
            "thresholds": self.thresholds,
        }


class DataProfile(Block):
    """Auto-EDA summary card.

    Attributes:
        title: Block title.
        columns: List of column profile dicts with ``name``, ``dtype``,
                 ``count``, ``null_count``, ``null_pct``, ``unique``,
                 and optional ``mean``, ``std``, ``min``, ``max``, ``top_values``.
    """

    type: Literal["data_profile"] = "data_profile"
    title: str
    columns: list[dict[str, Any]] = Field(default_factory=list)

    def to_props(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "columns": self.columns,
        }


class Compare(Block):
    """Side-by-side comparison container.

    Attributes:
        left_label: Label for the left pane.
        right_label: Label for the right pane.
        left_children: Blocks for the left pane.
        right_children: Blocks for the right pane.
        mode: Comparison mode: ``'side_by_side'`` or ``'overlay'``.
    """

    type: Literal["compare"] = "compare"
    left_label: str = "A"
    right_label: str = "B"
    left_children: list[AnyBlock] = Field(default_factory=list)
    right_children: list[AnyBlock] = Field(default_factory=list)
    mode: Literal["side_by_side", "overlay"] = "side_by_side"

    def serialize(self, block_id: str, *, counter: int = 0) -> dict[str, Any]:
        """Serialise compare block and its children.

        Args:
            block_id: This block's assigned ID.
            counter: Starting counter for child ID generation.

        Returns:
            Full block dict with serialised left and right children.
        """
        child_offset = counter
        serialised_left: list[dict[str, Any]] = []
        for i, child in enumerate(self.left_children):
            child_id = f"block_{child_offset + i + 1:03d}"
            if isinstance(child, (Section, Columns, Tabs, Accordion, Compare)):
                serialised_left.append(child.serialize(child_id, counter=child_offset + i + 1))
            elif isinstance(child, Block):
                serialised_left.append(child.serialize(child_id))
            else:
                serialised_left.append(child)
        child_offset += len(self.left_children)

        serialised_right: list[dict[str, Any]] = []
        for i, child in enumerate(self.right_children):
            child_id = f"block_{child_offset + i + 1:03d}"
            if isinstance(child, (Section, Columns, Tabs, Accordion, Compare)):
                serialised_right.append(child.serialize(child_id, counter=child_offset + i + 1))
            elif isinstance(child, Block):
                serialised_right.append(child.serialize(child_id))
            else:
                serialised_right.append(child)

        return {
            "id": block_id,
            "type": self.type,
            "props": {
                "left_label": self.left_label,
                "right_label": self.right_label,
                "left_children": serialised_left,
                "right_children": serialised_right,
                "mode": self.mode,
            },
        }


# ---------------------------------------------------------------------------
# Discriminated union
# ---------------------------------------------------------------------------

AnyBlock = Annotated[
    KPI
    | LineChart
    | AreaChart
    | BarChart
    | PieChart
    | ScatterChart
    | RadarChart
    | GaugeChart
    | FunnelChart
    | TreemapChart
    | DataTable
    | Markdown
    | CodeBlock
    | Image
    | Alert
    | ProgressBar
    | Metric
    | Divider
    | Section
    | Columns
    | Tabs
    | Slider
    | NumberInput
    | Toggle
    | Accordion
    | StatComparison
    | HeatmapChart
    | CandlestickChart
    | SankeyChart
    | WaterfallChart
    | BoxPlotChart
    | MapChart
    | Timeline
    | Callout
    | Embed
    | JsonViewer
    | UserCard
    | StatusList
    | InfoList
    | Stepper
    | Dropdown
    | TextInput
    | CheckboxGroup
    | RadioGroup
    | TagList
    | Sparkline
    | Video
    | GanttChart
    | DAGChart
    | CorrelationMatrix
    | Scorecard
    | DataProfile
    | Compare,
    Field(discriminator="type"),
]
"""Union type of all block models, discriminated on the ``type`` field."""

# Rebuild models that reference AnyBlock (forward ref resolution)
Section.model_rebuild()
Columns.model_rebuild()
Tabs.model_rebuild()
Accordion.model_rebuild()
Compare.model_rebuild()
