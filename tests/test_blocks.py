"""Tests for all HolySheet block models — both original and new v0.2.0 types."""

from __future__ import annotations

from holysheet import (
    KPI,
    Accordion,
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
    Embed,
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
    NumberInput,
    PieChart,
    ProgressBar,
    RadarChart,
    RadioGroup,
    Report,
    SankeyChart,
    ScatterChart,
    Section,
    Slider,
    Sparkline,
    StatComparison,
    StatusList,
    Stepper,
    Tabs,
    TagList,
    TextInput,
    Timeline,
    Toggle,
    TreemapChart,
    UserCard,
    Video,
    WaterfallChart,
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
        t = Toggle(
            label="Notifications", description="Enable push notifications", default_value=True
        )
        props = t.to_props()
        assert props["description"] == "Enable push notifications"
        assert props["defaultValue"] is True


class TestAccordion:
    def test_basic(self) -> None:
        a = Accordion(
            panels=[
                {
                    "title": "Panel 1",
                    "children": [KPI(label="A", value=1)],
                    "default_expanded": True,
                },
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
    """Verify all 47 block types work together in a single report."""

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

        # Original Charts
        r.add(LineChart(title="Line", data=SAMPLE_DATA, x="x", y="y"))
        r.add(AreaChart(title="Area", data=SAMPLE_DATA, x="x", y="y"))
        r.add(BarChart(title="Bar", data=SAMPLE_DATA, x="x", y="y"))
        r.add(PieChart(title="Pie", data=SAMPLE_DATA, name="x", value="y"))
        r.add(ScatterChart(title="Scatter", data=SAMPLE_DATA, x="x", y="y"))
        r.add(RadarChart(title="Radar", data=SAMPLE_DATA, indicators=["x", "y", "z"]))
        r.add(GaugeChart(title="Gauge", value=75))
        r.add(FunnelChart(title="Funnel", data=SAMPLE_DATA, name="x", value="y"))
        r.add(TreemapChart(title="Tree", data=SAMPLE_DATA, name="x", value="y"))

        # New Charts
        r.add(
            HeatmapChart(title="Heat", data=[{"x": "A", "y": "B", "v": 1}], x="x", y="y", value="v")
        )
        r.add(
            CandlestickChart(
                title="OHLC",
                data=[{"d": "2024-01", "o": 100, "c": 110, "l": 95, "h": 115}],
                x="d",
                open="o",
                close="c",
                low="l",
                high="h",
            )
        )
        r.add(
            SankeyChart(
                title="Flow",
                nodes=[{"name": "A"}, {"name": "B"}],
                links=[{"source": "A", "target": "B", "value": 10}],
            )
        )
        r.add(
            WaterfallChart(
                title="Bridge", data=[{"cat": "Start", "val": 100}], category="cat", value="val"
            )
        )
        r.add(BoxPlotChart(title="Box", data=[[10, 20, 30, 40, 50]], categories=["A"]))
        r.add(
            MapChart(
                title="Map",
                data=[{"lat": 48.8, "lng": 2.3, "v": 100}],
                lat="lat",
                lng="lng",
                value="v",
            )
        )

        # Data
        r.add(DataTable(title="Table", data=SAMPLE_DATA))

        # Content
        r.add(Markdown(content="# Hello"))
        r.add(CodeBlock(code="x = 1", language="python"))
        r.add(Image(src="https://example.com/img.png"))
        r.add(Alert(severity="info", message="Test"))

        # Progress
        r.add(ProgressBar(label="CPU", value=73))

        # New Content
        r.add(Timeline(title="Events", events=[{"date": "2024-01", "title": "Launch"}]))
        r.add(Callout(content="Quote", variant="quote"))
        r.add(Embed(url="https://example.com"))
        r.add(JsonViewer(data={"key": "value"}, title="Config"))
        r.add(UserCard(name="Alice", role="CEO"))
        r.add(StatusList(title="Services", items=[{"label": "API", "status": "success"}]))
        r.add(InfoList(title="Info", items=[{"key": "Version", "value": "1.0"}]))
        r.add(Stepper(title="Steps", steps=[{"label": "Start"}]))
        r.add(TagList(title="Tags", tags=[{"label": "v1.0"}]))
        r.add(Sparkline(data=[10, 20, 30, 40]))
        r.add(Video(src="https://example.com/video.mp4"))

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
        r.add(
            StatComparison(title="Compare", items=[{"label": "A", "current": 100, "previous": 80}])
        )
        r.add(Dropdown(label="Region", options=[{"label": "US", "value": "us"}]))
        r.add(TextInput(label="Name", placeholder="Enter name"))
        r.add(CheckboxGroup(label="Features", options=[{"label": "Dark", "value": "dark"}]))
        r.add(RadioGroup(label="Plan", options=[{"label": "Free", "value": "free"}]))

        schema = r.to_schema()
        assert len(schema.blocks) == 47
        assert schema.author == "Test Suite"

        # Verify JSON roundtrip
        import json

        json_str = r.to_json()
        parsed = json.loads(json_str)
        assert len(parsed["blocks"]) == 47

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
            "heatmap_chart",
            "candlestick_chart",
            "sankey_chart",
            "waterfall_chart",
            "box_plot_chart",
            "map_chart",
            "data_table",
            "markdown",
            "code_block",
            "image",
            "alert",
            "progress",
            "timeline",
            "callout",
            "embed",
            "json_viewer",
            "user_card",
            "status_list",
            "info_list",
            "stepper",
            "tag_list",
            "sparkline",
            "video",
            "divider",
            "section",
            "columns",
            "tabs",
            "slider",
            "number_input",
            "toggle",
            "accordion",
            "stat_comparison",
            "dropdown",
            "text_input",
            "checkbox_group",
            "radio_group",
        }
        assert types == expected


# ---------------------------------------------------------------------------
# Tests for new v0.3.0 block types
# ---------------------------------------------------------------------------


class TestHeatmapChart:
    def test_basic(self) -> None:
        c = HeatmapChart(title="Heat", data=[{"x": "A", "y": "B", "v": 5}], x="x", y="y", value="v")
        assert c.type == "heatmap_chart"
        props = c.to_props()
        assert props["title"] == "Heat"
        assert len(props["data"]) == 1
        assert props["height"] == 360


class TestCandlestickChart:
    def test_basic(self) -> None:
        data = [{"d": "2024-01", "o": 100, "c": 110, "l": 95, "h": 115}]
        c = CandlestickChart(title="OHLC", data=data, x="d", open="o", close="c", low="l", high="h")
        assert c.type == "candlestick_chart"
        props = c.to_props()
        assert props["open"] == "o"
        assert props["height"] == 400


class TestSankeyChart:
    def test_basic(self) -> None:
        c = SankeyChart(
            title="Flow",
            nodes=[{"name": "A"}, {"name": "B"}],
            links=[{"source": "A", "target": "B", "value": 10}],
        )
        assert c.type == "sankey_chart"
        props = c.to_props()
        assert len(props["nodes"]) == 2
        assert len(props["links"]) == 1


class TestWaterfallChart:
    def test_basic(self) -> None:
        data = [{"cat": "Revenue", "val": 1000}, {"cat": "Costs", "val": -400}]
        c = WaterfallChart(title="Bridge", data=data, category="cat", value="val")
        assert c.type == "waterfall_chart"
        assert len(c.to_props()["data"]) == 2


class TestBoxPlotChart:
    def test_basic(self) -> None:
        c = BoxPlotChart(
            title="Box", data=[[10, 20, 30, 40, 50], [15, 25, 35, 45, 55]], categories=["A", "B"]
        )
        assert c.type == "box_plot_chart"
        assert len(c.to_props()["data"]) == 2


class TestMapChart:
    def test_basic(self) -> None:
        data = [{"lat": 48.8, "lng": 2.3, "v": 100, "n": "Paris"}]
        c = MapChart(title="Map", data=data, lat="lat", lng="lng", value="v", name="n")
        assert c.type == "map_chart"
        assert c.to_props()["name"] == "n"


class TestTimeline:
    def test_basic(self) -> None:
        t = Timeline(
            title="Events", events=[{"date": "2024-01", "title": "Launch", "description": "v1.0"}]
        )
        assert t.type == "timeline"
        assert len(t.to_props()["events"]) == 1


class TestCallout:
    def test_basic(self) -> None:
        c = Callout(content="Important quote", author="CEO", variant="highlight")
        assert c.type == "callout"
        props = c.to_props()
        assert props["variant"] == "highlight"
        assert props["author"] == "CEO"


class TestEmbed:
    def test_basic(self) -> None:
        e = Embed(url="https://example.com", title="Site", height=500)
        assert e.type == "embed"
        assert e.to_props()["height"] == 500


class TestJsonViewer:
    def test_basic(self) -> None:
        j = JsonViewer(data={"key": "value", "nested": {"a": [1, 2, 3]}}, title="Config")
        assert j.type == "json_viewer"
        assert j.to_props()["collapsed_depth"] == 2


class TestUserCard:
    def test_basic(self) -> None:
        u = UserCard(
            name="Alice",
            role="CEO",
            email="alice@co.com",
            stats=[{"label": "Projects", "value": "12"}],
        )
        assert u.type == "user_card"
        props = u.to_props()
        assert props["name"] == "Alice"
        assert len(props["stats"]) == 1


class TestStatusList:
    def test_basic(self) -> None:
        s = StatusList(
            title="Services",
            items=[
                {"label": "API", "status": "success"},
                {"label": "DB", "status": "error"},
            ],
        )
        assert s.type == "status_list"
        assert len(s.to_props()["items"]) == 2


class TestInfoList:
    def test_basic(self) -> None:
        i = InfoList(title="Details", items=[{"key": "Version", "value": "1.0"}])
        assert i.type == "info_list"
        assert len(i.to_props()["items"]) == 1


class TestStepper:
    def test_basic(self) -> None:
        s = Stepper(
            title="Onboarding",
            steps=[
                {"label": "Sign Up", "status": "complete"},
                {"label": "Verify", "status": "active"},
                {"label": "Done", "status": "pending"},
            ],
            current_step=1,
        )
        assert s.type == "stepper"
        assert s.to_props()["current_step"] == 1


class TestDropdown:
    def test_basic(self) -> None:
        d = Dropdown(
            label="Region",
            options=[{"label": "US", "value": "us"}, {"label": "EU", "value": "eu"}],
            default_value="us",
        )
        assert d.type == "dropdown"
        assert d.to_props()["default_value"] == "us"


class TestTextInput:
    def test_basic(self) -> None:
        t = TextInput(label="Name", placeholder="Enter name", multiline=True, rows=5)
        assert t.type == "text_input"
        props = t.to_props()
        assert props["multiline"] is True
        assert props["rows"] == 5


class TestCheckboxGroup:
    def test_basic(self) -> None:
        c = CheckboxGroup(
            label="Features",
            options=[
                {"label": "Dark Mode", "value": "dark"},
                {"label": "Notifications", "value": "notif"},
            ],
            default_values=["dark"],
        )
        assert c.type == "checkbox_group"
        assert c.to_props()["default_values"] == ["dark"]


class TestRadioGroup:
    def test_basic(self) -> None:
        r = RadioGroup(
            label="Plan",
            options=[
                {"label": "Free", "value": "free"},
                {"label": "Pro", "value": "pro"},
            ],
            default_value="free",
        )
        assert r.type == "radio_group"
        assert r.to_props()["default_value"] == "free"


class TestTagList:
    def test_basic(self) -> None:
        t = TagList(
            title="Technologies",
            tags=[
                {"label": "Python", "color": "#3776AB"},
                {"label": "React", "color": "#61DAFB"},
            ],
        )
        assert t.type == "tag_list"
        assert len(t.to_props()["tags"]) == 2


class TestSparkline:
    def test_basic(self) -> None:
        s = Sparkline(data=[10, 20, 15, 30, 25, 35, 40], color="#6C63FF", show_area=False)
        assert s.type == "sparkline"
        props = s.to_props()
        assert len(props["data"]) == 7
        assert props["show_area"] is False


class TestVideo:
    def test_basic(self) -> None:
        v = Video(
            src="https://example.com/video.mp4",
            title="Demo",
            poster="https://example.com/poster.jpg",
        )
        assert v.type == "video"
        props = v.to_props()
        assert props["controls"] is True
        assert props["autoplay"] is False
