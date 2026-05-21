"""Shared test fixtures for HolySheet tests."""

from __future__ import annotations

from typing import Any

import pytest

from holysheet import KPI, BarChart, DataTable, LineChart, Markdown, PieChart, Report, Section

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_records() -> list[dict[str, Any]]:
    """A small list of record dicts for chart/table tests."""
    return [
        {"month": "Jan", "revenue": 1200, "costs": 800},
        {"month": "Feb", "revenue": 1500, "costs": 900},
        {"month": "Mar", "revenue": 1800, "costs": 950},
        {"month": "Apr", "revenue": 2100, "costs": 1000},
    ]


@pytest.fixture()
def sample_column_data() -> dict[str, list[Any]]:
    """Column-oriented dict of lists."""
    return {
        "name": ["Alice", "Bob", "Charlie"],
        "score": [95, 87, 92],
        "grade": ["A", "B+", "A-"],
    }


@pytest.fixture()
def pie_data() -> list[dict[str, Any]]:
    """Pie chart data."""
    return [
        {"category": "Desktop", "share": 62},
        {"category": "Mobile", "share": 31},
        {"category": "Tablet", "share": 7},
    ]


# ---------------------------------------------------------------------------
# Block fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def kpi_block() -> KPI:
    """A basic KPI block."""
    return KPI(
        label="Total Revenue",
        value="$1.2M",
        unit="USD",
        delta="+12.3%",
        status="positive",
        description="Year-to-date",
    )


@pytest.fixture()
def line_chart_block(sample_records: list[dict[str, Any]]) -> LineChart:
    """A line chart block with sample data."""
    return LineChart(
        title="Revenue Trend",
        data=sample_records,
        x="month",
        y="revenue",
    )


@pytest.fixture()
def bar_chart_block(sample_records: list[dict[str, Any]]) -> BarChart:
    """A bar chart block with sample data."""
    return BarChart(
        title="Revenue vs Costs",
        data=sample_records,
        x="month",
        y=["revenue", "costs"],
    )


@pytest.fixture()
def pie_chart_block(pie_data: list[dict[str, Any]]) -> PieChart:
    """A pie chart block."""
    return PieChart(
        title="Device Distribution",
        data=pie_data,
        name="category",
        value="share",
    )


@pytest.fixture()
def data_table_block(sample_records: list[dict[str, Any]]) -> DataTable:
    """A data table block."""
    return DataTable(
        title="Monthly Breakdown",
        data=sample_records,
    )


@pytest.fixture()
def markdown_block() -> Markdown:
    """A markdown block."""
    return Markdown(content="## Executive Summary\n\nThis is a test report.")


@pytest.fixture()
def section_block(kpi_block: KPI, markdown_block: Markdown) -> Section:
    """A section with child blocks."""
    return Section(
        title="Overview",
        description="Key metrics and summary",
        children=[kpi_block, markdown_block],
    )


# ---------------------------------------------------------------------------
# Report fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def empty_report() -> Report:
    """An empty report."""
    return Report(title="Test Report", theme="light")


@pytest.fixture()
def populated_report(
    kpi_block: KPI,
    line_chart_block: LineChart,
    bar_chart_block: BarChart,
    pie_chart_block: PieChart,
    data_table_block: DataTable,
    markdown_block: Markdown,
) -> Report:
    """A report populated with one of every block type."""
    report = Report(title="Full Test Report", subtitle="All block types", theme="dark")
    report.add(kpi_block)
    report.add(line_chart_block)
    report.add(bar_chart_block)
    report.add(pie_chart_block)
    report.add(data_table_block)
    report.add(markdown_block)
    return report
