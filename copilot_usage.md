# ◈ GitHub Copilot Usage Documentation

> **Microsoft Agents League 2026 — Creative Apps Track**
> This document evidences how GitHub Copilot was used throughout
> the development of Aether Weaver, as required by the challenge.

---

## How Copilot Was Used

### 1. SVG Canvas Engine (`app.py` — `build_fabric_svg`)

The entire SVG node graph rendering engine was built with Copilot assistance.

**Prompt used:**
```
Generate a Python function that builds an SVG string rendering 
a network graph of data entities. Each entity should be a 
glowing circular node with outer glow ring, inner body, core dot, 
and text label. Nodes should be connected by quadratic bezier 
curves with particle dots along each path. Use radialGradient 
and filter elements in the SVG defs section. Accept a selected_id 
parameter to highlight one node with stronger glow effects.
```

**Copilot generated:** The complete `build_fabric_svg` function including:
- `<defs>` section with radialGradient, linearGradient, and feGaussianBlur filter elements
- Bezier curve control point calculation: `mx = (x1 + x2) / 2`, `my = (y1 + y2) / 2 - 40`
- Particle dot interpolation along bezier path using quadratic formula
- Node ring layering (outer glow → mid ring → inner body → core)
- Selected node highlight logic with stronger glow and outer arc

---

### 2. Fabric Lore Weaver Agent (`agents/lore_weaver.py`)

The multi-step narrative pipeline was scaffolded with Copilot.

**Prompt used:**
```
Create a Python function called weave_narrative that takes an entity 
dict and a relationships dict. It should run a multi-step pipeline:
Step 1 - resolve archetype and health tone from lookup dicts
Step 2 - build upstream clause using entity names
Step 3 - build downstream clause  
Step 4 - generate activity narrative based on read counts and 
         refresh frequency
Step 5 - add anomaly clause if anomalies exist
Step 6 - compose full narrative as an f-string
Step 7 - generate insight summary with insight_type field
Return a dict with narrative, insight, insight_type, connections, 
activity_stats, and citation fields.
```

**Copilot generated:** The complete step-by-step pipeline structure, the activity threshold logic (`reads > 10000`, `reads > 1000`), refresh frequency branching, and the insight classification logic.

---

### 3. Cosmic Dark CSS Theme (`app.py` — CSS block)

The full design system was generated with Copilot.

**Prompt used:**
```
Generate a CSS block for a Streamlit app with a cosmic dark theme.
Use a radial gradient background from deep navy to pure black.
Include styles for: a hero header with gradient text, badge pills 
in four color variants, a node card grid with hover effects and 
colored top border accents, a lore panel with subtle border glow,
activity stat cards, insight boxes in four health-status colors
(healthy/warning/critical/info), and custom scrollbar styling.
Use CSS variables and rgba colors throughout. Font stack: 
Cinzel for display, Crimson Pro for narrative, Inter for UI.
```

**Copilot generated:** The complete 400-line CSS block including all component styles, the radial gradient background, hover transitions, and the four insight color variants.

---

### 4. Fabric IQ Ontology Schema (`data/fabric_ontology.json`)

The synthetic data structure was designed with Copilot.

**Prompt used:**
```
Design a JSON schema for a synthetic Microsoft Fabric IQ ontology.
Include 7 entities of types: Lakehouse, Dataflow, Semantic Model,
Power BI Report, Data Warehouse, ML Model, Event Stream.
Each entity needs: id, name, type, archetype, description, owner,
upstream array, downstream array, activity object (with refresh_
frequency_hours, reads_last_24h, writes_last_24h, health_status,
last_refresh, anomalies), x and y canvas coordinates.
Include a relationships array with from, to, type, throughput fields.
Make the data bidirectionally consistent. Include one warning entity
with anomalies and one idle entity.
```

**Copilot generated:** The complete ontology structure. Manual review confirmed bidirectional consistency and added the E007→E001 upstream relationship.

---

### 5. Evaluation Suite (`eval.py`)

The 78-test evaluation suite was built with Copilot.

**Prompt used:**
```
Generate a Python test suite for a data fabric narrative agent.
Tests should cover: JSON data integrity, entity retrieval tool,
relationship retrieval tool, narrative quality (length, citations,
no underscore names), health tone accuracy (warning/idle/healthy),
full pipeline completeness, responsible AI checks (no PII, all cited),
and visual helper functions (node colors, icons, number formatting,
SVG generation). Use a simple pass/fail pattern printing results.
```

**Copilot generated:** The complete test structure, all assertion patterns, and the summary statistics block.

---

### 6. Debugging Assistance

Throughout development, Copilot Chat was used to:
- Identify the `"the the"` double-article bug in the anomaly clause
- Fix the bidirectional upstream/downstream inconsistency in the ontology
- Resolve the `**bold**` → `<strong>` markdown-to-HTML conversion issue
- Remove unused imports (`os`, `time`, `math`, `get_entity_by_id`)
- Fix the orphaned `<div>` in the connections section

---

## Summary

| Component | Copilot Role |
|---|---|
| SVG canvas engine | Full generation from prompt |
| Lore Weaver pipeline | Scaffolding + step structure |
| CSS design system | Full generation from prompt |
| Ontology schema | Full generation + manual review |
| Evaluation suite | Full generation from prompt |
| Bug fixes | Copilot Chat debugging assistance |

> GitHub Copilot was integral to every layer of this project —
> from initial architecture to final bug fixes.
> Development time was reduced by an estimated 60–70%.
