"""Report templates for common dashboard layouts.

Pre-built report configurations that produce beautiful dashboards
with a single line of code::

    from holysheet.templates import SalesDashboard

    report = SalesDashboard(data=df)
    report.export_html("dashboard.html")
"""

from __future__ import annotations

from typing import Any

from holysheet.blocks import (
    KPI,
    Alert,
    AreaChart,
    BarChart,
    Columns,
    DataTable,
    Divider,
    FunnelChart,
    GaugeChart,
    LineChart,
    PieChart,
    ProgressBar,
    Section,
    StatusList,
    Tabs,
    Timeline,
)
from holysheet.report import Report


def _safe_get(data: dict[str, Any] | None, key: str, default: Any = None) -> Any:
    """Safely get a value from a dict or return default."""
    if data is None:
        return default
    return data.get(key, default)


# ---------------------------------------------------------------------------
# Sales Dashboard
# ---------------------------------------------------------------------------


class SalesDashboard(Report):
    """Pre-built sales dashboard with KPIs, revenue charts, and pipeline.

    Args:
        data: Optional dict with keys: ``kpis``, ``revenue``, ``pipeline``,
              ``by_region``, ``top_clients``.
        theme: Theme name (default ``"dark"``).
        title: Dashboard title.
    """

    def __init__(
        self,
        data: dict[str, Any] | None = None,
        theme: str = "dark",
        title: str = "Sales Dashboard",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            title=title,
            theme=theme,
            **kwargs,
        )
        self._build(data or {})

    def _build(self, data: dict[str, Any]) -> None:
        # KPI row
        kpis = data.get("kpis", {})
        self.add(
            Columns(
                children=[
                    KPI(
                        label="Revenue",
                        value=kpis.get("revenue", "$0"),
                        delta=kpis.get("revenue_delta", ""),
                        status=kpis.get("revenue_status", "neutral"),
                    ),
                    KPI(
                        label="Deals Won",
                        value=kpis.get("deals_won", 0),
                        delta=kpis.get("deals_delta", ""),
                        status=kpis.get("deals_status", "neutral"),
                    ),
                    KPI(
                        label="Avg Deal Size",
                        value=kpis.get("avg_deal", "$0"),
                        delta=kpis.get("avg_deal_delta", ""),
                        status=kpis.get("avg_deal_status", "neutral"),
                    ),
                    KPI(
                        label="Win Rate",
                        value=kpis.get("win_rate", "0%"),
                        delta=kpis.get("win_rate_delta", ""),
                        status=kpis.get("win_rate_status", "neutral"),
                    ),
                ],
                layout="equal",
            )
        )

        self.add(Divider())

        # Revenue trend
        if data.get("revenue"):
            self.add(
                Section(
                    title="Revenue Trend",
                    children=[
                        AreaChart(
                            title="Monthly Revenue",
                            data=data["revenue"],
                            x=data.get("revenue_x", "month"),
                            y=data.get("revenue_y", "revenue"),
                        ),
                    ],
                )
            )

        # Regional breakdown and pipeline
        children_tabs: list[dict[str, Any]] = []
        if data.get("by_region"):
            children_tabs.append(
                {
                    "label": "By Region",
                    "children": [
                        PieChart(
                            title="Revenue by Region",
                            data=data["by_region"],
                            name=data.get("region_name", "region"),
                            value=data.get("region_value", "revenue"),
                        ),
                    ],
                }
            )
        if data.get("pipeline"):
            children_tabs.append(
                {
                    "label": "Pipeline",
                    "children": [
                        FunnelChart(
                            title="Sales Pipeline",
                            data=data["pipeline"],
                            name=data.get("pipeline_name", "stage"),
                            value=data.get("pipeline_value", "count"),
                        ),
                    ],
                }
            )

        if children_tabs:
            self.add(Tabs(tabs=children_tabs))

        # Top clients table
        if data.get("top_clients"):
            self.add(
                DataTable(
                    title="Top Clients",
                    data=data["top_clients"],
                    searchable=True,
                    paginated=True,
                )
            )


# ---------------------------------------------------------------------------
# Executive Summary
# ---------------------------------------------------------------------------


class ExecutiveSummary(Report):
    """Pre-built executive summary with scorecards, trends, and highlights.

    Args:
        data: Optional dict with keys: ``metrics``, ``highlights``,
              ``trends``, ``milestones``.
        theme: Theme name (default ``"executive"``).
        title: Report title.
    """

    def __init__(
        self,
        data: dict[str, Any] | None = None,
        theme: str = "executive",
        title: str = "Executive Summary",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            title=title,
            theme=theme,
            **kwargs,
        )
        self._build(data or {})

    def _build(self, data: dict[str, Any]) -> None:
        # Metrics row
        metrics = data.get("metrics", [])
        if metrics:
            metric_blocks = []
            for m in metrics[:6]:
                metric_blocks.append(
                    KPI(
                        label=m.get("label", ""),
                        value=m.get("value", 0),
                        unit=m.get("unit"),
                        delta=m.get("delta"),
                        status=m.get("status", "neutral"),
                    )
                )
            self.add(Columns(children=list(metric_blocks), layout="equal"))
            self.add(Divider())

        # Highlights
        highlights = data.get("highlights", [])
        if highlights:
            self.add(
                Section(
                    title="Key Highlights",
                    children=[
                        Alert(
                            severity=h.get("severity", "info"),
                            title=h.get("title"),
                            message=h.get("message", ""),
                        )
                        for h in highlights
                    ],
                )
            )

        # Trends
        if data.get("trends"):
            self.add(
                LineChart(
                    title="Key Trends",
                    data=data["trends"],
                    x=data.get("trends_x", "period"),
                    y=data.get("trends_y"),
                )
            )

        # Milestones
        milestones = data.get("milestones", [])
        if milestones:
            self.add(
                Timeline(
                    title="Key Milestones",
                    events=milestones,
                )
            )


# ---------------------------------------------------------------------------
# Ops Monitor
# ---------------------------------------------------------------------------


class OpsMonitor(Report):
    """Pre-built operations monitoring dashboard.

    Args:
        data: Optional dict with keys: ``services``, ``metrics``,
              ``errors``, ``latency``.
        theme: Theme name (default ``"dark"``).
        title: Dashboard title.
    """

    def __init__(
        self,
        data: dict[str, Any] | None = None,
        theme: str = "dark",
        title: str = "Operations Monitor",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            title=title,
            theme=theme,
            **kwargs,
        )
        self._build(data or {})

    def _build(self, data: dict[str, Any]) -> None:
        # Service health
        services = data.get("services", [])
        if services:
            self.add(
                StatusList(
                    title="Service Health",
                    items=services,
                )
            )
            self.add(Divider())

        # Key metrics gauges
        metrics = data.get("metrics", [])
        if metrics:
            gauge_blocks = []
            for m in metrics[:4]:
                gauge_blocks.append(
                    GaugeChart(
                        title=m.get("label", ""),
                        value=m.get("value", 0),
                        min=m.get("min", 0),
                        max=m.get("max", 100),
                        unit=m.get("unit"),
                    )
                )
            self.add(Columns(children=list(gauge_blocks), layout="equal"))

        # Error rate over time
        if data.get("errors"):
            self.add(
                BarChart(
                    title="Error Rate",
                    data=data["errors"],
                    x=data.get("errors_x", "time"),
                    y=data.get("errors_y", "count"),
                )
            )

        # Latency percentiles
        if data.get("latency"):
            self.add(
                LineChart(
                    title="Latency (p50 / p95 / p99)",
                    data=data["latency"],
                    x=data.get("latency_x", "time"),
                    y=data.get("latency_y", ["p50", "p95", "p99"]),
                )
            )

        # Progress bars for SLOs
        slos = data.get("slos", [])
        if slos:
            self.add(
                Section(
                    title="SLO Compliance",
                    children=[
                        ProgressBar(
                            label=s.get("label", ""),
                            value=s.get("value", 0),
                            max=s.get("max", 100),
                            color=s.get("color"),
                        )
                        for s in slos
                    ],
                )
            )
