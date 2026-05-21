"""Tests for new v0.4.0 block types — GanttChart, DAGChart, CorrelationMatrix, Scorecard, DataProfile, Compare."""

from __future__ import annotations

import json
from typing import Any

from holysheet import (
    KPI,
    Compare,
    CorrelationMatrix,
    DAGChart,
    DataProfile,
    GanttChart,
    Markdown,
    Report,
    Scorecard,
)

# ---------------------------------------------------------------------------
# GanttChart
# ---------------------------------------------------------------------------


class TestGanttChart:
    """Test GanttChart block model."""

    def test_basic(self) -> None:
        """GanttChart has correct type and basic props."""
        block = GanttChart(
            title="Project Plan",
            tasks=[
                {
                    "name": "Task 1",
                    "start": "2024-01-01",
                    "end": "2024-06-30",
                    "progress": 50,
                },
            ],
        )
        assert block.type == "gantt_chart"
        props = block.to_props()
        assert props["title"] == "Project Plan"
        assert len(props["tasks"]) == 1
        assert props["tasks"][0]["name"] == "Task 1"
        assert props["tasks"][0]["progress"] == 50
        assert props["height"] == 400

    def test_multiple_tasks(self) -> None:
        """GanttChart handles multiple tasks."""
        tasks = [
            {"name": "Design", "start": "2024-01-01", "end": "2024-03-31", "group": "Phase 1"},
            {"name": "Build", "start": "2024-04-01", "end": "2024-09-30", "group": "Phase 2"},
            {"name": "Test", "start": "2024-10-01", "end": "2024-12-31", "group": "Phase 2"},
        ]
        block = GanttChart(title="Timeline", tasks=tasks)
        props = block.to_props()
        assert len(props["tasks"]) == 3

    def test_custom_height(self) -> None:
        """GanttChart supports custom height."""
        block = GanttChart(title="Custom", tasks=[], height=600)
        assert block.to_props()["height"] == 600

    def test_empty_tasks(self) -> None:
        """GanttChart can be created with empty tasks."""
        block = GanttChart(title="Empty")
        props = block.to_props()
        assert props["tasks"] == []

    def test_serialize(self) -> None:
        """GanttChart.serialize() returns correct structure."""
        block = GanttChart(
            title="Test",
            tasks=[{"name": "T", "start": "2024-01-01", "end": "2024-12-31"}],
        )
        result = block.serialize("block_001")
        assert result["id"] == "block_001"
        assert result["type"] == "gantt_chart"
        assert "props" in result
        assert result["props"]["title"] == "Test"

    def test_in_report(self, tmp_path: Any) -> None:
        """GanttChart integrates with Report add + export_json."""
        r = Report(title="Gantt Report")
        r.add(
            GanttChart(
                title="Sprint Plan",
                tasks=[{"name": "Sprint 1", "start": "2024-01-01", "end": "2024-01-14"}],
            )
        )
        out = tmp_path / "gantt.json"
        r.export_json(out)
        data = json.loads(out.read_text())
        assert len(data["blocks"]) == 1
        assert data["blocks"][0]["type"] == "gantt_chart"

    def test_task_with_optional_fields(self) -> None:
        """GanttChart task dicts can carry optional fields."""
        block = GanttChart(
            title="Colors",
            tasks=[
                {
                    "name": "Design",
                    "start": "2024-01-01",
                    "end": "2024-03-31",
                    "color": "#FF0000",
                    "progress": 100,
                    "group": "Phase 1",
                },
            ],
        )
        props = block.to_props()
        assert props["tasks"][0]["color"] == "#FF0000"


# ---------------------------------------------------------------------------
# DAGChart
# ---------------------------------------------------------------------------


class TestDAGChart:
    """Test DAGChart block model."""

    def test_basic(self) -> None:
        """DAGChart has correct type and basic props."""
        block = DAGChart(
            title="Pipeline",
            nodes=[{"id": "A", "label": "Extract"}, {"id": "B", "label": "Transform"}],
            edges=[{"from": "A", "to": "B"}],
        )
        assert block.type == "dag_chart"
        props = block.to_props()
        assert props["title"] == "Pipeline"
        assert len(props["nodes"]) == 2
        assert len(props["edges"]) == 1
        assert props["layout"] == "force"
        assert props["height"] == 400

    def test_circular_layout(self) -> None:
        """DAGChart supports circular layout."""
        block = DAGChart(title="Graph", nodes=[], edges=[], layout="circular")
        assert block.to_props()["layout"] == "circular"

    def test_empty_graph(self) -> None:
        """DAGChart can be created with no nodes or edges."""
        block = DAGChart(title="Empty DAG")
        props = block.to_props()
        assert props["nodes"] == []
        assert props["edges"] == []

    def test_edge_labels(self) -> None:
        """DAGChart edges can carry labels."""
        block = DAGChart(
            title="Flow",
            nodes=[{"id": "1", "label": "Start"}, {"id": "2", "label": "End"}],
            edges=[{"from": "1", "to": "2", "label": "next"}],
        )
        props = block.to_props()
        assert props["edges"][0]["label"] == "next"

    def test_serialize(self) -> None:
        """DAGChart.serialize() returns correct structure."""
        block = DAGChart(
            title="DAG",
            nodes=[{"id": "X", "label": "X"}],
            edges=[],
        )
        result = block.serialize("block_005")
        assert result["id"] == "block_005"
        assert result["type"] == "dag_chart"
        assert result["props"]["nodes"][0]["id"] == "X"

    def test_custom_height(self) -> None:
        """DAGChart supports custom height."""
        block = DAGChart(title="Tall", nodes=[], edges=[], height=800)
        assert block.to_props()["height"] == 800

    def test_in_report(self, tmp_path: Any) -> None:
        """DAGChart integrates with Report add + export_json."""
        r = Report(title="DAG Report")
        r.add(
            DAGChart(
                title="ETL",
                nodes=[{"id": "a", "label": "Src"}, {"id": "b", "label": "Sink"}],
                edges=[{"from": "a", "to": "b"}],
            )
        )
        out = tmp_path / "dag.json"
        r.export_json(out)
        data = json.loads(out.read_text())
        assert data["blocks"][0]["type"] == "dag_chart"


# ---------------------------------------------------------------------------
# CorrelationMatrix
# ---------------------------------------------------------------------------


class TestCorrelationMatrix:
    """Test CorrelationMatrix block model."""

    def test_basic(self) -> None:
        """CorrelationMatrix has correct type and basic props."""
        block = CorrelationMatrix(
            title="Feature Correlation",
            matrix=[[1.0, 0.5], [0.5, 1.0]],
            labels=["A", "B"],
        )
        assert block.type == "correlation_matrix"
        props = block.to_props()
        assert props["title"] == "Feature Correlation"
        assert props["matrix"] == [[1.0, 0.5], [0.5, 1.0]]
        assert props["labels"] == ["A", "B"]
        assert props["height"] == 400

    def test_3x3_matrix(self) -> None:
        """CorrelationMatrix handles 3x3 matrix."""
        block = CorrelationMatrix(
            title="3x3",
            matrix=[
                [1.0, 0.8, -0.3],
                [0.8, 1.0, 0.1],
                [-0.3, 0.1, 1.0],
            ],
            labels=["X", "Y", "Z"],
        )
        props = block.to_props()
        assert len(props["matrix"]) == 3
        assert len(props["labels"]) == 3

    def test_empty_matrix(self) -> None:
        """CorrelationMatrix can be created with empty matrix."""
        block = CorrelationMatrix(title="Empty")
        props = block.to_props()
        assert props["matrix"] == []
        assert props["labels"] == []

    def test_serialize(self) -> None:
        """CorrelationMatrix.serialize() returns correct structure."""
        block = CorrelationMatrix(
            title="Corr",
            matrix=[[1.0]],
            labels=["A"],
        )
        result = block.serialize("block_010")
        assert result["id"] == "block_010"
        assert result["type"] == "correlation_matrix"
        assert result["props"]["matrix"] == [[1.0]]

    def test_custom_height(self) -> None:
        """CorrelationMatrix supports custom height."""
        block = CorrelationMatrix(title="H", matrix=[], labels=[], height=500)
        assert block.to_props()["height"] == 500

    def test_negative_correlations(self) -> None:
        """CorrelationMatrix handles negative correlation values."""
        block = CorrelationMatrix(
            title="Negative",
            matrix=[[1.0, -1.0], [-1.0, 1.0]],
            labels=["P", "Q"],
        )
        props = block.to_props()
        assert props["matrix"][0][1] == -1.0

    def test_in_report(self, tmp_path: Any) -> None:
        """CorrelationMatrix integrates with Report add + export_json."""
        r = Report(title="Corr Report")
        r.add(
            CorrelationMatrix(
                title="Features",
                matrix=[[1.0, 0.5], [0.5, 1.0]],
                labels=["A", "B"],
            )
        )
        out = tmp_path / "corr.json"
        r.export_json(out)
        data = json.loads(out.read_text())
        assert data["blocks"][0]["type"] == "correlation_matrix"


# ---------------------------------------------------------------------------
# Scorecard
# ---------------------------------------------------------------------------


class TestScorecard:
    """Test Scorecard block model."""

    def test_basic(self) -> None:
        """Scorecard has correct type and basic props."""
        data = [
            {"metric": "Uptime", "value": 99.9},
            {"metric": "Latency", "value": 45},
        ]
        block = Scorecard(title="SLA Metrics", data=data)
        assert block.type == "scorecard"
        props = block.to_props()
        assert props["title"] == "SLA Metrics"
        assert len(props["data"]) == 2

    def test_with_thresholds(self) -> None:
        """Scorecard supports conditional thresholds."""
        block = Scorecard(
            title="Scores",
            data=[{"name": "Test", "score": 85}],
            value_column="score",
            thresholds={"green": ">90", "yellow": ">70", "red": "<=70"},
        )
        props = block.to_props()
        assert props["value_column"] == "score"
        assert props["thresholds"]["green"] == ">90"

    def test_with_explicit_columns(self) -> None:
        """Scorecard accepts explicit column names."""
        block = Scorecard(
            title="Custom",
            data=[{"a": 1, "b": 2, "c": 3}],
            columns=["a", "b"],
        )
        props = block.to_props()
        assert props["columns"] == ["a", "b"]

    def test_empty_data(self) -> None:
        """Scorecard can be created with no data."""
        block = Scorecard(title="Empty")
        props = block.to_props()
        assert props["data"] == []

    def test_serialize(self) -> None:
        """Scorecard.serialize() returns correct structure."""
        block = Scorecard(title="Test", data=[{"k": "v"}])
        result = block.serialize("block_020")
        assert result["id"] == "block_020"
        assert result["type"] == "scorecard"

    def test_in_report(self, tmp_path: Any) -> None:
        """Scorecard integrates with Report add + export_json."""
        r = Report(title="Scorecard Report")
        r.add(Scorecard(title="Metrics", data=[{"kpi": "Revenue", "val": 100}]))
        out = tmp_path / "scorecard.json"
        r.export_json(out)
        data = json.loads(out.read_text())
        assert data["blocks"][0]["type"] == "scorecard"


# ---------------------------------------------------------------------------
# DataProfile
# ---------------------------------------------------------------------------


class TestDataProfile:
    """Test DataProfile block model."""

    def test_basic(self) -> None:
        """DataProfile has correct type and basic props."""
        block = DataProfile(
            title="Data Overview",
            columns=[
                {
                    "name": "age",
                    "dtype": "int64",
                    "count": 1000,
                    "null_count": 5,
                    "null_pct": 0.5,
                    "unique": 80,
                    "mean": 35.2,
                    "std": 12.1,
                    "min": 18,
                    "max": 90,
                },
            ],
        )
        assert block.type == "data_profile"
        props = block.to_props()
        assert props["title"] == "Data Overview"
        assert len(props["columns"]) == 1
        assert props["columns"][0]["name"] == "age"
        assert props["columns"][0]["mean"] == 35.2

    def test_multiple_columns(self) -> None:
        """DataProfile handles multiple column profiles."""
        cols = [
            {
                "name": "id",
                "dtype": "int64",
                "count": 100,
                "null_count": 0,
                "null_pct": 0.0,
                "unique": 100,
            },
            {
                "name": "name",
                "dtype": "object",
                "count": 100,
                "null_count": 2,
                "null_pct": 2.0,
                "unique": 95,
            },
            {
                "name": "score",
                "dtype": "float64",
                "count": 100,
                "null_count": 10,
                "null_pct": 10.0,
                "unique": 50,
            },
        ]
        block = DataProfile(title="Profile", columns=cols)
        props = block.to_props()
        assert len(props["columns"]) == 3

    def test_with_top_values(self) -> None:
        """DataProfile column can include top_values."""
        block = DataProfile(
            title="Categorical",
            columns=[
                {
                    "name": "color",
                    "dtype": "object",
                    "count": 50,
                    "null_count": 0,
                    "null_pct": 0.0,
                    "unique": 3,
                    "top_values": [("red", 25), ("blue", 15), ("green", 10)],
                },
            ],
        )
        props = block.to_props()
        assert len(props["columns"][0]["top_values"]) == 3

    def test_empty_columns(self) -> None:
        """DataProfile can be created with no columns."""
        block = DataProfile(title="Empty")
        props = block.to_props()
        assert props["columns"] == []

    def test_serialize(self) -> None:
        """DataProfile.serialize() returns correct structure."""
        block = DataProfile(
            title="Profile",
            columns=[
                {
                    "name": "x",
                    "dtype": "int",
                    "count": 10,
                    "null_count": 0,
                    "null_pct": 0.0,
                    "unique": 5,
                }
            ],
        )
        result = block.serialize("block_030")
        assert result["id"] == "block_030"
        assert result["type"] == "data_profile"

    def test_in_report(self, tmp_path: Any) -> None:
        """DataProfile integrates with Report add + export_json."""
        r = Report(title="Profile Report")
        r.add(DataProfile(title="Data", columns=[]))
        out = tmp_path / "profile.json"
        r.export_json(out)
        data = json.loads(out.read_text())
        assert data["blocks"][0]["type"] == "data_profile"


# ---------------------------------------------------------------------------
# Compare
# ---------------------------------------------------------------------------


class TestCompare:
    """Test Compare block model."""

    def test_basic(self) -> None:
        """Compare has correct type and basic props."""
        block = Compare(
            left_label="Before",
            right_label="After",
            left_children=[KPI(label="Rev", value=100)],
            right_children=[KPI(label="Rev", value=150)],
        )
        assert block.type == "compare"

    def test_serialize(self) -> None:
        """Compare.serialize() returns correct structure with nested children."""
        block = Compare(
            left_label="Q3",
            right_label="Q4",
            left_children=[KPI(label="A", value=10)],
            right_children=[KPI(label="A", value=20)],
        )
        result = block.serialize("block_040", counter=40)
        assert result["id"] == "block_040"
        assert result["type"] == "compare"
        assert result["props"]["left_label"] == "Q3"
        assert result["props"]["right_label"] == "Q4"
        assert len(result["props"]["left_children"]) == 1
        assert len(result["props"]["right_children"]) == 1
        # Verify children are serialised
        assert result["props"]["left_children"][0]["type"] == "kpi"
        assert result["props"]["right_children"][0]["type"] == "kpi"

    def test_default_labels(self) -> None:
        """Compare has default labels A and B."""
        block = Compare()
        result = block.serialize("block_050", counter=0)
        assert result["props"]["left_label"] == "A"
        assert result["props"]["right_label"] == "B"

    def test_overlay_mode(self) -> None:
        """Compare supports overlay mode."""
        block = Compare(mode="overlay")
        result = block.serialize("block_060", counter=0)
        assert result["props"]["mode"] == "overlay"

    def test_side_by_side_mode(self) -> None:
        """Compare defaults to side_by_side mode."""
        block = Compare()
        result = block.serialize("block_070", counter=0)
        assert result["props"]["mode"] == "side_by_side"

    def test_empty_children(self) -> None:
        """Compare can be created with empty children."""
        block = Compare(left_label="L", right_label="R")
        result = block.serialize("block_080", counter=0)
        assert result["props"]["left_children"] == []
        assert result["props"]["right_children"] == []

    def test_multiple_children(self) -> None:
        """Compare handles multiple children per side."""
        block = Compare(
            left_children=[KPI(label="A", value=1), Markdown(content="## Left")],
            right_children=[KPI(label="B", value=2), Markdown(content="## Right")],
        )
        result = block.serialize("block_090", counter=90)
        assert len(result["props"]["left_children"]) == 2
        assert len(result["props"]["right_children"]) == 2

    def test_in_report(self, tmp_path: Any) -> None:
        """Compare integrates with Report add + export_json."""
        r = Report(title="Compare Report")
        r.add(
            Compare(
                left_label="Old",
                right_label="New",
                left_children=[KPI(label="Users", value=1000)],
                right_children=[KPI(label="Users", value=1500)],
            )
        )
        out = tmp_path / "compare.json"
        r.export_json(out)
        data = json.loads(out.read_text())
        assert data["blocks"][0]["type"] == "compare"
        assert data["blocks"][0]["props"]["left_label"] == "Old"


# ---------------------------------------------------------------------------
# Integration: All 6 new blocks in a single report
# ---------------------------------------------------------------------------


class TestAllNewBlockTypes:
    """Verify all 6 new v0.4.0 block types work together in a single report."""

    def test_comprehensive_new_blocks(self, tmp_path: Any) -> None:
        """All 6 new block types can be added to one report."""
        r = Report(title="v0.4.0 Showcase", theme="dark")

        r.add(
            GanttChart(
                title="Gantt",
                tasks=[{"name": "T1", "start": "2024-01-01", "end": "2024-06-30"}],
            )
        )
        r.add(
            DAGChart(
                title="DAG",
                nodes=[{"id": "a", "label": "A"}],
                edges=[],
            )
        )
        r.add(
            CorrelationMatrix(
                title="Corr",
                matrix=[[1.0, 0.5], [0.5, 1.0]],
                labels=["X", "Y"],
            )
        )
        r.add(
            Scorecard(
                title="Scores",
                data=[{"metric": "SLA", "value": 99.9}],
            )
        )
        r.add(
            DataProfile(
                title="Profile",
                columns=[
                    {
                        "name": "col",
                        "dtype": "int",
                        "count": 10,
                        "null_count": 0,
                        "null_pct": 0.0,
                        "unique": 5,
                    }
                ],
            )
        )
        r.add(
            Compare(
                left_label="A",
                right_label="B",
                left_children=[KPI(label="V", value=1)],
                right_children=[KPI(label="V", value=2)],
            )
        )

        # Verify schema
        schema = r.to_schema()
        assert len(schema.blocks) == 6

        # Verify JSON roundtrip
        json_str = r.to_json()
        parsed = json.loads(json_str)
        types = {b["type"] for b in parsed["blocks"]}
        expected = {
            "gantt_chart",
            "dag_chart",
            "correlation_matrix",
            "scorecard",
            "data_profile",
            "compare",
        }
        assert types == expected

        # Verify export_json
        out = tmp_path / "all_new.json"
        r.export_json(out)
        assert out.exists()
        data = json.loads(out.read_text())
        assert len(data["blocks"]) == 6
