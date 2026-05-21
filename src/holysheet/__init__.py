"""HolySheet — Python-first report compiler for interactive dashboards.

Quick start::

    from holysheet import Report, KPI, LineChart

    report = Report(title="My Report", theme="dark")
    report.add(KPI(label="Users", value=42_000, delta="+5.2%", status="positive"))
    report.export_html("report.html")

Exports:
    Report, all block types, Theme, templates, and __version__
"""

from __future__ import annotations

from holysheet.blocks import (
    KPI,
    Accordion,
    Alert,
    AreaChart,
    BarChart,
    BoxPlotChart,
    Callout,
    CandlestickChart,
    CheckboxGroup,
    CodeBlock,
    Columns,
    Compare,
    CorrelationMatrix,
    DAGChart,
    DataProfile,
    DataTable,
    Divider,
    Dropdown,
    Embed,
    FunnelChart,
    GanttChart,
    GaugeChart,
    HeatmapChart,
    Image,
    InfoList,
    JsonViewer,
    LineChart,
    MapChart,
    Markdown,
    Metric,
    NumberInput,
    PieChart,
    ProgressBar,
    RadarChart,
    RadioGroup,
    SankeyChart,
    ScatterChart,
    Scorecard,
    Section,
    Slider,
    Sparkline,
    StatComparison,
    StatusList,
    Stepper,
    Tabs,
    TagList,
    TextInput,
    Timeline,
    Toggle,
    TreemapChart,
    UserCard,
    Video,
    WaterfallChart,
)
from holysheet.report import Report
from holysheet.themes import Theme

__version__ = "0.4.0"

__all__ = [
    # KPI & Metrics
    "KPI",
    "Accordion",
    "Alert",
    "AreaChart",
    "BarChart",
    "BoxPlotChart",
    "Callout",
    "CandlestickChart",
    "CheckboxGroup",
    "CodeBlock",
    "Columns",
    "Compare",
    "CorrelationMatrix",
    "DAGChart",
    "DataProfile",
    # Data & Content
    "DataTable",
    "Divider",
    "Dropdown",
    "Embed",
    "FunnelChart",
    "GanttChart",
    "GaugeChart",
    "HeatmapChart",
    "Image",
    "InfoList",
    "JsonViewer",
    # Charts
    "LineChart",
    "MapChart",
    "Markdown",
    "Metric",
    "NumberInput",
    "PieChart",
    "ProgressBar",
    "RadarChart",
    "RadioGroup",
    # Core
    "Report",
    "SankeyChart",
    "ScatterChart",
    "Scorecard",
    # Layout
    "Section",
    # Interactive
    "Slider",
    "Sparkline",
    "StatComparison",
    "StatusList",
    "Stepper",
    "Tabs",
    "TagList",
    "TextInput",
    "Theme",
    "Timeline",
    "Toggle",
    "TreemapChart",
    "UserCard",
    "Video",
    "WaterfallChart",
    # Meta
    "__version__",
]
