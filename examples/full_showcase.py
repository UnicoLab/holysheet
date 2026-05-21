#!/usr/bin/env python3
"""HolySheet v0.3.0 — Full showcase of all 47 block types.

This example generates a comprehensive dark-themed dashboard that demonstrates
every block type available in HolySheet.
fictional SaaS analytics platform called "NovaPulse".

Usage:
    python examples/full_showcase.py

Output:
    full_showcase.html  — A single, self-contained HTML file.
"""

from __future__ import annotations

from holysheet import (
    KPI,
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
    PieChart,
    ProgressBar,
    RadarChart,
    RadioGroup,
    Report,
    SankeyChart,
    ScatterChart,
    Section,
    Sparkline,
    StatusList,
    Stepper,
    Tabs,
    TagList,
    TextInput,
    Timeline,
    TreemapChart,
    UserCard,
    WaterfallChart,
)


def main() -> None:
    """Build the full showcase report."""

    # =================================================================
    # DATA
    # =================================================================

    # Monthly revenue data
    monthly_revenue = [
        {"month": "Jan", "revenue": 124_500, "costs": 78_200, "profit": 46_300},
        {"month": "Feb", "revenue": 138_200, "costs": 82_100, "profit": 56_100},
        {"month": "Mar", "revenue": 152_800, "costs": 85_600, "profit": 67_200},
        {"month": "Apr", "revenue": 149_300, "costs": 83_900, "profit": 65_400},
        {"month": "May", "revenue": 168_700, "costs": 91_200, "profit": 77_500},
        {"month": "Jun", "revenue": 185_400, "costs": 95_800, "profit": 89_600},
        {"month": "Jul", "revenue": 192_100, "costs": 98_400, "profit": 93_700},
        {"month": "Aug", "revenue": 201_600, "costs": 102_300, "profit": 99_300},
        {"month": "Sep", "revenue": 215_900, "costs": 108_700, "profit": 107_200},
        {"month": "Oct", "revenue": 228_400, "costs": 112_500, "profit": 115_900},
        {"month": "Nov", "revenue": 241_800, "costs": 118_200, "profit": 123_600},
        {"month": "Dec", "revenue": 258_300, "costs": 124_900, "profit": 133_400},
    ]

    # User growth data (area chart)
    user_growth = [
        {"month": "Jan", "active_users": 12_400, "new_signups": 2_100},
        {"month": "Feb", "active_users": 14_200, "new_signups": 2_450},
        {"month": "Mar", "active_users": 16_800, "new_signups": 3_200},
        {"month": "Apr", "active_users": 18_500, "new_signups": 2_900},
        {"month": "May", "active_users": 21_300, "new_signups": 3_600},
        {"month": "Jun", "active_users": 24_100, "new_signups": 4_100},
        {"month": "Jul", "active_users": 26_800, "new_signups": 3_800},
        {"month": "Aug", "active_users": 29_500, "new_signups": 4_300},
        {"month": "Sep", "active_users": 32_700, "new_signups": 4_800},
        {"month": "Oct", "active_users": 35_200, "new_signups": 4_200},
        {"month": "Nov", "active_users": 38_400, "new_signups": 5_100},
        {"month": "Dec", "active_users": 42_000, "new_signups": 5_600},
    ]

    # Revenue by segment (pie chart)
    revenue_by_segment = [
        {"segment": "Enterprise", "revenue": 980_000},
        {"segment": "Mid-Market", "revenue": 620_000},
        {"segment": "SMB", "revenue": 340_000},
        {"segment": "Startup", "revenue": 185_000},
        {"segment": "Individual", "revenue": 92_000},
    ]

    # Revenue by product (bar chart)
    revenue_by_product = [
        {"product": "Analytics Pro", "q3": 245_000, "q4": 312_000},
        {"product": "Data Pipeline", "q3": 189_000, "q4": 228_000},
        {"product": "Dashboard Hub", "q3": 156_000, "q4": 198_000},
        {"product": "API Gateway", "q3": 112_000, "q4": 145_000},
        {"product": "ML Studio", "q3": 78_000, "q4": 118_000},
    ]

    # Scatter plot: feature usage vs satisfaction
    feature_scatter = [
        {"feature": "Real-time Alerts", "usage_pct": 89, "satisfaction": 4.7, "users": 3200},
        {"feature": "Custom Charts", "usage_pct": 76, "satisfaction": 4.5, "users": 2800},
        {"feature": "API Access", "usage_pct": 62, "satisfaction": 4.2, "users": 1900},
        {"feature": "Scheduled Reports", "usage_pct": 54, "satisfaction": 4.6, "users": 1500},
        {"feature": "Data Export", "usage_pct": 71, "satisfaction": 3.9, "users": 2400},
        {"feature": "Team Sharing", "usage_pct": 83, "satisfaction": 4.4, "users": 3000},
        {"feature": "Embed Widgets", "usage_pct": 34, "satisfaction": 3.7, "users": 800},
        {"feature": "Slack Integration", "usage_pct": 47, "satisfaction": 4.1, "users": 1200},
        {"feature": "Webhooks", "usage_pct": 28, "satisfaction": 3.5, "users": 600},
        {"feature": "SSO / SAML", "usage_pct": 41, "satisfaction": 4.8, "users": 1100},
    ]

    # Radar chart: team performance
    radar_data = [
        {
            "team": "Engineering",
            "velocity": 92,
            "quality": 88,
            "collaboration": 76,
            "innovation": 95,
            "delivery": 84,
        },
        {
            "team": "Product",
            "velocity": 78,
            "quality": 91,
            "collaboration": 94,
            "innovation": 87,
            "delivery": 82,
        },
    ]

    # Funnel: conversion pipeline
    funnel_data = [
        {"stage": "Website Visitors", "count": 148_200},
        {"stage": "Sign-ups", "count": 24_500},
        {"stage": "Activated", "count": 14_800},
        {"stage": "Trial Started", "count": 8_200},
        {"stage": "Paid Conversion", "count": 3_400},
        {"stage": "Enterprise Upsell", "count": 420},
    ]

    # Treemap: infrastructure costs
    treemap_data = [
        {"service": "Compute (GKE)", "cost": 42_300},
        {"service": "Cloud SQL", "cost": 28_700},
        {"service": "BigQuery", "cost": 18_500},
        {"service": "Cloud Storage", "cost": 12_800},
        {"service": "Networking", "cost": 9_600},
        {"service": "Pub/Sub", "cost": 6_200},
        {"service": "Cloud Functions", "cost": 4_100},
        {"service": "Monitoring", "cost": 3_800},
        {"service": "Other", "cost": 2_900},
    ]

    # Data table: top customers
    top_customers = [
        {
            "company": "Meridian Corp",
            "plan": "Enterprise",
            "mrr": "$12,400",
            "users": 320,
            "health": "Excellent",
            "since": "2022-03",
        },
        {
            "company": "Atlas Dynamics",
            "plan": "Enterprise",
            "mrr": "$9,800",
            "users": 245,
            "health": "Good",
            "since": "2022-07",
        },
        {
            "company": "Helix Systems",
            "plan": "Enterprise",
            "mrr": "$8,200",
            "users": 198,
            "health": "Excellent",
            "since": "2021-11",
        },
        {
            "company": "Quantum Forge",
            "plan": "Mid-Market",
            "mrr": "$5,600",
            "users": 87,
            "health": "At Risk",
            "since": "2023-01",
        },
        {
            "company": "Prism AI",
            "plan": "Mid-Market",
            "mrr": "$4,900",
            "users": 72,
            "health": "Good",
            "since": "2023-04",
        },
        {
            "company": "Bolt Analytics",
            "plan": "Mid-Market",
            "mrr": "$4,200",
            "users": 65,
            "health": "Good",
            "since": "2022-09",
        },
        {
            "company": "NovaTech Ltd",
            "plan": "Startup",
            "mrr": "$1,800",
            "users": 24,
            "health": "Excellent",
            "since": "2023-08",
        },
        {
            "company": "CloudBridge",
            "plan": "SMB",
            "mrr": "$980",
            "users": 15,
            "health": "Good",
            "since": "2024-01",
        },
    ]

    # =================================================================
    # REPORT
    # =================================================================

    report = Report(
        title="NovaPulse — Annual Analytics Review",
        subtitle="Comprehensive platform metrics • FY 2025 • Confidential",
        theme="dark",
        logo_url="https://api.dicebear.com/7.x/shapes/svg?seed=novapulse&size=40",
    )

    # ── Hero Section ─────────────────────────────────────────────────
    report.add(
        Markdown(
            content=(
                "# 📊 NovaPulse Annual Review\n\n"
                "Welcome to the **NovaPulse FY 2025 Annual Analytics Review**. "
                "This dashboard provides a comprehensive view of platform performance, "
                "customer health, infrastructure utilisation, and team velocity across "
                "all business units.\n\n"
                "> *Generated with [HolySheet](https://github.com/UnicoLab/HolySheet) v0.2.0 "
                "— Python-first report compiler for interactive dashboards.*"
            )
        )
    )

    # ── Alert: headline achievement ──────────────────────────────────
    report.add(
        Alert(
            severity="success",
            title="🎉 Milestone Reached",
            message=(
                "NovaPulse crossed 42,000 monthly active users in December, "
                "exceeding the annual target of 35,000 by 20%."
            ),
        )
    )

    # ── KPI Row ──────────────────────────────────────────────────────
    report.add(Divider(label="Key Performance Indicators"))

    report.add(
        Columns(
            children=[
                KPI(
                    label="Annual Revenue",
                    value="$2.26M",
                    delta="+34.2%",
                    status="positive",
                    description="vs. $1.68M last year",
                ),
                KPI(
                    label="Active Users",
                    value="42,000",
                    delta="+72%",
                    status="positive",
                    description="Monthly active users",
                ),
                KPI(
                    label="Net Revenue Retention",
                    value="127%",
                    delta="+8pp",
                    status="positive",
                    description="Dollar-based NRR",
                ),
                KPI(
                    label="Churn Rate",
                    value="2.1%",
                    delta="-0.6pp",
                    status="positive",
                    description="Monthly logo churn",
                ),
            ]
        )
    )

    # ── Compact Metrics Row ──────────────────────────────────────────
    report.add(
        Columns(
            children=[
                Metric(label="Avg. Deal Size", value="$4,850", unit="USD"),
                Metric(label="LTV:CAC Ratio", value="5.2x"),
                Metric(label="Median Onboarding", value="3.4", unit="days"),
                Metric(label="NPS Score", value="72"),
            ]
        )
    )

    # ── Revenue Section ──────────────────────────────────────────────
    report.add(Divider())

    report.add(
        Section(
            title="💰 Revenue Analytics",
            description="Monthly revenue breakdown with year-over-year trends.",
            children=[
                Tabs(
                    tabs=[
                        {
                            "label": "📈 Revenue Trend",
                            "children": [
                                LineChart(
                                    title="Monthly Revenue, Costs & Profit",
                                    data=monthly_revenue,
                                    x="month",
                                    y=["revenue", "costs", "profit"],
                                    height=420,
                                ),
                            ],
                        },
                        {
                            "label": "📊 By Product",
                            "children": [
                                BarChart(
                                    title="Revenue by Product — Q3 vs Q4",
                                    data=revenue_by_product,
                                    x="product",
                                    y=["q3", "q4"],
                                    height=400,
                                ),
                            ],
                        },
                        {
                            "label": "🍩 By Segment",
                            "children": [
                                PieChart(
                                    title="Revenue Distribution by Customer Segment",
                                    data=revenue_by_segment,
                                    name="segment",
                                    value="revenue",
                                    height=400,
                                ),
                            ],
                        },
                    ]
                ),
            ],
        )
    )

    # ── Growth Section ───────────────────────────────────────────────
    report.add(
        Section(
            title="🚀 User Growth & Engagement",
            description="Platform adoption, user growth curves, and conversion funnel.",
            children=[
                AreaChart(
                    title="Active Users & New Sign-ups",
                    data=user_growth,
                    x="month",
                    y=["active_users", "new_signups"],
                    height=380,
                ),
                Divider(label="Conversion Funnel"),
                FunnelChart(
                    title="Sign-up to Paid Conversion Pipeline",
                    data=funnel_data,
                    name="stage",
                    value="count",
                ),
            ],
        )
    )

    # ── Product & Feature Analytics ──────────────────────────────────
    report.add(Divider(label="Product Intelligence"))

    report.add(
        Columns(
            children=[
                ScatterChart(
                    title="Feature Usage vs. Satisfaction",
                    data=feature_scatter,
                    x="usage_pct",
                    y="satisfaction",
                    size="users",
                ),
                RadarChart(
                    title="Team Performance Comparison",
                    data=radar_data,
                    indicators=["velocity", "quality", "collaboration", "innovation", "delivery"],
                ),
            ]
        )
    )

    # ── Infrastructure ───────────────────────────────────────────────
    report.add(
        Section(
            title="🖥️ Infrastructure & Operations",
            description="Cloud spend breakdown, system health, and SLA performance.",
            children=[
                TreemapChart(
                    title="Monthly Cloud Infrastructure Costs",
                    data=treemap_data,
                    name="service",
                    value="cost",
                ),
                Divider(),
                Alert(
                    severity="warning",
                    title="Cost Alert",
                    message=(
                        "Compute costs increased 18% month-over-month in December. "
                        "Consider reviewing autoscaling policies for the inference cluster."
                    ),
                ),
                Columns(
                    children=[
                        GaugeChart(
                            title="API Uptime (SLA)",
                            value=99.97,
                            min=99.0,
                            max=100.0,
                            unit="%",
                        ),
                        GaugeChart(
                            title="Avg Response Time",
                            value=142,
                            min=0,
                            max=500,
                            unit="ms",
                        ),
                        GaugeChart(
                            title="Error Rate",
                            value=0.12,
                            min=0,
                            max=5,
                            unit="%",
                        ),
                    ]
                ),
                Divider(),
                Columns(
                    children=[
                        ProgressBar(
                            label="CPU Utilisation",
                            value=73,
                            description="18 / 24 vCPUs allocated",
                        ),
                        ProgressBar(
                            label="Memory Usage",
                            value=61,
                            description="49 GB / 80 GB",
                        ),
                        ProgressBar(
                            label="Disk I/O",
                            value=42,
                            description="Healthy throughput",
                        ),
                        ProgressBar(
                            label="Network Bandwidth",
                            value=88,
                            description="Approaching limit — consider upgrade",
                        ),
                    ]
                ),
            ],
        )
    )

    # ── Customer Data Table ──────────────────────────────────────────
    report.add(Divider(label="Customer Intelligence"))

    report.add(
        DataTable(
            title="Top Accounts by MRR",
            data=top_customers,
        )
    )

    # ── Alerts ───────────────────────────────────────────────────────
    report.add(Divider())

    report.add(
        Alert(
            severity="info",
            title="Upcoming Renewal Cycle",
            message=(
                "12 Enterprise accounts are up for renewal in Q1 2026. "
                "Account health scores are attached in the appendix."
            ),
        )
    )

    report.add(
        Alert(
            severity="error",
            title="Action Required",
            message=(
                "Quantum Forge (MRR $5,600) has been flagged as 'At Risk'. "
                "Usage dropped 34% in the last 30 days. Escalate to CS team."
            ),
        )
    )

    # ── Image block ──────────────────────────────────────────────────
    report.add(
        Image(
            src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",
            alt="Data Visualization Dashboard",
            caption="NovaPulse Platform — Live Dashboard View",
        )
    )

    # ── Code Block ───────────────────────────────────────────────────
    report.add(Divider(label="Developer Resources"))

    report.add(
        CodeBlock(
            code=(
                "from holysheet import Report, KPI, LineChart\n\n"
                "# Create a report in 3 lines\n"
                "report = Report(title='Q4 Metrics', theme='dark')\n"
                "report.add(KPI(label='Revenue', value='$258K', delta='+12%', status='positive'))\n"
                "report.add(LineChart(title='Trend', data=monthly_data, x='month', y='revenue'))\n\n"
                "# Export to a single portable HTML file\n"
                "report.export_html('q4_report.html')\n"
                "print('Done! Open q4_report.html in any browser.')"
            ),
            language="python",
            title="Quick Start — Generate a Report in 10 Lines",
        )
    )

    # =================================================================
    # NEW CHARTS (v0.3.0)
    # =================================================================

    report.add(Divider(label="🔥 Advanced Charts"))

    # Heatmap
    heatmap_data = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours = ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm"]
    import random

    random.seed(42)
    for day in days:
        for hour in hours:
            heatmap_data.append({"day": day, "hour": hour, "visits": random.randint(10, 200)})

    report.add(
        HeatmapChart(
            title="Website Traffic Heatmap",
            data=heatmap_data,
            x="hour",
            y="day",
            value="visits",
            height=320,
        )
    )

    # Candlestick
    candlestick_data = [
        {"date": "2024-01", "open": 142.5, "close": 148.3, "low": 138.2, "high": 150.1},
        {"date": "2024-02", "open": 148.3, "close": 155.7, "low": 145.0, "high": 158.4},
        {"date": "2024-03", "open": 155.7, "close": 149.8, "low": 146.3, "high": 159.2},
        {"date": "2024-04", "open": 149.8, "close": 162.4, "low": 148.1, "high": 165.0},
        {"date": "2024-05", "open": 162.4, "close": 158.1, "low": 154.2, "high": 167.8},
        {"date": "2024-06", "open": 158.1, "close": 172.3, "low": 155.9, "high": 175.4},
        {"date": "2024-07", "open": 172.3, "close": 168.9, "low": 164.7, "high": 178.2},
        {"date": "2024-08", "open": 168.9, "close": 181.2, "low": 166.3, "high": 185.0},
    ]
    report.add(
        Columns(
            children=[
                CandlestickChart(title="AAPL Stock Price (OHLC)", data=candlestick_data, x="date"),
                SankeyChart(
                    title="Revenue Flow",
                    nodes=[
                        {"name": "Product Sales"},
                        {"name": "Services"},
                        {"name": "Licensing"},
                        {"name": "North America"},
                        {"name": "Europe"},
                        {"name": "Asia Pacific"},
                        {"name": "Net Revenue"},
                    ],
                    links=[
                        {"source": "Product Sales", "target": "North America", "value": 450},
                        {"source": "Product Sales", "target": "Europe", "value": 280},
                        {"source": "Product Sales", "target": "Asia Pacific", "value": 180},
                        {"source": "Services", "target": "North America", "value": 200},
                        {"source": "Services", "target": "Europe", "value": 150},
                        {"source": "Licensing", "target": "North America", "value": 120},
                        {"source": "Licensing", "target": "Asia Pacific", "value": 80},
                        {"source": "North America", "target": "Net Revenue", "value": 770},
                        {"source": "Europe", "target": "Net Revenue", "value": 430},
                        {"source": "Asia Pacific", "target": "Net Revenue", "value": 260},
                    ],
                ),
            ]
        )
    )

    # Waterfall + BoxPlot
    report.add(
        Columns(
            children=[
                WaterfallChart(
                    title="Revenue Bridge Q3 → Q4",
                    data=[
                        {"item": "Q3 Revenue", "amount": 1850},
                        {"item": "New Customers", "amount": 420},
                        {"item": "Upsells", "amount": 180},
                        {"item": "Churn", "amount": -210},
                        {"item": "Price Increase", "amount": 95},
                        {"item": "Refunds", "amount": -45},
                    ],
                    category="item",
                    value="amount",
                ),
                BoxPlotChart(
                    title="Response Time Distribution (ms)",
                    data=[
                        [12, 45, 68, 120, 250],
                        [8, 32, 55, 95, 180],
                        [15, 52, 82, 145, 310],
                        [10, 38, 61, 105, 220],
                    ],
                    categories=["API v1", "API v2", "GraphQL", "WebSocket"],
                ),
            ]
        )
    )

    # Geo Scatter
    report.add(
        MapChart(
            title="Global User Distribution",
            data=[
                {"lat": 40.7, "lng": -74.0, "users": 45000, "city": "New York"},
                {"lat": 51.5, "lng": -0.1, "users": 38000, "city": "London"},
                {"lat": 48.9, "lng": 2.3, "users": 28000, "city": "Paris"},
                {"lat": 35.7, "lng": 139.7, "users": 32000, "city": "Tokyo"},
                {"lat": 37.8, "lng": -122.4, "users": 41000, "city": "San Francisco"},
                {"lat": -33.9, "lng": 151.2, "users": 18000, "city": "Sydney"},
                {"lat": 1.3, "lng": 103.8, "users": 22000, "city": "Singapore"},
                {"lat": 55.8, "lng": 37.6, "users": 15000, "city": "Moscow"},
            ],
            lat="lat",
            lng="lng",
            value="users",
            name="city",
        )
    )

    # =================================================================
    # NEW CONTENT BLOCKS (v0.3.0)
    # =================================================================

    report.add(Divider(label="📋 Content & Display"))

    # Timeline
    report.add(
        Timeline(
            title="Product Roadmap 2024",
            events=[
                {
                    "date": "Jan 2024",
                    "title": "v1.0 Launch",
                    "description": "Initial public release with core features",
                    "color": "#22c55e",
                },
                {
                    "date": "Mar 2024",
                    "title": "v1.5 Charts",
                    "description": "Added 9 chart types powered by ECharts",
                    "color": "#6366f1",
                },
                {
                    "date": "Jun 2024",
                    "title": "v2.0 Interactive",
                    "description": "Sliders, toggles, dropdowns for interactive dashboards",
                    "color": "#f59e0b",
                },
                {
                    "date": "Sep 2024",
                    "title": "v3.0 Pro",
                    "description": "21 new block types, Sankey charts, timelines, and more",
                    "color": "#ef4444",
                },
                {
                    "date": "Dec 2024",
                    "title": "v4.0 Enterprise",
                    "description": "Real-time data, custom themes, plugin system",
                    "color": "#8b5cf6",
                },
            ],
        )
    )

    # Callout + UserCards
    report.add(
        Columns(
            children=[
                Callout(
                    content="The best dashboards tell a story. With HolySheet, your data becomes narrative.",
                    author="Product Team",
                    variant="quote",
                    icon="💡",
                ),
                Callout(
                    content="47 block types. 3 themes. Zero Node.js required.",
                    variant="highlight",
                ),
            ]
        )
    )

    report.add(
        Columns(
            children=[
                UserCard(
                    name="Alice Chen",
                    role="Chief Data Officer",
                    email="alice@novapulse.io",
                    stats=[
                        {"label": "Reports", "value": "142"},
                        {"label": "Dashboards", "value": "38"},
                    ],
                ),
                UserCard(
                    name="Marcus Johnson",
                    role="VP Engineering",
                    email="marcus@novapulse.io",
                    stats=[
                        {"label": "Deployments", "value": "1.2K"},
                        {"label": "Uptime", "value": "99.97%"},
                    ],
                ),
                UserCard(
                    name="Sarah Kim",
                    role="Head of Analytics",
                    email="sarah@novapulse.io",
                    stats=[
                        {"label": "Queries/day", "value": "45K"},
                        {"label": "Models", "value": "67"},
                    ],
                ),
            ]
        )
    )

    # Status List + Info List
    report.add(
        Columns(
            children=[
                StatusList(
                    title="Service Health",
                    items=[
                        {
                            "label": "API Gateway",
                            "status": "success",
                            "value": "12ms",
                            "description": "All endpoints responding",
                        },
                        {
                            "label": "PostgreSQL",
                            "status": "success",
                            "value": "3ms",
                            "description": "Primary + 2 replicas",
                        },
                        {
                            "label": "Redis Cache",
                            "status": "warning",
                            "value": "85%",
                            "description": "Memory usage elevated",
                        },
                        {
                            "label": "ML Pipeline",
                            "status": "error",
                            "value": "DOWN",
                            "description": "Model retraining failed",
                        },
                        {
                            "label": "CDN",
                            "status": "success",
                            "value": "99.99%",
                            "description": "Global edge nodes",
                        },
                        {
                            "label": "Email Service",
                            "status": "pending",
                            "value": "Queue: 142",
                            "description": "Backlog processing",
                        },
                    ],
                ),
                InfoList(
                    title="System Configuration",
                    items=[
                        {"key": "Environment", "value": "Production", "icon": "🌐"},
                        {"key": "Region", "value": "us-east-1", "icon": "📍"},
                        {"key": "Python", "value": "3.12.4", "icon": "🐍"},
                        {"key": "HolySheet", "value": "0.3.0", "icon": "📊"},
                        {"key": "Database", "value": "PostgreSQL 16.2", "icon": "🗄️"},
                        {"key": "Cache", "value": "Redis 7.2", "icon": "⚡"},
                        {"key": "Last Deploy", "value": "2024-12-15 14:32 UTC", "icon": "🚀"},
                    ],
                ),
            ]
        )
    )

    # Stepper
    report.add(
        Stepper(
            title="Deployment Pipeline",
            steps=[
                {"label": "Build", "description": "Compile & bundle", "status": "complete"},
                {"label": "Test", "description": "Unit + integration", "status": "complete"},
                {"label": "Security Scan", "description": "SAST + DAST", "status": "complete"},
                {"label": "Staging", "description": "Canary deploy", "status": "active"},
                {"label": "Production", "description": "Blue-green deploy", "status": "pending"},
            ],
            current_step=3,
        )
    )

    # Tags + Sparklines
    report.add(
        Columns(
            children=[
                TagList(
                    title="Technology Stack",
                    tags=[
                        {"label": "Python", "color": "#3776AB"},
                        {"label": "React", "color": "#61DAFB"},
                        {"label": "TypeScript", "color": "#3178C6"},
                        {"label": "PostgreSQL", "color": "#4169E1"},
                        {"label": "Redis", "color": "#DC382D"},
                        {"label": "Docker", "color": "#2496ED"},
                        {"label": "Kubernetes", "color": "#326CE5"},
                        {"label": "GraphQL", "color": "#E10098"},
                    ],
                ),
                Sparkline(data=[10, 25, 18, 35, 28, 42, 38, 55, 48, 62, 58, 75], color="#6C63FF"),
                Sparkline(data=[50, 45, 52, 48, 55, 42, 58, 62, 55, 68, 72, 80], color="#34d399"),
            ]
        )
    )

    # JSON Viewer
    report.add(
        JsonViewer(
            data={
                "report": {
                    "title": "NovaPulse Analytics",
                    "version": "0.3.0",
                    "blocks": 47,
                    "themes": ["dark", "light", "executive"],
                },
                "features": {
                    "charts": [
                        "line",
                        "bar",
                        "pie",
                        "heatmap",
                        "candlestick",
                        "sankey",
                        "waterfall",
                        "boxplot",
                    ],
                    "interactive": [
                        "slider",
                        "toggle",
                        "dropdown",
                        "checkbox",
                        "radio",
                        "text_input",
                    ],
                    "content": [
                        "timeline",
                        "callout",
                        "user_card",
                        "status_list",
                        "info_list",
                        "stepper",
                    ],
                },
                "performance": {
                    "render_time_ms": 42,
                    "bundle_size_kb": 549,
                    "lighthouse_score": 98,
                },
            },
            title="Report Configuration (JSON Viewer)",
            collapsed_depth=2,
        )
    )

    # =================================================================
    # NEW INTERACTIVE BLOCKS (v0.3.0)
    # =================================================================

    report.add(Divider(label="🎮 Interactive Controls"))

    report.add(
        Columns(
            children=[
                Dropdown(
                    label="Select Region",
                    options=[
                        {"label": "🇺🇸 North America", "value": "na"},
                        {"label": "🇪🇺 Europe", "value": "eu"},
                        {"label": "🌏 Asia Pacific", "value": "apac"},
                        {"label": "🌍 Middle East & Africa", "value": "mea"},
                        {"label": "🌎 Latin America", "value": "latam"},
                    ],
                    default_value="na",
                    description="Filter dashboard data by region",
                ),
                TextInput(
                    label="Search Reports",
                    placeholder="Type to search...",
                    description="Search across all reports and dashboards",
                ),
            ]
        )
    )

    report.add(
        Columns(
            children=[
                CheckboxGroup(
                    label="Dashboard Modules",
                    options=[
                        {"label": "Revenue Analytics", "value": "revenue"},
                        {"label": "User Metrics", "value": "users"},
                        {"label": "Infrastructure", "value": "infra"},
                        {"label": "Security Alerts", "value": "security"},
                    ],
                    default_values=["revenue", "users"],
                    description="Select modules to display",
                ),
                RadioGroup(
                    label="Time Range",
                    options=[
                        {"label": "Last 7 days", "value": "7d"},
                        {"label": "Last 30 days", "value": "30d"},
                        {"label": "Last 90 days", "value": "90d"},
                        {"label": "Year to date", "value": "ytd"},
                    ],
                    default_value="30d",
                    description="Select analysis period",
                ),
            ]
        )
    )

    # =================================================================
    # FOOTER
    # =================================================================

    report.add(Divider())
    report.add(
        Section(
            title="About This Dashboard",
            description="Auto-generated showcase of all HolySheet capabilities",
            children=[
                Markdown(
                    content=(
                        "This dashboard demonstrates all **47 block types** available in HolySheet v0.3.0:\n\n"
                        "**Charts (15):** Line, Area, Bar, Pie, Scatter, Radar, Gauge, Funnel, Treemap, "
                        "Heatmap, Candlestick, Sankey, Waterfall, BoxPlot, MapChart\n\n"
                        "**Content (14):** KPI, Metric, StatComparison, DataTable, Markdown, CodeBlock, "
                        "Image, Alert, ProgressBar, Timeline, Callout, JsonViewer, UserCard, Video\n\n"
                        "**Layout (7):** Section, Columns, Tabs, Accordion, Divider, Stepper, TagList\n\n"
                        "**Interactive (11):** Slider, NumberInput, Toggle, Dropdown, TextInput, "
                        "CheckboxGroup, RadioGroup, StatusList, InfoList, Sparkline, Embed\n\n"
                        "📄 MIT License • Built with ❤️ by UnicoLab"
                    )
                )
            ],
        )
    )

    # =================================================================
    # EXPORT
    # =================================================================

    output_path = report.export_html("full_showcase.html")
    print(f"✓ Exported: {output_path}")
    print(f"  Title:  {report.title}")
    print(f"  Theme:  {report.theme}")
    print(f"  Blocks: {len(report)} top-level blocks")
    print()
    print("Open full_showcase.html in any browser to view the dashboard.")


if __name__ == "__main__":
    main()
