"""
Aether Weaver — MCP Server
===========================
Exposes the Fabric Lore Weaver agent as MCP tools that work
directly inside GitHub Copilot Agent Mode in VS Code.

Tools available:
  - get_entity_lore      : Weave a poetic narrative for any Fabric IQ entity
  - list_fabric_entities : List all entities in the Fabric IQ ontology
  - get_fabric_health    : Get health summary of the entire data fabric
  - get_entity_lineage   : Get upstream/downstream connections for an entity

Setup (VS Code):
  1. pip install mcp
  2. Add to .vscode/mcp.json (see README for full config)
  3. Open GitHub Copilot Chat → switch to Agent mode
  4. Type: get the lore of the Sales Transactions Lakehouse

Microsoft Agents League 2026 · Creative Apps Track
Built with GitHub Copilot
"""

import json
import sys
from pathlib import Path

# Add project root to path so we can import our agents
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from agents.lore_weaver import (
    run as weave_lore,
    get_entity_by_id,
    get_entity_relationships,
)

# ── Initialise FastMCP server ──────────────────────────────────────
mcp = FastMCP(
    name="aether-weaver",
    instructions=(
        "You are connected to Aether Weaver — a Fabric IQ intelligence layer "
        "that transforms enterprise data entities into poetic narratives. "
        "Use get_entity_lore to generate a story for any entity, "
        "list_fabric_entities to discover available nodes, "
        "get_fabric_health for a team-level fabric overview, "
        "and get_entity_lineage to explore data connections."
    )
)

DATA_DIR = Path(__file__).parent / "data"


def _load_ontology() -> dict:
    """Load Fabric IQ synthetic ontology."""
    with open(DATA_DIR / "fabric_ontology.json") as f:
        return json.load(f)


# ── Tool 1: get_entity_lore ────────────────────────────────────────
@mcp.tool()
def get_entity_lore(entity_id: str) -> str:
    """
    Weave a poetic narrative for a Fabric IQ entity using the
    Fabric Lore Weaver agent. Returns the entity's archetype,
    health status, upstream/downstream lineage narrative,
    activity interpretation, and a grounded insight — all cited
    from the Fabric IQ synthetic ontology.

    Args:
        entity_id: The entity ID to narrate. Valid IDs are:
                   E001 (Sales Transactions Lakehouse),
                   E002 (POS Feeds Dataflow),
                   E003 (Sales KPI Semantic Model),
                   E004 (Daily Sales Report),
                   E005 (Customer 360 Warehouse - WARNING),
                   E006 (Churn Prediction Model - IDLE),
                   E007 (Inventory Event Stream)

    Returns:
        A formatted string containing the entity narrative,
        archetype, health status, activity stats, insight,
        and citation.
    """
    result = weave_lore(entity_id)

    if "error" in result:
        return f"Error: {result['error']}"

    # Format for clean Copilot display
    output = [
        f"# ✦ {result['entity_name']}",
        f"**Type:** {result['entity_type']}  |  "
        f"**Archetype:** {result['archetype']}  |  "
        f"**Health:** {result['health_status'].upper()}",
        "",
        "## The Lore Weaver Speaks",
        result['narrative'],
        "",
        "## Connections",
        f"- Upstream ({result['connections']['upstream_count']}): "
        f"{', '.join(result['connections']['upstream_names']) or 'None — primal source'}",
        f"- Downstream ({result['connections']['downstream_count']}): "
        f"{', '.join(result['connections']['downstream_names']) or 'None — terminal node'}",
        "",
        "## Activity (Last 24h)",
        f"- Reads: {result['activity_stats']['reads_24h']:,}",
        f"- Writes: {result['activity_stats']['writes_24h']:,}",
        f"- Refresh: every {result['activity_stats']['refresh_hours']}h"
        if result['activity_stats']['refresh_hours'] > 0
        else "- Refresh: continuous (real-time stream)",
        f"- Anomalies: {result['activity_stats']['anomaly_count']}",
        "",
        f"## Insight",
        result['insight'],
        "",
        f"*📎 {result['citation']}*",
    ]

    return "\n".join(output)


# ── Tool 2: list_fabric_entities ───────────────────────────────────
@mcp.tool()
def list_fabric_entities() -> str:
    """
    List all entities in the Fabric IQ synthetic ontology with
    their type, archetype, health status, and entity ID.
    Use the entity IDs with get_entity_lore to generate narratives.

    Returns:
        A formatted table of all 7 Fabric IQ entities.
    """
    ontology = _load_ontology()
    entities = ontology["entities"]

    health_icons = {
        "healthy": "🟢",
        "warning": "🟡",
        "idle": "🔵",
        "error": "🔴"
    }

    lines = [
        f"# ✦ Synthex Enterprise Data Fabric",
        f"**{len(entities)} entities** across {len(ontology['relationships'])} "
        f"data lineage connections",
        "",
        "| ID | Entity | Type | Archetype | Health |",
        "|---|---|---|---|---|",
    ]

    for e in entities:
        health = e["activity"]["health_status"]
        icon = health_icons.get(health, "⚪")
        name = e["name"].replace("_", " ")
        lines.append(
            f"| {e['id']} | {name} | {e['type']} | "
            f"{e['archetype']} | {icon} {health.upper()} |"
        )

    lines += [
        "",
        "Use `get_entity_lore` with any entity ID to hear its story.",
        "Use `get_fabric_health` for a full fabric health summary.",
    ]

    return "\n".join(lines)


# ── Tool 3: get_fabric_health ──────────────────────────────────────
@mcp.tool()
def get_fabric_health() -> str:
    """
    Get a health summary of the entire Synthex data fabric.
    Shows overall fabric status, entity health breakdown,
    total data activity in the last 24 hours, warning entities
    with their anomalies, and idle entities.

    Returns:
        A formatted health report of the full Fabric IQ ontology.
    """
    ontology = _load_ontology()
    entities = ontology["entities"]

    total_reads = sum(e["activity"]["reads_last_24h"] for e in entities)
    total_writes = sum(e["activity"]["writes_last_24h"] for e in entities)

    healthy = [e for e in entities if e["activity"]["health_status"] == "healthy"]
    warning = [e for e in entities if e["activity"]["health_status"] == "warning"]
    idle = [e for e in entities if e["activity"]["health_status"] == "idle"]
    error = [e for e in entities if e["activity"]["health_status"] == "error"]

    # Overall fabric health
    if error:
        overall = "🔴 CRITICAL"
    elif warning:
        overall = "🟡 WARNING"
    elif idle:
        overall = "🟢 HEALTHY (with idle nodes)"
    else:
        overall = "🟢 FULLY HEALTHY"

    lines = [
        f"# ✦ Synthex Fabric Health Report",
        f"**Overall Status:** {overall}",
        "",
        "## Entity Health Breakdown",
        f"- 🟢 Healthy: {len(healthy)}",
        f"- 🟡 Warning: {len(warning)}",
        f"- 🔵 Idle: {len(idle)}",
        f"- 🔴 Error: {len(error)}",
        "",
        "## Data Activity (Last 24h)",
        f"- Total Reads: {total_reads:,}",
        f"- Total Writes: {total_writes:,}",
        f"- Active Connections: {len(ontology['relationships'])}",
    ]

    if warning:
        lines += ["", "## ⚠️ Warning Entities"]
        for e in warning:
            name = e["name"].replace("_", " ")
            anomalies = e["activity"].get("anomalies", [])
            lines.append(f"**{name}** ({e['id']})")
            for a in anomalies:
                lines.append(f"  - {a}")

    if idle:
        lines += ["", "## 🔵 Idle Entities"]
        for e in idle:
            name = e["name"].replace("_", " ")
            hrs = e["activity"]["refresh_frequency_hours"]
            lines.append(
                f"**{name}** ({e['id']}) — "
                f"last refreshed {hrs}h ago"
            )

    lines += [
        "",
        "## High-Demand Entities (>5,000 reads/24h)",
    ]
    high_demand = [
        e for e in entities
        if e["activity"]["reads_last_24h"] > 5000
    ]
    if high_demand:
        for e in high_demand:
            name = e["name"].replace("_", " ")
            reads = e["activity"]["reads_last_24h"]
            lines.append(f"- **{name}** — {reads:,} reads")
    else:
        lines.append("- None")

    lines += [
        "",
        "*📎 Fabric IQ Synthetic Ontology — Synthex Enterprise Data Fabric (Demo)*",
        "*⚠️ All data is synthetic — for demonstration purposes only*",
    ]

    return "\n".join(lines)


# ── Tool 4: get_entity_lineage ─────────────────────────────────────
@mcp.tool()
def get_entity_lineage(entity_id: str) -> str:
    """
    Get the full data lineage for a Fabric IQ entity —
    showing its upstream data sources and downstream consumers,
    along with relationship types and throughput levels.

    Args:
        entity_id: The entity ID to explore lineage for.
                   Valid IDs: E001 through E007.

    Returns:
        A formatted lineage map showing upstream and downstream
        connections with relationship types and throughput.
    """
    entity = get_entity_by_id(entity_id)
    if "error" in entity:
        return f"Error: {entity['error']}"

    relationships = get_entity_relationships(entity_id)
    ontology = _load_ontology()

    # Build full relationship details
    all_rels = ontology["relationships"]
    name = entity["name"].replace("_", " ")

    lines = [
        f"# ✦ Data Lineage — {name}",
        f"**Type:** {entity['type']}  |  "
        f"**Archetype:** {entity['archetype']}",
        "",
    ]

    # Upstream
    upstream = relationships.get("upstream", [])
    lines.append(f"## ↑ Upstream Sources ({len(upstream)})")
    if upstream:
        for u in upstream:
            uname = u["name"].replace("_", " ")
            # Find relationship details
            rel = next(
                (r for r in all_rels
                 if r["from"] == u["id"] and r["to"] == entity_id),
                {}
            )
            rel_type = rel.get("type", "connects to")
            throughput = rel.get("throughput", "unknown")
            lines.append(
                f"- **{uname}** ({u['id']}) "
                f"→ _{rel_type}_ → {name} "
                f"[throughput: {throughput}]"
            )
    else:
        lines.append(
            "- *No upstream sources — this is a primal source node*"
        )

    lines.append("")

    # Downstream
    downstream = relationships.get("downstream", [])
    lines.append(f"## ↓ Downstream Consumers ({len(downstream)})")
    if downstream:
        for d in downstream:
            dname = d["name"].replace("_", " ")
            rel = next(
                (r for r in all_rels
                 if r["from"] == entity_id and r["to"] == d["id"]),
                {}
            )
            rel_type = rel.get("type", "connects to")
            throughput = rel.get("throughput", "unknown")
            lines.append(
                f"- {name} → _{rel_type}_ → "
                f"**{dname}** ({d['id']}) "
                f"[throughput: {throughput}]"
            )
    else:
        lines.append(
            "- *No downstream consumers — this is a terminal node*"
        )

    total = len(upstream) + len(downstream)
    lines += [
        "",
        f"**Total connections:** {total}",
        "",
        f"*📎 Fabric IQ Synthetic Ontology — Synthex Enterprise Data Fabric (Demo)*",
    ]

    return "\n".join(lines)


# ── Entry point ────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")


# ── Tool 5: compare_entities ───────────────────────────────────────
@mcp.tool()
def compare_entities(entity_id_a: str, entity_id_b: str) -> str:
    """
    Compare two Fabric IQ entities side by side — contrasting their
    archetypes, health status, activity levels, and lineage positions.
    Returns a narrative contrast revealing how they relate within
    the broader data fabric story.

    Args:
        entity_id_a: First entity ID (e.g. E001)
        entity_id_b: Second entity ID (e.g. E005)

    Returns:
        Side-by-side comparison table + narrative contrast.
    """
    entity_a = get_entity_by_id(entity_id_a)
    entity_b = get_entity_by_id(entity_id_b)

    if "error" in entity_a:
        return f"Error: {entity_a['error']}"
    if "error" in entity_b:
        return f"Error: {entity_b['error']}"

    rel_a = get_entity_relationships(entity_id_a)
    rel_b = get_entity_relationships(entity_id_b)

    name_a = entity_a["name"].replace("_", " ")
    name_b = entity_b["name"].replace("_", " ")
    act_a = entity_a["activity"]
    act_b = entity_b["activity"]

    a_downstream_ids = [d["id"] for d in rel_a.get("downstream", [])]
    a_upstream_ids = [u["id"] for u in rel_a.get("upstream", [])]

    if entity_id_b in a_upstream_ids:
        relationship = f"**{name_b}** feeds into **{name_a}** — they are directly connected."
    elif entity_id_b in a_downstream_ids:
        relationship = f"**{name_a}** feeds into **{name_b}** — they are directly connected."
    else:
        relationship = f"**{name_a}** and **{name_b}** operate as independent nodes in the fabric."

    health_map = {"healthy": "thriving", "warning": "troubled",
                  "idle": "dormant", "error": "broken"}
    mood_a = health_map.get(act_a["health_status"], "present")
    mood_b = health_map.get(act_b["health_status"], "present")
    reads_a = act_a["reads_last_24h"]
    reads_b = act_b["reads_last_24h"]

    if reads_a > reads_b * 2:
        activity_contrast = f"**{name_a}** commands far greater attention ({reads_a:,} vs {reads_b:,} reads/24h)."
    elif reads_b > reads_a * 2:
        activity_contrast = f"**{name_b}** commands far greater attention ({reads_b:,} vs {reads_a:,} reads/24h)."
    else:
        activity_contrast = f"Both attract similar levels of attention ({reads_a:,} vs {reads_b:,} reads/24h)."

    lines = [
        f"# ✦ Fabric Contrast — {name_a} vs {name_b}",
        "",
        f"## Relationship",
        relationship,
        "",
        "## Side-by-Side Comparison",
        f"| Attribute | {name_a} | {name_b} |",
        "|---|---|---|",
        f"| Type | {entity_a['type']} | {entity_b['type']} |",
        f"| Archetype | {entity_a['archetype']} | {entity_b['archetype']} |",
        f"| Health | {act_a['health_status'].upper()} | {act_b['health_status'].upper()} |",
        f"| Reads/24h | {reads_a:,} | {reads_b:,} |",
        f"| Writes/24h | {act_a['writes_last_24h']:,} | {act_b['writes_last_24h']:,} |",
        f"| Anomalies | {len(act_a.get('anomalies', []))} | {len(act_b.get('anomalies', []))} |",
        f"| Upstream | {len(rel_a.get('upstream', []))} | {len(rel_b.get('upstream', []))} |",
        f"| Downstream | {len(rel_a.get('downstream', []))} | {len(rel_b.get('downstream', []))} |",
        "",
        "## Narrative Contrast",
        (
            f"Where **{name_a}** stands {mood_a} at the heart of its domain, "
            f"**{name_b}** moves through the fabric in a state of {mood_b} purpose. "
            f"{activity_contrast} "
            f"One bears the archetype of {entity_a['archetype']} — the other, {entity_b['archetype']}. "
            f"Together they reveal the balance of forces that animate the Synthex data fabric."
        ),
        "",
        "*📎 Fabric IQ Synthetic Ontology — Synthex Enterprise Data Fabric (Demo)*",
    ]

    return "\n".join(lines)
