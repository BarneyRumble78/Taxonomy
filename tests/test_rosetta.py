"""Rosetta layer: formal cores, translation, holes, distances, derived edges."""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
import correspondences as corr  # noqa: E402
import rosetta  # noqa: E402


@pytest.fixture(scope="module")
def cores():
    return rosetta.load(ROOT)


@pytest.fixture(scope="module")
def graph(cores):
    return rosetta.Graph(ROOT, cores=cores)


def write_cores(tmp_path, cores):
    """A scratch repo root holding altered cores and the real schemas, pyramids and maps."""
    for name in ("schemas", "pyramids", "maps", "cards"):
        (tmp_path / name).symlink_to(ROOT / name)
    (tmp_path / "rosetta").mkdir()
    (tmp_path / "rosetta" / "cores.json").write_text(json.dumps({"cores": cores}), encoding="utf-8")
    return tmp_path


def test_seed_is_clean():
    assert rosetta.check(ROOT) == []


def test_every_core_is_draft_and_spans_fields(cores):
    assert len(cores) >= 12
    for core in cores:
        assert core["status"] == "draft"
        assert len({b["field"] for b in core["bindings"]}) >= 3


def test_every_binding_states_where_it_breaks(cores):
    for core in cores:
        for binding in core["bindings"]:
            assert binding["breaks"], (core["id"], binding["tool"])


def test_translate_maps_every_role(cores):
    core = rosetta.core_by_id(cores, "RC-diffusion")
    view = rosetta.translate(core, rosetta.one_binding(core, "PH"), rosetta.one_binding(core, "EC"))
    assert [r["role"] for r in view["roles"]] == list(core["roles"])
    by_role = {r["role"]: r for r in view["roles"]}
    assert "volatility" in by_role["diffusivity"]["target"]
    assert view["status"] == "generated-unverified"


def test_translate_reports_differences_and_withholds_the_guarantee(cores):
    core = rosetta.core_by_id(cores, "RC-diffusion")
    view = rosetta.translate(core, rosetta.one_binding(core, "PH"), rosetta.one_binding(core, "EC"))
    verdicts = {a["id"]: a["verdict"] for a in view["assumptions"]}
    assert verdicts["a2"] == "differs"
    assert view["guarantee_carries"] is False
    assert view["breaks_in_target"]


def test_guarantee_carries_only_when_all_assumptions_hold_in_both(cores):
    core = copy.deepcopy(rosetta.core_by_id(cores, "RC-network-laplacian"))
    left = rosetta.one_binding(core, "EN", "Resistor")
    right = copy.deepcopy(left)
    assert rosetta.translate(core, left, right)["guarantee_carries"] is True
    right["assumptions_met"]["a1"] = "?"
    view = rosetta.translate(core, left, right)
    assert view["guarantee_carries"] is False
    assert {a["id"]: a["verdict"] for a in view["assumptions"]}["a1"] == "not known"


def test_ambiguous_and_missing_bindings_are_errors(cores):
    core = rosetta.core_by_id(cores, "RC-network-laplacian")
    with pytest.raises(rosetta.RosettaError, match="2 bindings"):
        rosetta.one_binding(core, "EN")
    with pytest.raises(rosetta.RosettaError, match="no binding"):
        rosetta.one_binding(core, "LA")
    with pytest.raises(rosetta.RosettaError, match="unknown core"):
        rosetta.core_by_id(cores, "RC-nope")


def test_holes_are_questions_and_skip_bound_fields(cores):
    found = rosetta.holes(cores, core_id="RC-branching-threshold")
    fields = {h["field"] for h in found}
    assert "EC" in fields and "MD" not in fields and "MA" not in fields
    for hole in found:
        assert hole["status"] == "open question"
        assert len(hole["ask_roles"]) == 3 and len(hole["ask_assumptions"]) == 3


def test_holes_reject_unknown_field(cores):
    with pytest.raises(rosetta.RosettaError):
        rosetta.holes(cores, field="ZZ")


def test_find_matches_bindings_and_rejects_empty(cores):
    hits = rosetta.find("random link", cores)
    assert any(h.get("field") == "CS" and h["core"] == "RC-markov-stationary" for h in hits)
    assert rosetta.find("zzzzqqq", cores) == []
    with pytest.raises(rosetta.RosettaError):
        rosetta.find("  ", cores)


# ---- distances

def test_lineage_distance_near_and_far(graph):
    assert graph.distance("PH.O.A5.1", "PH.O.A5.1") == 0
    assert graph.distance("PH.O.A5.1", "PH.O.A5") == 1
    shared_core = graph.distance("PH.O.A5.1", "EC.O.A1.2")       # both bind diffusion
    unrelated = graph.distance("PH.O.A5.1", "LA.O.A1")
    assert shared_core == 2
    assert unrelated > shared_core


def test_cores_shorten_cross_field_distance(cores):
    bare = rosetta.Graph(ROOT, cores=cores, use_cores=False, use_edges=False)
    full = rosetta.Graph(ROOT, cores=cores)
    assert bare.distance("MD.O.A5.2", "EN.O.A5.5") == 6      # up to the root and down again
    assert full.distance("MD.O.A5.2", "EN.O.A5.5") == 2      # both are branching thresholds


def test_lineage_distance_is_a_metric_on_a_sample(graph):
    nodes = ["PH.O.A5.1", "EC.O.A1.2", "BI.O.A4.1", "MD.O.A5.2", "EN.O.A4.1", "CS.O.A4.2", "LA", "MSC:35Kxx"]
    d = {(a, b): graph.distance(a, b) for a in nodes for b in nodes}
    for a in nodes:
        assert d[a, a] == 0
        for b in nodes:
            assert d[a, b] == d[b, a]
            assert (d[a, b] == 0) == (a == b)
            for c in nodes:
                assert d[a, c] <= d[a, b] + d[b, c]


def test_path_explains_each_link(graph):
    steps = graph.explain("PH.O.A5.1", "EC.O.A1.2")
    assert [s["via"] for s in steps] == ["binding", "binding"]


def test_unknown_node_is_an_error(graph):
    with pytest.raises(rosetta.RosettaError):
        graph.distance("PH.O.A5.1", "not-a-node")


def test_assumption_distance(cores):
    core = rosetta.core_by_id(cores, "RC-network-laplacian")
    resistor = rosetta.one_binding(core, "EN", "Resistor")
    pipes = rosetta.one_binding(core, "EN", "Pipe")
    assert rosetta.assumption_distance(core, resistor, core, resistor) == 0.0
    assert rosetta.assumption_distance(core, resistor, core, pipes) == pytest.approx(0.25)
    assert rosetta.assumption_distance(core, resistor, core, pipes) == rosetta.assumption_distance(core, pipes, core, resistor)
    other = rosetta.core_by_id(cores, "RC-diffusion")
    assert rosetta.assumption_distance(core, resistor, other, rosetta.one_binding(other, "PH")) == 1.0


# ---- derived edges

def test_derived_edges_validate_and_carry_mappings(cores):
    edges = rosetta.derived_edges(cores)
    assert len(edges) >= 90
    for edge in edges:
        assert edge["status"] == "generated-unverified"
        assert edge["provenance"]["origin"] == "formal-core"
        assert edge["mapping"]["objects"] and edge["mapping"]["methods"]
        assert edge["breaks_where"]
        assert edge["source"] != edge["target"]


def test_stored_edges_match_the_cores(cores):
    stored = json.loads((ROOT / "correspondences" / "rosetta_edges.json").read_text(encoding="utf-8"))["edges"]
    assert stored == rosetta.derived_edges(cores)
    assert corr.check(ROOT) == []


# ---- validation catches bad data

@pytest.mark.parametrize("change, expect", [
    (lambda c: c[0]["bindings"][0]["roles"].pop("gain"), "roles differ"),
    (lambda c: c[0]["bindings"][0]["assumptions_met"].update(a9="y"), "assumptions_met differs"),
    (lambda c: c[0]["bindings"][0].update(cell="PH.O.A1.1"), "belongs to PH"),
    (lambda c: c[0]["bindings"][0].update(cell="EN.O.A99"), "does not resolve"),
    (lambda c: c[0].update(ma_node="PhySH:nope"), "not a mathematics node"),
    (lambda c: c[0]["bindings"][0].update(breaks=[]), "schema"),
    (lambda c: c[0]["bindings"][0].update(maturity="proven"), "schema"),
    (lambda c: c.append(copy.deepcopy(c[0])), "duplicate core id"),
])
def test_bad_cores_are_reported(tmp_path, cores, change, expect):
    altered = copy.deepcopy(cores)
    change(altered)
    problems = rosetta.check(write_cores(tmp_path, altered))
    assert any(expect in p for p in problems), problems


def test_missing_data_is_an_error_not_an_empty_result(tmp_path):
    with pytest.raises(rosetta.RosettaError):
        rosetta.load(tmp_path)
    assert rosetta.check(tmp_path) == ["rosetta/cores.json not found"]


def test_cli_exit_codes(capsys):
    assert rosetta.main(["translate", "RC-diffusion", "PH", "EC"]) == 0
    assert json.loads(capsys.readouterr().out)["core"] == "RC-diffusion"
    assert rosetta.main(["translate", "RC-nope", "PH", "EC"]) == 2
    assert "unknown core" in capsys.readouterr().err
