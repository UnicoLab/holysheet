"""HolySheet — Python-first report compiler for interactive dashboards.

Quick start::

    from holysheet import Report, KPI, LineChart

    report = Report(title="My Report", theme="dark")
    report.add(KPI(label="Users", value=42_000, delta="+5.2%", status="positive"))
    report.export_html("report.html")

Exports:
    Report, KPI, Metric, LineChart, AreaChart, BarChart, PieChart, ScatterChart,
    RadarChart, GaugeChart, FunnelChart, TreemapChart, DataTable, Markdown,
    CodeBlock, Image, Alert, ProgressBar, Divider, Section, Columns, Tabs,
    Slider, NumberInput, Toggle, Accordion, StatComparison, __version__
"""

from __future__ import annotations

from holysheet.blocks import (
    KPI,
    Accordion,
    Alert,
    AreaChart,
    BarChart,
    CodeBlock,
    Columns,
    DataTable,
    Divider,
    FunnelChart,
    GaugeChart,
    Image,
    LineChart,
    Markdown,
    Metric,
    NumberInput,
    PieChart,
    ProgressBar,
    RadarChart,
    ScatterChart,
    Section,
    Slider,
    StatComparison,
    Tabs,
    Toggle,
    TreemapChart,
)
from holysheet.report import Report

__version__ = "0.2.0"

__all__ = [
    "Accordion",
    "Alert",
    "AreaChart",
    "BarChart",
    "CodeBlock",
    "Columns",
    "DataTable",
    "Divider",
    "FunnelChart",
    "GaugeChart",
    "Image",
    "KPI",
    "LineChart",
    "Markdown",
    "Metric",
    "NumberInput",
    "PieChart",
    "ProgressBar",
    "RadarChart",
    "Report",
    "ScatterChart",
    "Section",
    "Slider",
    "StatComparison",
    "Tabs",
    "Toggle",
    "TreemapChart",
    "__version__",
]
