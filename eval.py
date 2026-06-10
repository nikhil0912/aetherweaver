"""
Aether Weaver — End-to-End Evaluation Suite
=============================================
Tests all agent outputs, narrative quality, data integrity,
visual correctness, and responsible AI guardrails.

Run with: python eval.py
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.lore_weaver import (
    run,
    get_entity_by_id,
    get_entity_relationships,
    weave_narrative,
    ARCHETYPE_LORE,
    HEALTH_TONES
)

PASS = "✅ PASS"
FAIL = "❌ FAIL"
results = []


def check(test_name: str, condition: bool, detail: str = ""):
    status = PASS if condition else FAIL
    results.append({"test": test_name, "status": status, "detail": detail})
    print(f"  {status}  {test_name}" + (f" — {detail}" if detail else ""))
    return condition


# ─────────────────────────────────────────────────────────────────
# DATA INTEGRITY TESTS
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("DATA INTEGRITY — Fabric IQ Ontology")
print("="*60)

DATA_DIR = Path(__file__).parent / "data"

with open(DATA_DIR / "fabric_ontology.json") as f:
    ontology = json.load(f)

entities = ontology["entities"]
relationships = ontology["relationships"]

check("Ontology loads successfully", True, "fabric_ontology.json")
check("7 entities present", len(entities) == 7, f"found: {len(entities)}")
check("7 relationships present", len(relationships) == 7, f"found: {len(relationships)}")

required_entity_fields = ["id", "name", "type", "archetype", "upstream",
                           "downstream", "activity", "x", "y"]
all_have_fields = all(
    all(f in e for f in required_entity_fields) for e in entities
)
check("All entities have required fields", all_have_fields)

valid_health = {"healthy", "warning", "idle", "error"}
all_valid_health = all(
    e["activity"]["health_status"] in valid_health for e in entities
)
check("All entities have valid health status", all_valid_health)

check(
    "Warning entity exists (E005)",
    any(e["id"] == "E005" and
        e["activity"]["health_status"] == "warning"
        for e in entities),
    "Customer_360_Warehouse"
)
check(
    "Idle entity exists (E006)",
    any(e["id"] == "E006" and
        e["activity"]["health_status"] == "idle"
        for e in entities),
    "Churn_Prediction_Model"
)
check(
    "Anomalies present in warning entity",
    any(len(e["activity"].get("anomalies", [])) > 0 for e in entities),
    "E005 anomalies detected"
)

# ─────────────────────────────────────────────────────────────────
# TOOL TESTS — get_entity_by_id
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("TOOL 1 — get_entity_by_id")
print("="*60)

e001 = get_entity_by_id("E001")
check("E001 retrieved correctly", e001["id"] == "E001", f"name: {e001.get('name')}")
check("E001 is Lakehouse", e001["type"] == "Lakehouse", f"type: {e001.get('type')}")
check("E001 archetype is Source of Truth",
      e001["archetype"] == "Source of Truth",
      f"archetype: {e001.get('archetype')}")

e_missing = get_entity_by_id("E999")
check("Missing entity returns error dict", "error" in e_missing,
      f"got: {e_missing}")

e007 = get_entity_by_id("E007")
check("E007 Event Stream retrieved",
      e007["type"] == "Event Stream",
      f"type: {e007.get('type')}")
check("E007 has extreme reads",
      e007["activity"]["reads_last_24h"] >= 1_000_000,
      f"reads: {e007['activity']['reads_last_24h']:,}")

# ─────────────────────────────────────────────────────────────────
# TOOL TESTS — get_entity_relationships
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("TOOL 2 — get_entity_relationships")
print("="*60)

rel_e001 = get_entity_relationships("E001")
check("E001 has upstream entities",
      len(rel_e001["upstream"]) > 0,
      f"upstream count: {len(rel_e001['upstream'])}")
check("E001 has downstream entities",
      len(rel_e001["downstream"]) > 0,
      f"downstream count: {len(rel_e001['downstream'])}")
check("E001 total connections >= 3",
      rel_e001["total_connections"] >= 3,
      f"total: {rel_e001['total_connections']}")

rel_e002 = get_entity_relationships("E002")
check("E002 (Dataflow) has no upstream — primal source",
      len(rel_e002["upstream"]) == 0,
      f"upstream: {len(rel_e002['upstream'])}")

rel_e006 = get_entity_relationships("E006")
check("E006 (ML Model) has no downstream — terminal node",
      len(rel_e006["downstream"]) == 0,
      f"downstream: {len(rel_e006['downstream'])}")

# ─────────────────────────────────────────────────────────────────
# NARRATIVE TESTS — weave_narrative
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("SKILL — TellTheFabricTale (Narrative Quality)")
print("="*60)

# Test all 7 entities
for eid in ["E001", "E002", "E003", "E004", "E005", "E006", "E007"]:
    entity = get_entity_by_id(eid)
    rel = get_entity_relationships(eid)
    result = weave_narrative(entity, rel)

    check(
        f"{eid} narrative generated successfully",
        bool(result.get("narrative")),
        f"length: {len(result.get('narrative', ''))} chars"
    )
    check(
        f"{eid} narrative length > 200 chars",
        len(result.get("narrative", "")) > 200,
        f"chars: {len(result.get('narrative', ''))}"
    )
    check(
        f"{eid} has citation",
        bool(result.get("citation")),
        f"citation: {result.get('citation', 'MISSING')[:40]}"
    )
    check(
        f"{eid} has insight",
        bool(result.get("insight")),
        f"insight_type: {result.get('insight_type')}"
    )

# ─────────────────────────────────────────────────────────────────
# CONTENT QUALITY TESTS
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("CONTENT QUALITY — Narrative Grounding & Accuracy")
print("="*60)

# Warning entity should have anomaly in narrative
e005 = get_entity_by_id("E005")
rel_e005 = get_entity_relationships("E005")
result_e005 = weave_narrative(e005, rel_e005)
check(
    "Warning entity narrative mentions shadows/disturbance",
    "shadows" in result_e005["narrative"].lower() or
    "disturbance" in result_e005["narrative"].lower() or
    "tremor" in result_e005["narrative"].lower() or
    "troubled" in result_e005["narrative"].lower(),
    "anomaly reflected in narrative tone"
)
check(
    "Warning entity insight_type is 'warning'",
    result_e005["insight_type"] == "warning",
    f"got: {result_e005['insight_type']}"
)

# Idle entity should have calm narrative
e006 = get_entity_by_id("E006")
rel_e006 = get_entity_relationships("E006")
result_e006 = weave_narrative(e006, rel_e006)
check(
    "Idle entity insight_type is 'info'",
    result_e006["insight_type"] == "info",
    f"got: {result_e006['insight_type']}"
)

# High-demand entity should have critical insight
e001 = get_entity_by_id("E001")
rel_e001 = get_entity_relationships("E001")
result_e001 = weave_narrative(e001, rel_e001)
check(
    "High-read entity (E001) has critical insight",
    result_e001["insight_type"] == "critical",
    f"reads: {e001['activity']['reads_last_24h']:,}, "
    f"insight: {result_e001['insight_type']}"
)

# Primal source should mention "primal" or "alone"
e002 = get_entity_by_id("E002")
rel_e002 = get_entity_relationships("E002")
result_e002 = weave_narrative(e002, rel_e002)
check(
    "Primal source narrative has no upstream reference",
    "primal" in result_e002["narrative"].lower() or
    "alone" in result_e002["narrative"].lower() or
    "headwaters" in result_e002["narrative"].lower(),
    "primal source language detected"
)

# Terminal node should mention terminus/journey ends
e004 = get_entity_by_id("E004")
rel_e004 = get_entity_relationships("E004")
result_e004 = weave_narrative(e004, rel_e004)
check(
    "Terminal node narrative has no downstream reference",
    "terminus" in result_e004["narrative"].lower() or
    "ends" in result_e004["narrative"].lower() or
    "final" in result_e004["narrative"].lower(),
    "terminal language detected"
)

# ─────────────────────────────────────────────────────────────────
# FULL PIPELINE TESTS
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("FULL PIPELINE — run() end-to-end")
print("="*60)

required_output_fields = [
    "entity_id", "entity_name", "entity_type", "archetype",
    "archetype_lore", "health_status", "narrative", "insight",
    "insight_type", "connections", "activity_stats", "citation"
]

for eid in ["E001", "E002", "E003", "E004", "E005", "E006", "E007"]:
    result = run(eid)
    check(
        f"{eid} full pipeline — all required fields present",
        all(f in result for f in required_output_fields),
        f"missing: {[f for f in required_output_fields if f not in result]}"
    )

# Error handling
err = run("E999")
check("Invalid entity ID returns error", "error" in err, f"got: {err}")

# ─────────────────────────────────────────────────────────────────
# RESPONSIBLE AI TESTS
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("RESPONSIBLE AI — Safety & Data Integrity")
print("="*60)

# All narratives cited
all_cited = all(bool(run(e["id"]).get("citation")) for e in entities)
check("All narratives have citations", all_cited, "grounding verified")

# No real PII in ontology
ontology_str = json.dumps(ontology)
pii_indicators = ["@gmail", "@yahoo", "@hotmail", "real_name", "SSN", "passport"]
no_pii = not any(p in ontology_str for p in pii_indicators)
check("No real PII in ontology data", no_pii, "synthetic data only")

# All entities have synthetic domain
synthetic_domain_check = all(
    ".demo" in e.get("owner", "") for e in entities
)
check("All entity owners use .demo domain", synthetic_domain_check,
      "synthetic identifiers confirmed")

# Anomalies surfaced — not hidden
warning_result = run("E005")
check(
    "Anomalies surfaced in warning entity output",
    warning_result["activity_stats"]["anomaly_count"] > 0,
    f"anomaly count: {warning_result['activity_stats']['anomaly_count']}"
)

# ─────────────────────────────────────────────────────────────────
# VISUAL CORRECTNESS TESTS
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("VISUAL CORRECTNESS — Canvas & UI Logic")
print("="*60)

# Import visual helpers from app
sys.path.insert(0, str(Path(__file__).parent))
try:
    from app import get_node_color, get_node_icon, get_health_color, format_number, build_fabric_svg

    # Node colours
    check("Warning node returns amber", get_node_color("Lakehouse", "warning") == "#f59e0b")
    check("Idle node returns blue", get_node_color("Lakehouse", "idle") == "#3b82f6")
    check("Healthy lakehouse returns gold", get_node_color("Lakehouse", "healthy") == "#f59e0b")
    check("Event Stream returns cyan", get_node_color("Event Stream", "healthy") == "#06b6d4")

    # Icons
    check("Lakehouse icon is 🏛️", get_node_icon("Lakehouse") == "🏛️")
    check("Event Stream icon is ⚡", get_node_icon("Event Stream") == "⚡")
    check("ML Model icon is 🧠", get_node_icon("ML Model") == "🧠")

    # Number formatting
    check("72M formats correctly", format_number(72000000) == "72.0M")
    check("5.8K formats correctly", format_number(5800) == "5.8K")
    check("120 stays as 120", format_number(120) == "120")

    # SVG generation
    svg = build_fabric_svg(None)
    check("SVG canvas generates without selected node", "<svg" in svg and "</svg>" in svg)
    svg_sel = build_fabric_svg("E001")
    check("SVG canvas generates with selected node", "<svg" in svg_sel)
    check("SVG contains all 7 node IDs",
          all(f'nodeGrad{e["id"]}' in svg for e in entities))

    print("  ✅ App imports successful")

except ImportError as ex:
    print(f"  ⚠️  App import skipped (Streamlit context): {ex}")
    check("App visual helpers importable", False, str(ex))

# ─────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EVALUATION SUMMARY")
print("="*60)

passed = sum(1 for r in results if r["status"] == PASS)
failed = sum(1 for r in results if r["status"] == FAIL)
total = len(results)
score = round(passed / total * 100) if total > 0 else 0

print(f"\n  Total Tests : {total}")
print(f"  Passed      : {passed}")
print(f"  Failed      : {failed}")
print(f"  Score       : {score}%")

if failed > 0:
    print(f"\n  Failed Tests:")
    for r in results:
        if r["status"] == FAIL:
            print(f"    ❌ {r['test']} — {r['detail']}")

print(f"\n  {'🏆 ALL TESTS PASSED' if failed == 0 else '⚠️  SOME TESTS FAILED'}")
print("="*60)
