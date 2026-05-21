#!/usr/bin/env python3
"""Sales dashboard example for HolySheet.

Run:
    python examples/sales_dashboard.py
"""

from holysheet import (
    KPI,
    BarChart,
    DataTable,
    LineChart,
    Markdown,
    PieChart,
    Report,
    Section,
)

# ── Fake Data ──────────────────────────────────────────────────────────────────

monthly_sales = [
    {"month": "Jan", "sales": 245_000, "returns": 12_000},
    {"month": "Feb", "sales": 268_000, "returns": 15_000},
    {"month": "Mar", "sales": 312_000, "returns": 9_000},
    {"month": "Apr", "sales": 298_000, "returns": 11_000},
    {"month": "May", "sales": 342_000, "returns": 14_000},
    {"month": "Jun", "sales": 389_000, "returns": 8_000},
    {"month": "Jul", "sales": 356_000, "returns": 13_000},
    {"month": "Aug", "sales": 410_000, "returns": 10_000},
    {"month": "Sep", "sales": 445_000, "returns": 16_000},
    {"month": "Oct", "sales": 478_000, "returns": 12_000},
    {"month": "Nov", "sales": 512_000, "returns": 18_000},
    {"month": "Dec", "sales": 580_000, "returns": 22_000},
]

region_data = [
    {"region": "North America", "sales": 1_840_000},
    {"region": "Europe", "sales": 1_250_000},
    {"region": "Asia Pacific", "sales": 920_000},
    {"region": "Latin America", "sales": 410_000},
    {"region": "Middle East", "sales": 215_000},
]

channel_data = [
    {"channel": "Direct Sales", "revenue": 2_100_000},
    {"channel": "Online Store", "revenue": 1_500_000},
    {"channel": "Partners", "revenue": 800_000},
    {"channel": "Retail", "revenue": 450_000},
    {"channel": "Referrals", "revenue": 285_000},
]

top_deals = [
    {
        "deal": "Enterprise Suite - Acme Corp",
        "rep": "Michael Torres",
        "value": "$450,000",
        "stage": "Closed Won",
        "close_date": "2026-11-15",
    },
    {
        "deal": "Platform License - GlobalTech",
        "rep": "Sarah Kim",
        "value": "$320,000",
        "stage": "Negotiation",
        "close_date": "2026-12-01",
    },
    {
        "deal": "Data Analytics - FinCorp",
        "rep": "James Wilson",
        "value": "$280,000",
        "stage": "Closed Won",
        "close_date": "2026-10-28",
    },
    {
        "deal": "Cloud Migration - MedHealth",
        "rep": "Ana Garcia",
        "value": "$210,000",
        "stage": "Proposal",
        "close_date": "2026-12-15",
    },
    {
        "deal": "AI Integration - RetailMax",
        "rep": "David Chen",
        "value": "$195,000",
        "stage": "Closed Won",
        "close_date": "2026-11-20",
    },
    {
        "deal": "Security Platform - BankSafe",
        "rep": "Lisa Park",
        "value": "$175,000",
        "stage": "Contract Review",
        "close_date": "2026-12-10",
    },
]

# ── Build Report ───────────────────────────────────────────────────────────────

report = Report(
    title="Q4 Sales Performance Dashboard",
    subtitle="Sales metrics, pipeline, and regional performance",
    theme="executive",
)

report.add(
    Markdown(
        content="""## Sales Overview

Q4 has been our strongest quarter yet, with **$4.64M** in total sales representing
a **23% increase** over Q3. The sales team has exceeded quota by 15%, with particularly
strong performance in the North America and Europe regions.
"""
    )
)

# KPIs
report.add(KPI(label="Total Sales", value="$4.64M", delta="+23%", status="positive"))
report.add(KPI(label="Deals Closed", value=127, delta="+18", status="positive"))
report.add(
    KPI(
        label="Win Rate",
        value=68,
        unit="%",
        delta="+4.2%",
        status="positive",
        description="Up from 63.8% last quarter",
    )
)
report.add(KPI(label="Avg Deal Size", value="$36.5K", delta="+$2.1K", status="positive"))

# Sales trends
report.add(
    LineChart(
        title="Monthly Sales Trend",
        data=monthly_sales,
        x="month",
        y="sales",
        height=400,
    )
)

# Regional breakdown
report.add(
    Section(
        title="Regional & Channel Analysis",
        description="Sales distribution by geography and channel",
        children=[
            BarChart(
                title="Sales by Region",
                data=region_data,
                x="region",
                y="sales",
            ),
            PieChart(
                title="Revenue by Channel",
                data=channel_data,
                name="channel",
                value="revenue",
            ),
        ],
    )
)

# Top deals
report.add(
    DataTable(
        title="Top Deals This Quarter",
        data=top_deals,
        columns=["deal", "rep", "value", "stage", "close_date"],
    )
)

# ── Export ──────────────────────────────────────────────────────────────────────

output_path = report.export_html("sales_dashboard.html")
print(f"✅ Sales dashboard exported to: {output_path}")
print(f"   Open in browser: file://{output_path}")
