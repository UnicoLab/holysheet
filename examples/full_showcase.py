#!/usr/bin/env python3
"""HolySheet v0.2.0 — Full showcase of all 21 block types.

This example generates a comprehensive dark-themed dashboard that demonstrates
every block type available in HolySheet. It uses realistic fake data for a
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
    PieChart,
    ProgressBar,
    RadarChart,
    Report,
    ScatterChart,
    Section,
    Tabs,
    TreemapChart,
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

    # ── Footer Markdown ──────────────────────────────────────────────
    report.add(Divider())

    report.add(
        Markdown(
            content=(
                "---\n\n"
                "**Report generated by [HolySheet](https://github.com/UnicoLab/HolySheet) v0.2.0** "
                "• Python-first report compiler for interactive React dashboards.\n\n"
                "*This showcase demonstrates all 21 block types available in HolySheet: "
                "KPI, Metric, GaugeChart, ProgressBar, LineChart, AreaChart, BarChart, PieChart, "
                "ScatterChart, RadarChart, FunnelChart, TreemapChart, DataTable, Markdown, "
                "CodeBlock, Image, Alert, Section, Columns, Tabs, and Divider.*\n\n"
                "📄 MIT License • Built with ❤️ by UnicoLab"
            )
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
