"""HolySheet v0.5.0 Feature Showcase.

Demonstrates: anomaly detection, SQL blocks, narration, cross-block filters,
auto-narrate, and new block types.

Usage:
    python examples/v050_showcase.py
"""

from holysheet import (
    KPI,
    BarChart,
    Columns,
    DataTable,
    LineChart,
    NarrationBlock,
    Report,
    SqlBlock,
)

# Sample data
metrics = [
    {"month": "Jan", "revenue": 120000, "users": 4200, "region": "US"},
    {"month": "Feb", "revenue": 135000, "users": 4800, "region": "US"},
    {"month": "Mar", "revenue": 128000, "users": 5100, "region": "EU"},
    {"month": "Apr", "revenue": 142000, "users": 5500, "region": "EU"},
    {"month": "May", "revenue": 155000, "users": 6200, "region": "APAC"},
    {"month": "Jun", "revenue": 500000, "users": 6100, "region": "US"},  # Anomaly!
    {"month": "Jul", "revenue": 148000, "users": 6800, "region": "EU"},
    {"month": "Aug", "revenue": 152000, "users": 7200, "region": "APAC"},
    {"month": "Sep", "revenue": 160000, "users": 7800, "region": "US"},
    {"month": "Oct", "revenue": 168000, "users": 8100, "region": "EU"},
    {"month": "Nov", "revenue": 175000, "users": 8500, "region": "APAC"},
    {"month": "Dec", "revenue": 190000, "users": 9200, "region": "US"},
]

report = Report(
    title="v0.5.0 Feature Showcase",
    theme="dark",
    theme_switch=True,
    download_buttons=True,
)

# Global filter
report.add_filter(
    "region",
    type="dropdown",
    label="Region",
    options=["US", "EU", "APAC"],
    default="US",
)

# KPIs
report.add(
    Columns(
        children=[
            KPI(label="Total Revenue", value="$1.97M", delta="+58%", status="positive"),
            KPI(label="Active Users", value="9.2K", delta="+119%", status="positive"),
            KPI(label="Avg Monthly", value="$164K", unit="/mo"),
        ]
    )
)

# Anomaly detection chart
report.add(
    LineChart(
        title="Revenue Trend (with Anomaly Detection)",
        data=metrics,
        x="month",
        y="revenue",
        anomaly_detection=True,
        downloadable=True,
    )
)

# Bar chart
report.add(
    BarChart(
        title="Users by Month",
        data=metrics,
        x="month",
        y="users",
        downloadable=True,
    )
)

# SQL block
report.add(
    SqlBlock(
        title="Revenue Query",
        query=(
            "SELECT region, SUM(revenue) as total_revenue "
            "FROM data GROUP BY region ORDER BY total_revenue DESC"
        ),
        data=metrics,
    )
)

# Data table
report.add(
    DataTable(
        title="Monthly Metrics",
        data=metrics,
        searchable=True,
        paginated=True,
    )
)

# Auto-narration
narration_text = report.auto_narrate()
report.add(
    NarrationBlock(
        text=narration_text,
        autoplay=False,
    )
)

report.export_html("v050_showcase.html")
print(f"✅ Report exported with {len(metrics)} data points")
print(f"📝 Auto-narration: {narration_text[:100]}...")
