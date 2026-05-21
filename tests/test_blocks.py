"""Tests for all HolySheet block models — both original and new v0.2.0 types."""

from __future__ import annotations

from holysheet import (
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
    Report,
    ScatterChart,
    Section,
    Slider,
    StatComparison,
    Tabs,
    Toggle,
    TreemapChart,
)

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_DATA = [
    {"x": 1, "y": 10, "z": 100},
    {"x": 2, "y": 20, "z": 200},
    {"x": 3, "y": 30, "z": 300},
]


# ---------------------------------------------------------------------------
# KPI & Metric
# ---------------------------------------------------------------------------


class TestKPI:
    """Test KPI block model."""

    def test_basic(self) -> None:
        kpi = KPI(label="Revenue", value=1000)
        assert kpi.type == "kpi"
        props = kpi.to_props()
        assert props["label"] == "Revenue"
        assert props["value"] == 1000

    def test_full_props(self) -> None:
        kpi = KPI(
            label="Users",
            value="42K",
            unit="users",
            delta="+5%",
            status="positive",
            description="Monthly active",
        )
        props = kpi.to_props()
        assert props["unit"] == "users"
        assert props["delta"] == "+5%"
        assert props["status"] == "positive"
        assert props["description"] == "Monthly active"

    def test_serialize(self) -> None:
        kpi = KPI(label="Test", value=1)
        d = kpi.serialize("block_001")
        assert d["id"] == "block_001"
        assert d["type"] == "kpi"
        assert "props" in d


class TestMetric:
    """Test Metric block model."""

    def test_basic(self) -> None:
        m = Metric(label="Uptime", value="99.97%")
        assert m.type == "metric"
        props = m.to_props()
        assert props["label"] == "Uptime"
        assert props["value"] == "99.97%"

    def test_with_unit(self) -> None:
        m = Metric(label="CPU", value=73, unit="%")
        props = m.to_props()
        assert props["unit"] == "%"


# ---------------------------------------------------------------------------
# Chart blocks
# ---------------------------------------------------------------------------


class TestLineChart:
    def test_basic(self) -> None:
        c = LineChart(title="Test", data=SAMPLE_DATA, x="x", y="y")
        assert c.type == "line_chart"
        props = c.to_props()
        assert len(props["data"]) == 3
        assert props["height"] == 360


class TestAreaChart:
    def test_basic(self) -> None:
        c = AreaChart(title="Area", data=SAMPLE_DATA, x="x", y="y")
        assert c.type == "area_chart"
        props = c.to_props()
        assert len(props["data"]) == 3

    def test_multi_y(self) -> None:
        c = AreaChart(title="Multi", data=SAMPLE_DATA, x="x", y=["y", "z"])
        props = c.to_props()
        assert props["y"] == ["y", "z"]


class TestBarChart:
    def test_basic(self) -> None:
        c = BarChart(title="Bar", data=SAMPLE_DATA, x="x", y="y")
        assert c.type == "bar_chart"


class TestPieChart:
    def test_basic(self) -> None:
        c = PieChart(title="Pie", data=SAMPLE_DATA, name="x", value="y")
        assert c.type == "pie_chart"
        props = c.to_props()
        assert props["name"] == "x"


class TestScatterChart:
    def test_basic(self) -> None:
        c = ScatterChart(title="Scatter", data=SAMPLE_DATA, x="x", y="y")
        assert c.type == "scatter_chart"
        props = c.to_props()
        assert props["x"] == "x"
        assert props["y"] == "y"

    def test_with_size(self) -> None:
        c = ScatterChart(title="Bubble", data=SAMPLE_DATA, x="x", y="y", size="z")
        props = c.to_props()
        assert props["size"] == "z"

    def test_with_category(self) -> None:
        c = ScatterChart(title="Cat", data=SAMPLE_DATA, x="x", y="y", category="z")
        props = c.to_props()
        assert props["category"] == "z"


class TestRadarChart:
    def test_basic(self) -> None:
        c = RadarChart(title="Radar", data=SAMPLE_DATA, indicators=["x", "y", "z"])
        assert c.type == "radar_chart"
        props = c.to_props()
        assert props["indicators"] == ["x", "y", "z"]
        assert len(props["data"]) == 3


class TestGaugeChart:
    def test_basic(self) -> None:
        c = GaugeChart(title="Speed", value=75)
        assert c.type == "gauge"
        props = c.to_props()
        assert props["value"] == 75
        assert props["min"] == 0
        assert props["max"] == 100

    def test_custom_range(self) -> None:
        c = GaugeChart(title="Temp", value=37.5, min=0, max=50, unit="°C")
        props = c.to_props()
        assert props["min"] == 0
        assert props["max"] == 50
        assert props["unit"] == "°C"

    def test_thresholds(self) -> None:
        c = GaugeChart(
            title="Health",
            value=85,
            thresholds=[
                {"value": 30, "color": "red"},
                {"value": 70, "color": "yellow"},
                {"value": 100, "color": "green"},
            ],
        )
        props = c.to_props()
        assert len(props["thresholds"]) == 3


class TestFunnelChart:
    def test_basic(self) -> None:
        data = [
            {"stage": "Visit", "count": 1000},
            {"stage": "Signup", "count": 500},
            {"stage": "Purchase", "count": 100},
        ]
        c = FunnelChart(title="Conversion", data=data, name="stage", value="count")
        assert c.type == "funnel_chart"
        props = c.to_props()
        assert len(props["data"]) == 3


class TestTreemapChart:
    def test_basic(self) -> None:
        data = [
            {"name": "A", "value": 100},
            {"name": "B", "value": 200},
        ]
        c = TreemapChart(title="Tree", data=data, name="name", value="value")
        assert c.type == "treemap_chart"
        props = c.to_props()
        assert len(props["data"]) == 2


# ---------------------------------------------------------------------------
# Content blocks
# ---------------------------------------------------------------------------


class TestMarkdown:
    def test_basic(self) -> None:
        m = Markdown(content="# Hello")
        assert m.type == "markdown"
        assert m.to_props()["content"] == "# Hello"


class TestCodeBlock:
    def test_basic(self) -> None:
        c = CodeBlock(code="print('hello')")
        assert c.type == "code_block"
        props = c.to_props()
        assert props["code"] == "print('hello')"

    def test_with_language(self) -> None:
        c = CodeBlock(code="x = 1", language="python", title="Example")
        props = c.to_props()
        assert props["language"] == "python"
        assert props["title"] == "Example"


class TestImage:
    def test_basic(self) -> None:
        i = Image(src="https://example.com/img.png")
        assert i.type == "image"
        props = i.to_props()
        assert props["src"] == "https://example.com/img.png"

    def test_with_caption(self) -> None:
        i = Image(
            src="https://example.com/img.png",
            alt="Chart",
            caption="Revenue overview",
            width=800,
        )
        props = i.to_props()
        assert props["caption"] == "Revenue overview"
        assert props["width"] == 800


class TestAlert:
    def test_basic(self) -> None:
        a = Alert(severity="info", message="Hello")
        assert a.type == "alert"
        props = a.to_props()
        assert props["severity"] == "info"
        assert props["message"] == "Hello"

    def test_with_title(self) -> None:
        a = Alert(severity="warning", title="Caution", message="Watch out")
        props = a.to_props()
        assert props["title"] == "Caution"

    def test_all_severities(self) -> None:
        for sev in ["info", "warning", "error", "success"]:
            a = Alert(severity=sev, message="test")
            assert a.severity == sev


# ---------------------------------------------------------------------------
# Progress block
# ---------------------------------------------------------------------------


class TestProgressBar:
    def test_basic(self) -> None:
        p = ProgressBar(label="Upload", value=45)
        assert p.type == "progress"
        props = p.to_props()
        assert props["value"] == 45
        assert props["max"] == 100

    def test_custom_max(self) -> None:
        p = ProgressBar(label="Steps", value=7, max=10)
        props = p.to_props()
        assert props["max"] == 10


# ---------------------------------------------------------------------------
# Layout blocks
# ---------------------------------------------------------------------------


class TestDivider:
    def test_basic(self) -> None:
        d = Divider()
        assert d.type == "divider"
        props = d.to_props()
        assert props["variant"] == "solid"

    def test_with_label(self) -> None:
        d = Divider(label="Section Break", variant="dashed")
        props = d.to_props()
        assert props["label"] == "Section Break"
        assert props["variant"] == "dashed"


class TestSection:
    def test_basic(self) -> None:
        s = Section(title="Group", children=[KPI(label="A", value=1)])
        assert s.type == "section"
        d = s.serialize("block_001", counter=1)
        assert d["type"] == "section"
        assert len(d["props"]["children"]) == 1

    def test_nested_sections(self) -> None:
        inner = Section(title="Inner", children=[Markdown(content="hi")])
        outer = Section(title="Outer", children=[inner])
        d = outer.serialize("block_001", counter=1)
        assert d["props"]["children"][0]["type"] == "section"


class TestColumns:
    def test_basic(self) -> None:
        c = Columns(children=[KPI(label="A", value=1), KPI(label="B", value=2)])
        assert c.type == "columns"
        d = c.serialize("block_001", counter=1)
        assert len(d["props"]["children"]) == 2

    def test_with_widths(self) -> None:
        c = Columns(
            children=[KPI(label="A", value=1), KPI(label="B", value=2)],
            widths=[4, 8],
        )
        d = c.serialize("block_001", counter=1)
        assert d["props"]["widths"] == [4, 8]

    def test_bento_layout(self) -> None:
        c = Columns(
            children=[KPI(label="A", value=1), KPI(label="B", value=2)],
            layout="bento",
        )
        d = c.serialize("block_001", counter=1)
        assert d["props"]["layout"] == "bento"


class TestTabs:
    def test_basic(self) -> None:
        t = Tabs(
            tabs=[
                {"label": "Tab 1", "children": [KPI(label="A", value=1)]},
                {"label": "Tab 2", "children": [Markdown(content="hello")]},
            ]
        )
        assert t.type == "tabs"
        d = t.serialize("block_001", counter=1)
        assert len(d["props"]["tabs"]) == 2
        assert d["props"]["tabs"][0]["label"] == "Tab 1"
        assert len(d["props"]["tabs"][0]["children"]) == 1


# ---------------------------------------------------------------------------
# Interactive blocks
# ---------------------------------------------------------------------------


class TestSlider:
    def test_basic(self) -> None:
        s = Slider(label="Temperature", min=0, max=100, default_value=50)
        assert s.type == "slider"
        props = s.to_props()
        assert props["label"] == "Temperature"
        assert props["min"] == 0
        assert props["max"] == 100
        assert props["defaultValue"] == 50

    def test_range(self) -> None:
        s = Slider(label="Range", default_value=[20, 80], step=5)
        props = s.to_props()
        assert props["defaultValue"] == [20, 80]
        assert props["step"] == 5


class TestNumberInput:
    def test_basic(self) -> None:
        n = NumberInput(label="Quantity", min=0, max=100, default_value=10)
        assert n.type == "number_input"
        props = n.to_props()
        assert props["label"] == "Quantity"
        assert props["defaultValue"] == 10

    def test_with_unit(self) -> None:
        n = NumberInput(label="Weight", default_value=5, unit="kg")
        props = n.to_props()
        assert props["unit"] == "kg"


class TestToggle:
    def test_basic(self) -> None:
        t = Toggle(label="Dark Mode")
        assert t.type == "toggle"
        props = t.to_props()
        assert props["label"] == "Dark Mode"
        assert props["defaultValue"] is False

    def test_with_description(self) -> None:
        t = Toggle(label="Notifications", description="Enable push notifications", default_value=True)
        props = t.to_props()
        assert props["description"] == "Enable push notifications"
        assert props["defaultValue"] is True


class TestAccordion:
    def test_basic(self) -> None:
        a = Accordion(
            panels=[
                {"title": "Panel 1", "children": [KPI(label="A", value=1)], "default_expanded": True},
                {"title": "Panel 2", "children": [Markdown(content="hi")]},
            ]
        )
        assert a.type == "accordion"
        d = a.serialize("block_001", counter=1)
        assert len(d["props"]["panels"]) == 2
        assert d["props"]["panels"][0]["title"] == "Panel 1"
        assert d["props"]["panels"][0]["defaultExpanded"] is True
        assert len(d["props"]["panels"][0]["children"]) == 1


class TestStatComparison:
    def test_basic(self) -> None:
        s = StatComparison(
            title="Q4 vs Q3",
            items=[
                {"label": "Revenue", "current": 250000, "previous": 210000, "unit": "USD"},
                {"label": "Users", "current": 42000, "previous": 35000},
            ],
        )
        assert s.type == "stat_comparison"
        props = s.to_props()
        assert props["title"] == "Q4 vs Q3"
        assert len(props["items"]) == 2


# ---------------------------------------------------------------------------
# Integration: All block types in a single report
# ---------------------------------------------------------------------------


class TestAllBlockTypes:
    """Verify all 26 block types work together in a single report."""

    def test_comprehensive_report(self) -> None:
        r = Report(
            title="Full Test",
            theme="dark",
            author="Test Suite",
            report_version="1.0",
            footer="Generated by pytest",
        )

        # KPI & Metric
        r.add(KPI(label="Revenue", value=100, delta="+5%", status="positive"))
        r.add(Metric(label="Uptime", value="99.9%"))

        # Charts
        r.add(LineChart(title="Line", data=SAMPLE_DATA, x="x", y="y"))
        r.add(AreaChart(title="Area", data=SAMPLE_DATA, x="x", y="y"))
        r.add(BarChart(title="Bar", data=SAMPLE_DATA, x="x", y="y"))
        r.add(PieChart(title="Pie", data=SAMPLE_DATA, name="x", value="y"))
        r.add(ScatterChart(title="Scatter", data=SAMPLE_DATA, x="x", y="y"))
        r.add(RadarChart(title="Radar", data=SAMPLE_DATA, indicators=["x", "y", "z"]))
        r.add(GaugeChart(title="Gauge", value=75))
        r.add(FunnelChart(title="Funnel", data=SAMPLE_DATA, name="x", value="y"))
        r.add(TreemapChart(title="Tree", data=SAMPLE_DATA, name="x", value="y"))

        # Data
        r.add(DataTable(title="Table", data=SAMPLE_DATA))

        # Content
        r.add(Markdown(content="# Hello"))
        r.add(CodeBlock(code="x = 1", language="python"))
        r.add(Image(src="https://example.com/img.png"))
        r.add(Alert(severity="info", message="Test"))

        # Progress
        r.add(ProgressBar(label="CPU", value=73))

        # Layout
        r.add(Divider(label="Break"))
        r.add(Section(title="Group", children=[KPI(label="N", value=1)]))
        r.add(Columns(children=[KPI(label="L", value=1), KPI(label="R", value=2)]))
        r.add(
            Tabs(
                tabs=[
                    {"label": "A", "children": [KPI(label="T1", value=10)]},
                    {"label": "B", "children": [Markdown(content="Tab 2")]},
                ]
            )
        )

        # Interactive blocks
        r.add(Slider(label="Threshold", default_value=50))
        r.add(NumberInput(label="Count", default_value=10))
        r.add(Toggle(label="Enable"))
        r.add(
            Accordion(
                panels=[
                    {"title": "Details", "children": [Markdown(content="Info")]},
                ]
            )
        )
        r.add(StatComparison(title="Compare", items=[{"label": "A", "current": 100, "previous": 80}]))

        schema = r.to_schema()
        assert len(schema.blocks) == 26
        assert schema.author == "Test Suite"
        assert schema.report_version == "1.0"
        assert schema.footer == "Generated by pytest"

        # Verify JSON roundtrip
        import json

        json_str = r.to_json()
        parsed = json.loads(json_str)
        assert parsed["schema_version"] == "1.0.0"
        assert len(parsed["blocks"]) == 26

        # Verify all types are present
        types = {b["type"] for b in parsed["blocks"]}
        expected = {
            "kpi",
            "metric",
            "line_chart",
            "area_chart",
            "bar_chart",
            "pie_chart",
            "scatter_chart",
            "radar_chart",
            "gauge",
            "funnel_chart",
            "treemap_chart",
            "data_table",
            "markdown",
            "code_block",
            "image",
            "alert",
            "progress",
            "divider",
            "section",
            "columns",
            "tabs",
            "slider",
            "number_input",
            "toggle",
            "accordion",
            "stat_comparison",
        }
        assert types == expected


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_DATA = [
    {"x": 1, "y": 10, "z": 100},
    {"x": 2, "y": 20, "z": 200},
    {"x": 3, "y": 30, "z": 300},
]


# ---------------------------------------------------------------------------
# KPI & Metric
# ---------------------------------------------------------------------------


class TestKPI:
    """Test KPI block model."""

    def test_basic(self) -> None:
        kpi = KPI(label="Revenue", value=1000)
        assert kpi.type == "kpi"
        props = kpi.to_props()
        assert props["label"] == "Revenue"
        assert props["value"] == 1000

    def test_full_props(self) -> None:
        kpi = KPI(
            label="Users",
            value="42K",
            unit="users",
            delta="+5%",
            status="positive",
            description="Monthly active",
        )
        props = kpi.to_props()
        assert props["unit"] == "users"
        assert props["delta"] == "+5%"
        assert props["status"] == "positive"
        assert props["description"] == "Monthly active"

    def test_serialize(self) -> None:
        kpi = KPI(label="Test", value=1)
        d = kpi.serialize("block_001")
        assert d["id"] == "block_001"
        assert d["type"] == "kpi"
        assert "props" in d


class TestMetric:
    """Test Metric block model."""

    def test_basic(self) -> None:
        m = Metric(label="Uptime", value="99.97%")
        assert m.type == "metric"
        props = m.to_props()
        assert props["label"] == "Uptime"
        assert props["value"] == "99.97%"

    def test_with_unit(self) -> None:
        m = Metric(label="CPU", value=73, unit="%")
        props = m.to_props()
        assert props["unit"] == "%"


# ---------------------------------------------------------------------------
# Chart blocks
# ---------------------------------------------------------------------------


class TestLineChart:
    def test_basic(self) -> None:
        c = LineChart(title="Test", data=SAMPLE_DATA, x="x", y="y")
        assert c.type == "line_chart"
        props = c.to_props()
        assert len(props["data"]) == 3
        assert props["height"] == 360


class TestAreaChart:
    def test_basic(self) -> None:
        c = AreaChart(title="Area", data=SAMPLE_DATA, x="x", y="y")
        assert c.type == "area_chart"
        props = c.to_props()
        assert len(props["data"]) == 3

    def test_multi_y(self) -> None:
        c = AreaChart(title="Multi", data=SAMPLE_DATA, x="x", y=["y", "z"])
        props = c.to_props()
        assert props["y"] == ["y", "z"]


class TestBarChart:
    def test_basic(self) -> None:
        c = BarChart(title="Bar", data=SAMPLE_DATA, x="x", y="y")
        assert c.type == "bar_chart"


class TestPieChart:
    def test_basic(self) -> None:
        c = PieChart(title="Pie", data=SAMPLE_DATA, name="x", value="y")
        assert c.type == "pie_chart"
        props = c.to_props()
        assert props["name"] == "x"


class TestScatterChart:
    def test_basic(self) -> None:
        c = ScatterChart(title="Scatter", data=SAMPLE_DATA, x="x", y="y")
        assert c.type == "scatter_chart"
        props = c.to_props()
        assert props["x"] == "x"
        assert props["y"] == "y"

    def test_with_size(self) -> None:
        c = ScatterChart(title="Bubble", data=SAMPLE_DATA, x="x", y="y", size="z")
        props = c.to_props()
        assert props["size"] == "z"

    def test_with_category(self) -> None:
        c = ScatterChart(title="Cat", data=SAMPLE_DATA, x="x", y="y", category="z")
        props = c.to_props()
        assert props["category"] == "z"


class TestRadarChart:
    def test_basic(self) -> None:
        c = RadarChart(title="Radar", data=SAMPLE_DATA, indicators=["x", "y", "z"])
        assert c.type == "radar_chart"
        props = c.to_props()
        assert props["indicators"] == ["x", "y", "z"]
        assert len(props["data"]) == 3


class TestGaugeChart:
    def test_basic(self) -> None:
        c = GaugeChart(title="Speed", value=75)
        assert c.type == "gauge"
        props = c.to_props()
        assert props["value"] == 75
        assert props["min"] == 0
        assert props["max"] == 100

    def test_custom_range(self) -> None:
        c = GaugeChart(title="Temp", value=37.5, min=0, max=50, unit="°C")
        props = c.to_props()
        assert props["min"] == 0
        assert props["max"] == 50
        assert props["unit"] == "°C"

    def test_thresholds(self) -> None:
        c = GaugeChart(
            title="Health",
            value=85,
            thresholds=[
                {"value": 30, "color": "red"},
                {"value": 70, "color": "yellow"},
                {"value": 100, "color": "green"},
            ],
        )
        props = c.to_props()
        assert len(props["thresholds"]) == 3


class TestFunnelChart:
    def test_basic(self) -> None:
        data = [
            {"stage": "Visit", "count": 1000},
            {"stage": "Signup", "count": 500},
            {"stage": "Purchase", "count": 100},
        ]
        c = FunnelChart(title="Conversion", data=data, name="stage", value="count")
        assert c.type == "funnel_chart"
        props = c.to_props()
        assert len(props["data"]) == 3


class TestTreemapChart:
    def test_basic(self) -> None:
        data = [
            {"name": "A", "value": 100},
            {"name": "B", "value": 200},
        ]
        c = TreemapChart(title="Tree", data=data, name="name", value="value")
        assert c.type == "treemap_chart"
        props = c.to_props()
        assert len(props["data"]) == 2


# ---------------------------------------------------------------------------
# Content blocks
# ---------------------------------------------------------------------------


class TestMarkdown:
    def test_basic(self) -> None:
        m = Markdown(content="# Hello")
        assert m.type == "markdown"
        assert m.to_props()["content"] == "# Hello"


class TestCodeBlock:
    def test_basic(self) -> None:
        c = CodeBlock(code="print('hello')")
        assert c.type == "code_block"
        props = c.to_props()
        assert props["code"] == "print('hello')"

    def test_with_language(self) -> None:
        c = CodeBlock(code="x = 1", language="python", title="Example")
        props = c.to_props()
        assert props["language"] == "python"
        assert props["title"] == "Example"


class TestImage:
    def test_basic(self) -> None:
        i = Image(src="https://example.com/img.png")
        assert i.type == "image"
        props = i.to_props()
        assert props["src"] == "https://example.com/img.png"

    def test_with_caption(self) -> None:
        i = Image(
            src="https://example.com/img.png",
            alt="Chart",
            caption="Revenue overview",
            width=800,
        )
        props = i.to_props()
        assert props["caption"] == "Revenue overview"
        assert props["width"] == 800


class TestAlert:
    def test_basic(self) -> None:
        a = Alert(severity="info", message="Hello")
        assert a.type == "alert"
        props = a.to_props()
        assert props["severity"] == "info"
        assert props["message"] == "Hello"

    def test_with_title(self) -> None:
        a = Alert(severity="warning", title="Caution", message="Watch out")
        props = a.to_props()
        assert props["title"] == "Caution"

    def test_all_severities(self) -> None:
        for sev in ["info", "warning", "error", "success"]:
            a = Alert(severity=sev, message="test")
            assert a.severity == sev


# ---------------------------------------------------------------------------
# Progress block
# ---------------------------------------------------------------------------


class TestProgressBar:
    def test_basic(self) -> None:
        p = ProgressBar(label="Upload", value=45)
        assert p.type == "progress"
        props = p.to_props()
        assert props["value"] == 45
        assert props["max"] == 100

    def test_custom_max(self) -> None:
        p = ProgressBar(label="Steps", value=7, max=10)
        props = p.to_props()
        assert props["max"] == 10


# ---------------------------------------------------------------------------
# Layout blocks
# ---------------------------------------------------------------------------


class TestDivider:
    def test_basic(self) -> None:
        d = Divider()
        assert d.type == "divider"
        props = d.to_props()
        assert props["variant"] == "solid"

    def test_with_label(self) -> None:
        d = Divider(label="Section Break", variant="dashed")
        props = d.to_props()
        assert props["label"] == "Section Break"
        assert props["variant"] == "dashed"


class TestSection:
    def test_basic(self) -> None:
        s = Section(title="Group", children=[KPI(label="A", value=1)])
        assert s.type == "section"
        d = s.serialize("block_001", counter=1)
        assert d["type"] == "section"
        assert len(d["props"]["children"]) == 1

    def test_nested_sections(self) -> None:
        inner = Section(title="Inner", children=[Markdown(content="hi")])
        outer = Section(title="Outer", children=[inner])
        d = outer.serialize("block_001", counter=1)
        assert d["props"]["children"][0]["type"] == "section"


class TestColumns:
    def test_basic(self) -> None:
        c = Columns(children=[KPI(label="A", value=1), KPI(label="B", value=2)])
        assert c.type == "columns"
        d = c.serialize("block_001", counter=1)
        assert len(d["props"]["children"]) == 2

    def test_with_widths(self) -> None:
        c = Columns(
            children=[KPI(label="A", value=1), KPI(label="B", value=2)],
            widths=[4, 8],
        )
        d = c.serialize("block_001", counter=1)
        assert d["props"]["widths"] == [4, 8]


class TestTabs:
    def test_basic(self) -> None:
        t = Tabs(
            tabs=[
                {"label": "Tab 1", "children": [KPI(label="A", value=1)]},
                {"label": "Tab 2", "children": [Markdown(content="hello")]},
            ]
        )
        assert t.type == "tabs"
        d = t.serialize("block_001", counter=1)
        assert len(d["props"]["tabs"]) == 2
        assert d["props"]["tabs"][0]["label"] == "Tab 1"
        assert len(d["props"]["tabs"][0]["children"]) == 1


# ---------------------------------------------------------------------------
# Integration: All block types in a single report
# ---------------------------------------------------------------------------


class TestAllBlockTypes:
    """Verify all 21 block types work together in a single report."""

    def test_comprehensive_report(self) -> None:
        r = Report(
            title="Full Test",
            theme="dark",
            author="Test Suite",
            report_version="1.0",
            footer="Generated by pytest",
        )

        # KPI & Metric
        r.add(KPI(label="Revenue", value=100, delta="+5%", status="positive"))
        r.add(Metric(label="Uptime", value="99.9%"))

        # Charts
        r.add(LineChart(title="Line", data=SAMPLE_DATA, x="x", y="y"))
        r.add(AreaChart(title="Area", data=SAMPLE_DATA, x="x", y="y"))
        r.add(BarChart(title="Bar", data=SAMPLE_DATA, x="x", y="y"))
        r.add(PieChart(title="Pie", data=SAMPLE_DATA, name="x", value="y"))
        r.add(ScatterChart(title="Scatter", data=SAMPLE_DATA, x="x", y="y"))
        r.add(RadarChart(title="Radar", data=SAMPLE_DATA, indicators=["x", "y", "z"]))
        r.add(GaugeChart(title="Gauge", value=75))
        r.add(FunnelChart(title="Funnel", data=SAMPLE_DATA, name="x", value="y"))
        r.add(TreemapChart(title="Tree", data=SAMPLE_DATA, name="x", value="y"))

        # Data
        r.add(DataTable(title="Table", data=SAMPLE_DATA))

        # Content
        r.add(Markdown(content="# Hello"))
        r.add(CodeBlock(code="x = 1", language="python"))
        r.add(Image(src="https://example.com/img.png"))
        r.add(Alert(severity="info", message="Test"))

        # Progress
        r.add(ProgressBar(label="CPU", value=73))

        # Layout
        r.add(Divider(label="Break"))
        r.add(Section(title="Group", children=[KPI(label="N", value=1)]))
        r.add(Columns(children=[KPI(label="L", value=1), KPI(label="R", value=2)]))
        r.add(
            Tabs(
                tabs=[
                    {"label": "A", "children": [KPI(label="T1", value=10)]},
                    {"label": "B", "children": [Markdown(content="Tab 2")]},
                ]
            )
        )

        schema = r.to_schema()
        assert len(schema.blocks) == 21
        assert schema.author == "Test Suite"
        assert schema.report_version == "1.0"
        assert schema.footer == "Generated by pytest"

        # Verify JSON roundtrip
        import json

        json_str = r.to_json()
        parsed = json.loads(json_str)
        assert parsed["schema_version"] == "1.0.0"
        assert len(parsed["blocks"]) == 21

        # Verify all types are present
        types = {b["type"] for b in parsed["blocks"]}
        expected = {
            "kpi",
            "metric",
            "line_chart",
            "area_chart",
            "bar_chart",
            "pie_chart",
            "scatter_chart",
            "radar_chart",
            "gauge",
            "funnel_chart",
            "treemap_chart",
            "data_table",
            "markdown",
            "code_block",
            "image",
            "alert",
            "progress",
            "divider",
            "section",
            "columns",
            "tabs",
        }
        assert types == expected
