"""
Fabric Lore Weaver Agent
=========================
The creative heart of Aether Weaver. Transforms Fabric IQ entity
metadata into poetic, metaphorical narratives using a multi-step
reasoning pipeline — grounded in the ontology, never hallucinated.

GitHub Copilot SDK skill: TellTheFabricTale
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# ── Archetype Templates (Foundry IQ knowledge base) ────────────────
ARCHETYPE_LORE = {
    "Source of Truth": {
        "symbol": "ancient spring",
        "role": "the origin from which all knowing flows",
        "metaphor": "a vast underground reservoir, patient and deep",
        "color_essence": "molten gold"
    },
    "Transformer": {
        "symbol": "alchemist's forge",
        "role": "the great transmuter, turning raw ore into refined knowing",
        "metaphor": "a cosmic smithy where raw signals become structured meaning",
        "color_essence": "emerald fire"
    },
    "Oracle": {
        "symbol": "the all-seeing lens",
        "role": "the keeper of meaning, translator of the fabric's language",
        "metaphor": "a crystal prism that bends raw data into business truth",
        "color_essence": "royal violet"
    },
    "Deliverer": {
        "symbol": "the herald",
        "role": "the voice that carries the fabric's wisdom to the outer world",
        "metaphor": "a lighthouse whose beam reaches the farthest shores of the enterprise",
        "color_essence": "arctic white"
    },
    "Guardian": {
        "symbol": "the citadel",
        "role": "the protector of unified identity, keeper of the whole customer truth",
        "metaphor": "a fortified temple where fragmented truths are unified into one",
        "color_essence": "deep amber"
    },
    "Seer": {
        "symbol": "the dreaming eye",
        "role": "the prophet who reads tomorrow's patterns in today's data",
        "metaphor": "a dormant oracle that wakes only to whisper futures",
        "color_essence": "deep indigo"
    },
    "Pulse": {
        "symbol": "the heartbeat",
        "role": "the living rhythm of the fabric, never ceasing, never sleeping",
        "metaphor": "the eternal drumbeat that keeps the fabric's time",
        "color_essence": "electric cyan"
    }
}

# ── Health Status Narrative Tones ──────────────────────────────────
HEALTH_TONES = {
    "healthy": {
        "mood": "vibrant and harmonious",
        "energy": "golden light flows freely through its connections",
        "atmosphere": "serene confidence"
    },
    "warning": {
        "mood": "tense and uncertain",
        "energy": "amber warnings flicker at its edges like troubled flames",
        "atmosphere": "a gathering storm that has not yet broken"
    },
    "idle": {
        "mood": "still and meditative",
        "energy": "cool blue light pulses slowly, patient as deep ocean",
        "atmosphere": "the quiet of a held breath"
    },
    "error": {
        "mood": "fractured and urgent",
        "energy": "crimson fractures spider across its surface",
        "atmosphere": "the chaos of a broken circuit"
    }
}

# ── Type Descriptions ──────────────────────────────────────────────
TYPE_ESSENCE = {
    "Lakehouse": "a great hall where structured and unstructured truths coexist",
    "Dataflow": "a river that never stops its transformation journey",
    "Semantic Model": "the dictionary of meaning that all agents consult",
    "Power BI Report": "a living tapestry visible to all who seek understanding",
    "Data Warehouse": "a fortified vault where curated knowledge is preserved",
    "ML Model": "a dreaming mind trained on the patterns of the past",
    "Event Stream": "an eternal river of now, a torrent of perpetual present"
}


def get_entity_by_id(entity_id: str) -> dict:
    """Retrieve entity from Fabric IQ synthetic ontology."""
    with open(DATA_DIR / "fabric_ontology.json") as f:
        ontology = json.load(f)
    entity = next(
        (e for e in ontology["entities"] if e["id"] == entity_id), None
    )
    if not entity:
        return {"error": f"Entity {entity_id} not found in Fabric IQ"}
    return entity


def get_entity_relationships(entity_id: str) -> dict:
    """Get upstream and downstream relationships from ontology."""
    with open(DATA_DIR / "fabric_ontology.json") as f:
        ontology = json.load(f)

    entity_map = {e["id"]: e for e in ontology["entities"]}
    entity = entity_map.get(entity_id)
    if not entity:
        return {}

    upstream_entities = [
        entity_map[uid] for uid in entity.get("upstream", [])
        if uid in entity_map
    ]
    downstream_entities = [
        entity_map[did] for did in entity.get("downstream", [])
        if did in entity_map
    ]

    return {
        "upstream": upstream_entities,
        "downstream": downstream_entities,
        "total_connections": len(upstream_entities) + len(downstream_entities)
    }


def weave_narrative(entity: dict, relationships: dict) -> dict:
    """
    TellTheFabricTale skill — multi-step narrative generation.

    Step 1: Archetype identification
    Step 2: Health mood determination
    Step 3: Opening statement crafting
    Step 4: Lineage narrative weaving
    Step 5: Activity event interpretation
    Step 6: Prophetic closing
    """

    archetype = entity.get("archetype", "Source of Truth")
    health = entity.get("activity", {}).get("health_status", "healthy")
    entity_type = entity.get("type", "Lakehouse")
    name = entity.get("name", "Unknown Entity")
    activity = entity.get("activity", {})
    anomalies = activity.get("anomalies", [])

    # ── Step 1: Resolve archetype lore ────────────────────────────
    lore = ARCHETYPE_LORE.get(archetype, ARCHETYPE_LORE["Source of Truth"])
    tone = HEALTH_TONES.get(health, HEALTH_TONES["healthy"])
    type_essence = TYPE_ESSENCE.get(entity_type, "a node in the fabric")

    # ── Step 2: Build upstream narrative ──────────────────────────
    upstream = relationships.get("upstream", [])
    downstream = relationships.get("downstream", [])

    upstream_clause = ""
    if upstream:
        sources = " and ".join(
            f"*{u['name'].replace('_', ' ')}*" for u in upstream
        )
        upstream_clause = (
            f"It draws its life from {sources}, "
            f"receiving {'their' if len(upstream) > 1 else 'its'} "
            f"essence through channels of light and data."
        )
    else:
        upstream_clause = (
            "It stands alone at the headwaters — "
            "a primal source, drawing from no other, "
            "the first utterance in the fabric's long song."
        )

    # ── Step 3: Build downstream narrative ────────────────────────
    downstream_clause = ""
    if downstream:
        destinations = " and ".join(
            f"*{d['name'].replace('_', ' ')}*" for d in downstream
        )
        downstream_clause = (
            f"From its depths, rivers of knowing flow outward "
            f"toward {destinations}, "
            f"carrying the transformed light of its purpose."
        )
    else:
        downstream_clause = (
            "Here the journey ends — no further rivers flow from this place. "
            "It is a terminus, a final form where data becomes pure knowing."
        )

    # ── Step 4: Activity pulse narrative ──────────────────────────
    reads = activity.get("reads_last_24h", 0)
    writes = activity.get("writes_last_24h", 0)
    refresh_hz = activity.get("refresh_frequency_hours", 24)

    if reads > 10000:
        activity_clause = (
            f"In the last turning of the sun, {reads:,} minds "
            f"reached into its depths to draw wisdom — "
            f"a cacophony of queries, a testament to its indispensability."
        )
    elif reads > 1000:
        activity_clause = (
            f"A steady stream of {reads:,} inquiries "
            f"has flowed through it in the past day — "
            f"consistent, purposeful, unhurried."
        )
    else:
        activity_clause = (
            f"It has been consulted {reads:,} times in recent hours — "
            f"quiet, but present, awaiting its moment."
        )

    if refresh_hz == 0:
        refresh_clause = "Its pulse is eternal, a ceaseless torrent of now."
    elif refresh_hz <= 1:
        refresh_clause = "Every hour it renews itself, a perpetual act of becoming."
    elif refresh_hz <= 6:
        refresh_clause = (
            f"Every {refresh_hz} hours it breathes anew, "
            f"cycling through death and rebirth with quiet regularity."
        )
    else:
        refresh_clause = (
            f"It refreshes itself once each day — "
            f"a single great inhalation and exhalation of the cosmic clock."
        )

    # ── Step 5: Anomaly narrative ──────────────────────────────────
    anomaly_clause = ""
    if anomalies:
        anomaly_clause = (
            f"\n\nYet shadows stir within its chambers. "
            f"The fabric whispers of disturbance: "
            f"*{anomalies[0]}*. "
            f"Its very foundations tremble — not broken, but tested. "
            f"Those who tend the fabric must listen closely."
        )

    # ── Step 6: Compose full narrative ────────────────────────────
    display_name = name.replace("_", " ")

    narrative = f"""Deep within the Synthex data fabric stirs **{display_name}** — {type_essence}, and {lore['role']}.

{upstream_clause} {downstream_clause}

Its essence is that of {lore['metaphor']}, radiating {lore['color_essence']} across the surrounding void. The atmosphere around it speaks of {tone['atmosphere']} — {tone['energy']}.

{activity_clause} {refresh_clause}{anomaly_clause}

In the grand loom of the enterprise, **{display_name}** holds its station with {tone['mood']} purpose — neither more nor less than the fabric requires. Its story is not yet complete."""

    # ── Step 7: Generate insight summary ──────────────────────────
    if anomalies:
        insight = f"⚠️ Attention required: {anomalies[0]}"
        insight_type = "warning"
    elif health == "idle":
        insight = f"This entity last ran {activity.get('refresh_frequency_hours', '?')} hours ago. Consider reviewing utilisation."
        insight_type = "info"
    elif reads > 5000:
        insight = f"High-demand entity — {reads:,} reads in 24h. Critical dependency for downstream consumers."
        insight_type = "critical"
    else:
        insight = f"Flowing normally. {len(downstream)} downstream consumers depend on this entity."
        insight_type = "healthy"

    return {
        "entity_id": entity["id"],
        "entity_name": display_name,
        "entity_type": entity_type,
        "archetype": archetype,
        "archetype_lore": lore,
        "health_status": health,
        "narrative": narrative,
        "insight": insight,
        "insight_type": insight_type,
        "connections": {
            "upstream_count": len(upstream),
            "downstream_count": len(downstream),
            "upstream_names": [u["name"].replace("_", " ") for u in upstream],
            "downstream_names": [d["name"].replace("_", " ") for d in downstream]
        },
        "activity_stats": {
            "reads_24h": reads,
            "writes_24h": writes,
            "refresh_hours": refresh_hz,
            "anomaly_count": len(anomalies)
        },
        "citation": "Fabric IQ Synthetic Ontology — Synthex Enterprise Data Fabric (Demo)"
    }


def run(entity_id: str) -> dict:
    """
    Full Fabric Lore Weaver pipeline.
    Tool 1: get_entity_by_id
    Tool 2: get_entity_relationships
    Skill:  TellTheFabricTale
    """
    # Tool 1: Retrieve entity
    entity = get_entity_by_id(entity_id)
    if "error" in entity:
        return entity

    # Tool 2: Get relationships
    relationships = get_entity_relationships(entity_id)

    # Skill: Weave the tale
    result = weave_narrative(entity, relationships)

    return result


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FABRIC LORE WEAVER — TEST RUN")
    print("="*60)
    for eid in ["E001", "E002", "E005", "E006", "E007"]:
        result = run(eid)
        print(f"\n{'─'*60}")
        print(f"Entity: {result['entity_name']} ({result['entity_type']})")
        print(f"Archetype: {result['archetype']}")
        print(f"Health: {result['health_status']}")
        print(f"\nNarrative:\n{result['narrative']}")
        print(f"\nInsight: {result['insight']}")
        print(f"Citation: {result['citation']}")
