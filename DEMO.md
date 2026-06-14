# ✦ Aether Weaver — Judge Demo Guide

> **Microsoft Agents League 2026 · Creative Apps Track**
> Estimated demo time: **3 minutes**

This guide walks judges through both surfaces — the **Streamlit cosmic canvas** and the **MCP server inside VS Code Copilot**.

---

## ⚡ 60-Second Quick Start

```bash
git clone https://github.com/nikhil0912/aetherweaver
cd aetherweaver
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` — you'll see the cosmic dark canvas with 7 interconnected Fabric IQ nodes glowing in distinct colors.

---

## 🎬 Demo Path 1 — The Cosmic Canvas

| Step | Action | What to look for |
|---|---|---|
| 1 | App loads | 7 nodes float in cosmic dark space — gold Lakehouse center, emerald Dataflow, violet Semantic Model, amber Warehouse, cyan Event Stream |
| 2 | Click **✦ Weave** on **Sales Transactions Lakehouse (E001)** | The Lore Scroll panel awakens with a poetic narrative |
| 3 | Read the narrative aloud | *"Deep within the Synthex data fabric stirs Sales Transactions Lakehouse — a great hall where structured and unstructured truths coexist..."* |
| 4 | Notice connections, stats, citation | All grounded in Fabric IQ ontology |
| 5 | Click **Customer 360 Warehouse (E005)** | Notice **warning amber** pulsing — narrative tone shifts to shadow language |
| 6 | Read the anomaly clause | *"Yet shadows stir within its chambers. The fabric whispers of disturbance: Schema drift detected..."* |
| 7 | Click **Inventory Event Stream (E007)** | 72M reads/24h — "eternal pulse" narrative |

**What judges should notice:**
- Without a single label, node colour + pulse rate + edge density communicate fabric health
- Every narrative is grounded — `Citation: Fabric IQ Synthetic Ontology`
- Warning entities visibly change the narrative tone
- 6-step `TellTheFabricTale` pipeline traceable in `agents/lore_weaver.py`

---

## 🎬 Demo Path 2 — MCP Server in VS Code Copilot

This is the **second surface** — judges can use the Fabric Lore Weaver directly inside GitHub Copilot Agent Mode in VS Code.

### Setup (one-time, 30 seconds)

1. Open the cloned repo in VS Code
2. The `.vscode/mcp.json` file is already configured
3. Open Copilot Chat → switch to **Agent Mode** (dropdown in chat panel)
4. The `aether-weaver` MCP server connects automatically

### Try These Prompts

| Prompt to type in Copilot Chat | What happens |
|---|---|
| *"List all entities in the Fabric IQ data fabric"* | Copilot calls `list_fabric_entities` → renders table of all 7 nodes |
| *"Get the lore of E001"* | Copilot calls `get_entity_lore` → returns full poetic narrative inside the editor |
| *"What is the overall health of the fabric?"* | Copilot calls `get_fabric_health` → health report with warnings |
| *"Show me the lineage for E005"* | Copilot calls `get_entity_lineage` → upstream/downstream map |
| *"Compare E001 and E005"* | Copilot calls `compare_entities` → side-by-side contrast narrative |

**What judges should notice:**
- 5 MCP tools matching the previous Creative Apps winner pattern
- Works inside the editor — judges never leave VS Code
- All tools return formatted Markdown rendered in Copilot's response
- All outputs cited to `Fabric IQ Synthetic Ontology`

---

## 🧪 Run the Evaluation Suite

```bash
python eval.py
```

**Expected output:** `78/78 tests passing, 100% score`

Tests cover: data integrity, narrative quality, MCP tools, responsible AI, visual logic, edge cases.

---

## 🎨 The Visual Language — No Words Needed

| Visual cue | Meaning |
|---|---|
| **Gold pulse** | Healthy Lakehouse / high activity |
| **Emerald flow** | Healthy Dataflow / Transformer |
| **Violet glow** | Semantic Model / Oracle archetype |
| **Amber dashed ring** | WARNING — anomalies present |
| **Cool blue pulse** | IDLE — dormant entity |
| **Cyan particles** | Event Stream / extreme throughput |
| **Thick edges** | High data throughput |
| **Particle density** | Flow activity intensity |

---

## ⬡ Fabric IQ Integration

Fabric IQ is the **creative nucleus** — not an add-on:

| Fabric IQ capability | How Aether Weaver uses it |
|---|---|
| **Ontology** | Entity types, archetypes, business meaning → narrative identity |
| **Data lineage** | Upstream/downstream dependencies → visual edges + narrative lineage |
| **Semantic models** | Business relationships → grounded narrative generation |
| **Real-time events** | Activity signals, anomalies, refresh rates → visual pulse + narrative tone |

---

## ◈ GitHub Copilot Usage

Every layer was built with Copilot. See **`copilot_usage.md`** for the exact prompts used to generate:
- The SVG canvas engine
- The 6-step TellTheFabricTale narrative pipeline
- The cosmic dark CSS design system
- The Fabric IQ synthetic ontology schema
- The 78-test evaluation suite
- All 5 MCP tools

---

## 🏛️ Architecture at a Glance

```
                ┌─ Entry 1: Streamlit Web App ─┐
User selects ──▶│                              │──▶ Lore Scroll Panel
node             │   Fabric Lore Weaver Agent  │    (narrative + insight)
                ├─ Entry 2: VS Code MCP ──────┤
Copilot prompt ─▶│                            │──▶ Copilot Chat
                 │  TellTheFabricTale Skill   │    (5 MCP tools)
                 │                            │
                 │  Tool 1: get_entity_by_id  │
                 │  Tool 2: get_relationships │
                 │  6-step weaving pipeline   │
                 └────────────────────────────┘
                              ↓
                  ⬡ Microsoft Fabric IQ ⬡
                 (synthetic ontology, lineage,
                  semantic models, events)
```

Open `architecture.html` in a browser for the full visual diagram.

---

## 🔒 Responsible AI

- **All data is synthetic** — `data/fabric_ontology.json`, no real entities
- **All narratives cited** — explicit `Fabric IQ Synthetic Ontology` reference
- **No clinical, financial, or consequential decisions** ever
- **No PII** in any output
- **Anomalies are surfaced, not hidden** — warning entity narratives explicitly mention disturbances

---

## 📂 Repo Structure

```
aetherweaver/
├── app.py                      # Streamlit cosmic canvas + Lore Scroll
├── mcp_server.py               # 5 MCP tools for VS Code Copilot
├── eval.py                     # 78-test evaluation suite
├── copilot_usage.md            # GitHub Copilot documentation
├── architecture.html           # Full architecture diagram
├── .streamlit/
│   └── config.toml             # Dark theme enforcement
├── .vscode/
│   └── mcp.json                # MCP server configuration
├── agents/
│   ├── __init__.py
│   └── lore_weaver.py          # Fabric Lore Weaver + TellTheFabricTale
└── data/
    └── fabric_ontology.json    # Fabric IQ synthetic ontology
```

---

## 🌟 What Makes Aether Weaver Different

Every other Creative Apps submission will be a chatbot, an image generator, or a code helper. **Aether Weaver shows what enterprise data actually feels like** — the heartbeat of a Lakehouse, the warning glow of an anomalous warehouse, the eternal pulse of an event stream.

Data professionals spend their entire careers inside Fabric. They've never felt it before. Aether Weaver makes the invisible visible.

---

*All data is synthetic. Built entirely with GitHub Copilot for the Agents League 2026 hackathon.*
