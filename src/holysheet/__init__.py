"""HolySheet — Python-first report compiler for interactive dashboards.

Quick start::

    from holysheet import Report, KPI, LineChart

    report = Report(title="My Report", theme="dark")
    report.add(KPI(label="Users", value=42_000, delta="+5.2%", status="positive"))
    report.export_html("report.html")

Exports:
    Report, all 47 block types, and __version__
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
    DataTable,
    Divider,
    Dropdown,
    Embed,
    FunnelChart,
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

__version__ = "0.3.0"

__all__ = [
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
    "DataTable",
    "Divider",
    "Dropdown",
    "Embed",
    "FunnelChart",
    "GaugeChart",
    "HeatmapChart",
    "Image",
    "InfoList",
    "JsonViewer",
    "LineChart",
    "MapChart",
    "Markdown",
    "Metric",
    "NumberInput",
    "PieChart",
    "ProgressBar",
    "RadarChart",
    "RadioGroup",
    "Report",
    "SankeyChart",
    "ScatterChart",
    "Section",
    "Slider",
    "Sparkline",
    "StatComparison",
    "StatusList",
    "Stepper",
    "Tabs",
    "TagList",
    "TextInput",
    "Timeline",
    "Toggle",
    "TreemapChart",
    "UserCard",
    "Video",
    "WaterfallChart",
    "__version__",
]
