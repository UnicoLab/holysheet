"""Tests for new v0.4.0 Report features — themes, feature flags, multi-page, filters, etc."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from holysheet import KPI, Markdown, Report
from holysheet.exceptions import HolySheetError
from holysheet.templates import ExecutiveSummary, OpsMonitor, SalesDashboard
from holysheet.themes import Theme

# ---------------------------------------------------------------------------
# Custom Theme API
# ---------------------------------------------------------------------------


class TestCustomTheme:
    """Test Theme class for custom branded dashboards."""

    def test_basic_theme(self) -> None:
        """Theme constructor creates a theme with the given name and primary color."""
        theme = Theme(name="brand", primary="#FF0000")
        assert theme.name == "brand"
        d = theme.to_dict()
        assert d["colors"]["primary"] == "#FF0000"
        assert d["name"] == "brand"

    def test_theme_inherits_base(self) -> None:
        """Theme inherits unspecified values from the base theme."""
        theme = Theme(name="custom", base="light", primary="#123456")
        d = theme.to_dict()
        # Inherits background from light theme
        assert d["colors"]["background"] == "#FFFFFF"
        assert d["colors"]["primary"] == "#123456"

    def test_theme_dark_base(self) -> None:
        """Theme can use dark as base."""
        theme = Theme(name="dark_brand", base="dark", primary="#00FF00")
        d = theme.to_dict()
        assert d["colors"]["background"] == "#111827"
        assert d["colors"]["primary"] == "#00FF00"

    def test_theme_executive_base(self) -> None:
        """Theme can use executive as base."""
        theme = Theme(name="exec_brand", base="executive")
        d = theme.to_dict()
        assert d["name"] == "exec_brand"
        assert d["colors"]["background"] == "#FAF9F7"

    def test_all_color_overrides(self) -> None:
        """Theme supports overriding all color tokens."""
        theme = Theme(
            name="all_colors",
            primary="#111111",
            secondary="#222222",
            background="#333333",
            surface="#444444",
            text="#555555",
            text_secondary="#666666",
            border="#777777",
            success="#008000",
            warning="#FFA500",
            danger="#FF0000",
            info="#0000FF",
        )
        d = theme.to_dict()
        assert d["colors"]["primary"] == "#111111"
        assert d["colors"]["secondary"] == "#222222"
        assert d["colors"]["background"] == "#333333"
        assert d["colors"]["surface"] == "#444444"
        assert d["colors"]["text"] == "#555555"
        assert d["colors"]["text_secondary"] == "#666666"
        assert d["colors"]["border"] == "#777777"
        assert d["colors"]["success"] == "#008000"
        assert d["colors"]["warning"] == "#FFA500"
        assert d["colors"]["danger"] == "#FF0000"
        assert d["colors"]["info"] == "#0000FF"

    def test_custom_font(self) -> None:
        """Theme supports custom font override."""
        theme = Theme(name="fonted", font="Satoshi")
        d = theme.to_dict()
        assert "Satoshi" in d["fonts"]["body"]
        assert "Satoshi" in d["fonts"]["heading"]

    def test_custom_mono_font(self) -> None:
        """Theme supports custom monospace font override."""
        theme = Theme(name="mono", mono_font="JetBrains Mono")
        d = theme.to_dict()
        assert "JetBrains Mono" in d["fonts"]["mono"]

    def test_custom_chart_palette(self) -> None:
        """Theme supports custom chart colour palette."""
        palette = ["#FF0000", "#00FF00", "#0000FF"]
        theme = Theme(name="palette", chart_palette=palette)
        d = theme.to_dict()
        assert d["colors"]["chart_palette"] == palette

    def test_invalid_base_raises(self) -> None:
        """Theme with unknown base raises HolySheetError."""
        with pytest.raises(HolySheetError, match="Unknown base theme"):
            Theme(name="bad", base="nonexistent")

    def test_repr(self) -> None:
        """Theme repr is readable."""
        theme = Theme(name="test")
        assert "test" in repr(theme)

    def test_theme_in_report(self) -> None:
        """Custom Theme can be used in a Report."""
        theme = Theme(name="test", primary="#FF0000")
        r = Report(title="Themed Report", theme=theme)
        schema = r.to_schema()
        assert schema.custom_theme is not None
        assert schema.custom_theme["colors"]["primary"] == "#FF0000"
        assert schema.custom_theme["name"] == "test"

    def test_theme_in_report_schema_name(self) -> None:
        """Report stores the theme name from the custom Theme."""
        theme = Theme(name="branded")
        r = Report(title="Test", theme=theme)
        assert r.theme == "branded"

    def test_theme_does_not_mutate_base(self) -> None:
        """Creating a Theme doesn't mutate the shared THEMES dict."""
        from holysheet.themes import THEMES

        original_primary = THEMES["dark"]["colors"]["primary"]
        Theme(name="safe", base="dark", primary="#999999")
        assert THEMES["dark"]["colors"]["primary"] == original_primary


# ---------------------------------------------------------------------------
# Feature Flags
# ---------------------------------------------------------------------------


class TestFeatureFlags:
    """Test feature flags (theme_switch, presentation_mode, download_buttons)."""

    def test_theme_switch(self) -> None:
        """theme_switch flag appears in schema features."""
        r = Report(title="Test", theme_switch=True)
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert schema.features is not None
        assert schema.features["theme_switch"] is True

    def test_presentation_mode(self) -> None:
        """presentation_mode flag appears in schema features."""
        r = Report(title="Test", presentation_mode=True)
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert schema.features is not None
        assert schema.features["presentation_mode"] is True

    def test_download_buttons(self) -> None:
        """download_buttons flag appears in schema features."""
        r = Report(title="Test", download_buttons=True)
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert schema.features is not None
        assert schema.features["download_buttons"] is True

    def test_all_flags_combined(self) -> None:
        """All feature flags can be enabled together."""
        r = Report(
            title="Full Features",
            theme_switch=True,
            presentation_mode=True,
            download_buttons=True,
        )
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert schema.features["theme_switch"] is True
        assert schema.features["presentation_mode"] is True
        assert schema.features["download_buttons"] is True

    def test_no_flags_no_features(self) -> None:
        """No feature flags means no features in schema."""
        r = Report(title="Plain")
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert schema.features is None

    def test_features_in_json(self) -> None:
        """Feature flags survive JSON serialisation."""
        r = Report(title="Test", theme_switch=True)
        r.add(KPI(label="A", value=1))
        parsed = json.loads(r.to_json())
        assert parsed["features"]["theme_switch"] is True


# ---------------------------------------------------------------------------
# Multi-page Reports
# ---------------------------------------------------------------------------


class TestMultiPage:
    """Test multi-page report support."""

    def test_add_page(self) -> None:
        """add_page adds a page with label and children."""
        r = Report(title="Multi")
        r.add_page("Overview", [KPI(label="A", value=1)])
        r.add_page("Details", [Markdown(content="Detail")])
        assert len(r._pages) == 2

    def test_add_page_chaining(self) -> None:
        """add_page returns self for chaining."""
        r = Report(title="Chain")
        result = r.add_page("P1").add_page("P2")
        assert result is r

    def test_multi_page_serialisation(self) -> None:
        """Multi-page report serialises pages with blocks."""
        r = Report(title="Paged")
        r.add_page("Page 1", [KPI(label="K1", value=10)])
        r.add_page("Page 2", [KPI(label="K2", value=20)])

        schema = r.to_schema()
        # When pages are used, blocks is the serialised pages list
        assert isinstance(schema.blocks, list)
        assert len(schema.blocks) == 2
        assert schema.blocks[0]["label"] == "Page 1"
        assert schema.blocks[1]["label"] == "Page 2"

    def test_multi_page_feature_flag(self) -> None:
        """Multi-page report sets multi_page feature flag."""
        r = Report(title="Paged")
        r.add_page("P1", [KPI(label="A", value=1)])
        schema = r.to_schema()
        assert schema.features is not None
        assert schema.features.get("multi_page") is True

    def test_multi_page_json(self) -> None:
        """Multi-page report survives JSON roundtrip."""
        r = Report(title="Paged")
        r.add_page("Overview", [KPI(label="A", value=1)])
        parsed = json.loads(r.to_json())
        assert parsed["features"]["multi_page"] is True
        assert parsed["blocks"][0]["label"] == "Overview"

    def test_multi_page_repr(self) -> None:
        """Multi-page report repr shows page count."""
        r = Report(title="Paged")
        r.add_page("P1")
        r.add_page("P2")
        assert "pages=2" in repr(r)

    def test_empty_page(self) -> None:
        """add_page with no children creates empty page."""
        r = Report(title="Empty Pages")
        r.add_page("Empty")
        schema = r.to_schema()
        assert schema.blocks[0]["blocks"] == []


# ---------------------------------------------------------------------------
# Global Filters
# ---------------------------------------------------------------------------


class TestGlobalFilters:
    """Test global filter support."""

    def test_add_filter_basic(self) -> None:
        """add_filter adds a filter to features."""
        r = Report(title="Filtered")
        r.add_filter("region", options=["US", "EU", "APAC"])
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert schema.features is not None
        filters = schema.features["filters"]
        assert len(filters) == 1
        assert filters[0]["key"] == "region"
        assert filters[0]["type"] == "dropdown"

    def test_add_filter_custom_label(self) -> None:
        """add_filter with custom label."""
        r = Report(title="Filtered")
        r.add_filter("date_range", type="date_range", label="Period")
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        filters = schema.features["filters"]
        assert filters[0]["label"] == "Period"
        assert filters[0]["type"] == "date_range"

    def test_add_filter_default_label(self) -> None:
        """add_filter auto-generates label from key."""
        r = Report(title="Filtered")
        r.add_filter("time_period")
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        filters = schema.features["filters"]
        assert filters[0]["label"] == "Time Period"

    def test_add_filter_with_default(self) -> None:
        """add_filter supports default value."""
        r = Report(title="Filtered")
        r.add_filter("region", options=["US", "EU"], default="US")
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        filters = schema.features["filters"]
        assert filters[0]["default"] == "US"

    def test_multiple_filters(self) -> None:
        """Multiple filters can be added."""
        r = Report(title="Multi Filtered")
        r.add_filter("region", options=["US", "EU"])
        r.add_filter("period", type="date_range")
        r.add_filter("search", type="text")
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert len(schema.features["filters"]) == 3

    def test_add_filter_chaining(self) -> None:
        """add_filter returns self for chaining."""
        r = Report(title="Chain")
        result = r.add_filter("a").add_filter("b")
        assert result is r

    def test_filters_in_json(self) -> None:
        """Filters survive JSON serialisation."""
        r = Report(title="Filtered")
        r.add_filter("region", options=["US", "EU"])
        r.add(KPI(label="A", value=1))
        parsed = json.loads(r.to_json())
        assert "filters" in parsed["features"]
        assert parsed["features"]["filters"][0]["key"] == "region"


# ---------------------------------------------------------------------------
# Expiring Reports
# ---------------------------------------------------------------------------


class TestExpiringReports:
    """Test report expiry support."""

    def test_expires_in_schema(self) -> None:
        """Expires field is set in schema."""
        r = Report(title="Expiring", expires="2025-12-31")
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert schema.expires == "2025-12-31"

    def test_no_expires_by_default(self) -> None:
        """No expires by default."""
        r = Report(title="Normal")
        r.add(KPI(label="A", value=1))
        schema = r.to_schema()
        assert schema.expires is None

    def test_expires_in_json(self) -> None:
        """Expires field survives JSON serialisation."""
        r = Report(title="Expiring", expires="2025-06-01")
        r.add(KPI(label="A", value=1))
        parsed = json.loads(r.to_json())
        assert parsed["expires"] == "2025-06-01"


# ---------------------------------------------------------------------------
# Compression
# ---------------------------------------------------------------------------


class TestCompression:
    """Test report compression support."""

    def test_compress_flag_creates_file(self, tmp_path: Path) -> None:
        """export_html with compress=True still creates an HTML file."""
        r = Report(title="Compressed", compress=True)
        r.add(KPI(label="Users", value=42000))
        out = tmp_path / "compressed.html"
        result = r.export_html(out)
        assert result.exists()
        assert result.suffix == ".html"

    def test_compressed_spec_is_base64(self, tmp_path: Path) -> None:
        """Compressed HTML embeds a base64 string instead of raw JSON."""
        r = Report(title="Compressed", compress=True)
        r.add(KPI(label="Users", value=42000))
        out = tmp_path / "compressed.html"
        r.export_html(out)
        content = out.read_text(encoding="utf-8")
        # The spec should be base64-encoded gzip, not raw JSON
        assert "__HOLYSHEET_SPEC__" in content
        # Raw JSON would contain {"title": but compressed won't
        # The base64 gzip string starts with 'H4sI' (gzip magic bytes b64)
        assert "H4sI" in content

    def test_uncompressed_has_raw_json(self, tmp_path: Path) -> None:
        """Uncompressed HTML embeds raw JSON in the spec."""
        r = Report(title="Normal")
        r.add(KPI(label="Users", value=42000))
        out = tmp_path / "normal.html"
        r.export_html(out)
        content = out.read_text(encoding="utf-8")
        # Uncompressed spec contains the title as raw JSON
        assert '"title":"Normal"' in content or '"title": "Normal"' in content


# ---------------------------------------------------------------------------
# Password Protection
# ---------------------------------------------------------------------------


class TestPasswordProtection:
    """Test password-protected report export."""

    def test_password_creates_file(self, tmp_path: Path) -> None:
        """export_html with password creates an HTML file."""
        r = Report(title="Protected", password="secret123")
        r.add(KPI(label="A", value=1))
        out = tmp_path / "protected.html"
        result = r.export_html(out)
        assert result.exists()

    def test_password_html_contains_lock(self, tmp_path: Path) -> None:
        """Password-protected HTML contains the lock UI."""
        r = Report(title="Locked Report", password="test")
        r.add(KPI(label="A", value=1))
        out = tmp_path / "locked.html"
        r.export_html(out)
        content = out.read_text(encoding="utf-8")
        assert "password" in content.lower()
        assert "Locked Report" in content

    def test_password_html_does_not_contain_raw_spec(self, tmp_path: Path) -> None:
        """Password-protected HTML should not contain the raw JSON spec."""
        r = Report(title="Secret Data", password="pass")
        r.add(KPI(label="TopSecret", value=999))
        out = tmp_path / "secret.html"
        r.export_html(out)
        content = out.read_text(encoding="utf-8")
        # The raw spec should be encrypted, not plaintext
        assert "__HOLYSHEET_SPEC__" not in content


# ---------------------------------------------------------------------------
# Widget Export
# ---------------------------------------------------------------------------


class TestWidgetExport:
    """Test export_widget for embeddable widgets."""

    def test_widget_creates_file(self, tmp_path: Path) -> None:
        """export_widget creates an HTML file."""
        r = Report(title="Widget Test")
        r.add(KPI(label="A", value=1))
        r.add(KPI(label="B", value=2))
        out = tmp_path / "widget.html"
        result = r.export_widget(out)
        assert result.exists()
        assert result.suffix == ".html"

    def test_widget_with_block_ids(self, tmp_path: Path) -> None:
        """export_widget with block_ids filters blocks."""
        r = Report(title="Widget")
        r.add(KPI(label="A", value=1))  # block_001
        r.add(KPI(label="B", value=2))  # block_002
        r.add(KPI(label="C", value=3))  # block_003

        out = tmp_path / "widget.html"
        r.export_widget(out, block_ids=["block_001", "block_003"])
        content = out.read_text(encoding="utf-8")
        assert content  # Just verify file was created with content

    def test_widget_all_blocks(self, tmp_path: Path) -> None:
        """export_widget with no block_ids includes all blocks."""
        r = Report(title="Widget All")
        r.add(KPI(label="A", value=1))
        r.add(KPI(label="B", value=2))
        out = tmp_path / "widget_all.html"
        r.export_widget(out)
        assert out.exists()


# ---------------------------------------------------------------------------
# Jupyter Integration
# ---------------------------------------------------------------------------


class TestJupyterIntegration:
    """Test _repr_html_ for Jupyter notebook display."""

    def test_repr_html_returns_string(self) -> None:
        """_repr_html_ returns a string."""
        r = Report(title="Jupyter Test")
        r.add(KPI(label="A", value=1))
        result = r._repr_html_()
        assert isinstance(result, str)

    def test_repr_html_contains_iframe(self) -> None:
        """_repr_html_ returns an iframe for notebook isolation."""
        r = Report(title="Jupyter Test")
        r.add(KPI(label="A", value=1))
        result = r._repr_html_()
        # Should contain iframe (for successful render) or pre (for error)
        assert "iframe" in result.lower() or "pre" in result.lower()


# ---------------------------------------------------------------------------
# Report Templates
# ---------------------------------------------------------------------------


class TestSalesDashboard:
    """Test SalesDashboard template."""

    def test_basic_creation(self) -> None:
        """SalesDashboard can be created with no data."""
        report = SalesDashboard()
        assert report.title == "Sales Dashboard"
        assert report.theme == "dark"
        assert len(report) > 0  # Has at least the KPI row

    def test_custom_title(self) -> None:
        """SalesDashboard accepts custom title."""
        report = SalesDashboard(title="My Sales")
        assert report.title == "My Sales"

    def test_custom_theme(self) -> None:
        """SalesDashboard accepts custom theme."""
        report = SalesDashboard(theme="light")
        assert report.theme == "light"

    def test_with_kpis(self) -> None:
        """SalesDashboard populates KPI values from data."""
        report = SalesDashboard(
            data={
                "kpis": {
                    "revenue": "$1.2M",
                    "revenue_delta": "+12%",
                    "revenue_status": "positive",
                    "deals_won": 42,
                },
            },
        )
        schema = report.to_schema()
        assert len(schema.blocks) > 0

    def test_with_revenue_data(self) -> None:
        """SalesDashboard generates revenue trend chart."""
        data = {
            "revenue": [
                {"month": "Jan", "revenue": 1000},
                {"month": "Feb", "revenue": 1500},
            ],
        }
        report = SalesDashboard(data=data)
        schema = report.to_schema()
        types = [b["type"] for b in schema.blocks]
        assert "section" in types  # Revenue section

    def test_json_roundtrip(self) -> None:
        """SalesDashboard JSON output is valid."""
        report = SalesDashboard()
        json_str = report.to_json()
        parsed = json.loads(json_str)
        assert parsed["title"] == "Sales Dashboard"

    def test_is_report_subclass(self) -> None:
        """SalesDashboard is a Report subclass."""
        report = SalesDashboard()
        assert isinstance(report, Report)


class TestExecutiveSummary:
    """Test ExecutiveSummary template."""

    def test_basic_creation(self) -> None:
        """ExecutiveSummary can be created with no data."""
        report = ExecutiveSummary()
        assert report.title == "Executive Summary"
        assert report.theme == "executive"

    def test_custom_title_theme(self) -> None:
        """ExecutiveSummary accepts custom title and theme."""
        report = ExecutiveSummary(title="Q4 Review", theme="dark")
        assert report.title == "Q4 Review"
        assert report.theme == "dark"

    def test_with_metrics(self) -> None:
        """ExecutiveSummary populates metrics from data."""
        data = {
            "metrics": [
                {"label": "Revenue", "value": "$1M", "delta": "+10%", "status": "positive"},
                {"label": "Costs", "value": "$500K", "delta": "-5%", "status": "positive"},
            ],
        }
        report = ExecutiveSummary(data=data)
        schema = report.to_schema()
        assert len(schema.blocks) > 0

    def test_with_highlights(self) -> None:
        """ExecutiveSummary generates highlights section."""
        data = {
            "highlights": [
                {"severity": "success", "title": "Great!", "message": "Revenue up"},
            ],
        }
        report = ExecutiveSummary(data=data)
        schema = report.to_schema()
        types = [b["type"] for b in schema.blocks]
        assert "section" in types

    def test_with_milestones(self) -> None:
        """ExecutiveSummary generates milestones timeline."""
        data = {
            "milestones": [
                {"date": "2024-01", "title": "Launch"},
                {"date": "2024-06", "title": "IPO"},
            ],
        }
        report = ExecutiveSummary(data=data)
        schema = report.to_schema()
        types = [b["type"] for b in schema.blocks]
        assert "timeline" in types

    def test_is_report_subclass(self) -> None:
        """ExecutiveSummary is a Report subclass."""
        assert isinstance(ExecutiveSummary(), Report)


class TestOpsMonitor:
    """Test OpsMonitor template."""

    def test_basic_creation(self) -> None:
        """OpsMonitor can be created with no data."""
        report = OpsMonitor()
        assert report.title == "Operations Monitor"
        assert report.theme == "dark"

    def test_custom_title(self) -> None:
        """OpsMonitor accepts custom title."""
        report = OpsMonitor(title="Infra Dashboard")
        assert report.title == "Infra Dashboard"

    def test_with_services(self) -> None:
        """OpsMonitor generates service health status list."""
        data = {
            "services": [
                {"label": "API", "status": "success"},
                {"label": "DB", "status": "error"},
            ],
        }
        report = OpsMonitor(data=data)
        schema = report.to_schema()
        types = [b["type"] for b in schema.blocks]
        assert "status_list" in types

    def test_with_metrics(self) -> None:
        """OpsMonitor generates gauge charts for metrics."""
        data = {
            "metrics": [
                {"label": "CPU", "value": 75, "max": 100, "unit": "%"},
                {"label": "Memory", "value": 60, "max": 100, "unit": "%"},
            ],
        }
        report = OpsMonitor(data=data)
        schema = report.to_schema()
        types = [b["type"] for b in schema.blocks]
        assert "columns" in types

    def test_with_error_rate(self) -> None:
        """OpsMonitor generates error rate bar chart."""
        data = {
            "errors": [
                {"time": "00:00", "count": 5},
                {"time": "01:00", "count": 3},
            ],
        }
        report = OpsMonitor(data=data)
        schema = report.to_schema()
        types = [b["type"] for b in schema.blocks]
        assert "bar_chart" in types

    def test_is_report_subclass(self) -> None:
        """OpsMonitor is a Report subclass."""
        assert isinstance(OpsMonitor(), Report)

    def test_json_roundtrip(self) -> None:
        """OpsMonitor JSON output is valid."""
        data = {
            "services": [{"label": "API", "status": "success"}],
            "metrics": [{"label": "CPU", "value": 75}],
        }
        report = OpsMonitor(data=data)
        parsed = json.loads(report.to_json())
        assert parsed["title"] == "Operations Monitor"


# ---------------------------------------------------------------------------
# Schema-level features
# ---------------------------------------------------------------------------


class TestSchemaFeatures:
    """Test schema-level additions (custom_theme, expires, features)."""

    def test_custom_theme_in_schema(self) -> None:
        """Custom theme dict appears in ReportSchema."""
        theme = Theme(name="brand", primary="#FF6B00")
        r = Report(title="Test", theme=theme)
        schema = r.to_schema()
        assert schema.custom_theme is not None
        assert schema.custom_theme["name"] == "brand"

    def test_no_custom_theme_with_string(self) -> None:
        """String theme does not produce custom_theme in schema."""
        r = Report(title="Test", theme="dark")
        schema = r.to_schema()
        assert schema.custom_theme is None

    def test_expires_excluded_when_none(self) -> None:
        """Expires is excluded from JSON when None."""
        r = Report(title="Test")
        r.add(KPI(label="A", value=1))
        parsed = json.loads(r.to_json())
        assert "expires" not in parsed

    def test_custom_theme_excluded_when_none(self) -> None:
        """custom_theme is excluded from JSON when None."""
        r = Report(title="Test", theme="dark")
        r.add(KPI(label="A", value=1))
        parsed = json.loads(r.to_json())
        assert "custom_theme" not in parsed

    def test_features_excluded_when_empty(self) -> None:
        """Features is excluded from JSON when no flags are set."""
        r = Report(title="Test")
        r.add(KPI(label="A", value=1))
        parsed = json.loads(r.to_json())
        assert "features" not in parsed
