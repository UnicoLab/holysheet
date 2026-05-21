#!/usr/bin/env python3
"""Basic HolySheet report example.

Creates a simple report with a few KPI cards and a line chart,
then exports it to HTML and JSON.
"""

from __future__ import annotations

from holysheet import KPI, LineChart, Markdown, Report


def main() -> None:
    """Build and export a basic report."""
    # Sample data
    monthly_data = [
        {"month": "Jan", "users": 1_200},
        {"month": "Feb", "users": 1_450},
        {"month": "Mar", "users": 1_830},
        {"month": "Apr", "users": 2_100},
        {"month": "May", "users": 2_540},
        {"month": "Jun", "users": 2_890},
    ]

    # Build the report
    report = Report(
        title="Basic Report",
        subtitle="A quick overview of key metrics",
        theme="light",
    )

    # Add a markdown intro
    report.add(
        Markdown(
            content=(
                "## Welcome\n\n"
                "This is a basic HolySheet report demonstrating KPI cards "
                "and a simple line chart."
            )
        )
    )

    # Add KPI cards
    report.add(KPI(label="Total Users", value="2,890", delta="+13.8%", status="positive"))
    report.add(KPI(label="Active Rate", value=78, delta="+2.1%", status="positive", unit="%"))
    report.add(KPI(label="Churn Rate", value="4.2%", delta="-0.5%", status="positive"))

    # Add a line chart
    report.add(
        LineChart(
            title="User Growth",
            data=monthly_data,
            x="month",
            y="users",
            height=400,
        )
    )

    # Export
    report.export_html("basic_report.html")
    report.export_json("basic_report.json")
    print("✓ Exported: basic_report.html, basic_report.json")


if __name__ == "__main__":
    main()
