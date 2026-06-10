"""
Aether Weaver — The Pulse of Your Data Fabric, Manifested
===========================================================
Microsoft Agents League 2026 · Creative Apps Track
Built entirely with GitHub Copilot

Transforms Microsoft Fabric IQ semantic ontology, data lineage,
and real-time events into living generative art and poetic narratives
through the Fabric Lore Weaver AI agent.
"""

import streamlit as st
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.lore_weaver import run as weave_lore

DATA_DIR = Path(__file__).parent / "data"

# ── Page Config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aether Weaver",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Global CSS — Cosmic Dark Theme ────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&family=Crimson+Pro:ital,wght@0,300;0,400;1,300;1,400&display=swap');

  /* ── Reset & Base ── */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
  }

  .stApp {
    background: radial-gradient(ellipse at 20% 20%, #0d1b3e 0%, #060810 40%, #000000 100%);
    min-height: 100vh;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  .stDeployButton { display: none; }

  /* ── Hero Header ── */
  .aw-hero {
    background: linear-gradient(180deg, rgba(13,27,62,0.9) 0%, rgba(6,8,16,0) 100%);
    padding: 32px 48px 20px;
    border-bottom: 1px solid rgba(99,102,241,0.15);
    position: relative;
    overflow: hidden;
  }
  .aw-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -10%;
    width: 120%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(99,102,241,0.06) 0%, transparent 70%);
    pointer-events: none;
  }
  .aw-title {
    font-family: 'Cinzel', serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #c7d2fe 0%, #818cf8 40%, #6366f1 70%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: 0.05em;
  }
  .aw-subtitle {
    font-family: 'Crimson Pro', serif;
    font-size: 1.1rem;
    color: #94a3b8;
    font-style: italic;
    margin: 6px 0 0 0;
    letter-spacing: 0.02em;
  }
  .aw-badges {
    display: flex;
    gap: 10px;
    margin-top: 14px;
    flex-wrap: wrap;
  }
  .aw-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .badge-fabric {
    background: rgba(139,92,246,0.15);
    border: 1px solid rgba(139,92,246,0.4);
    color: #a78bfa;
  }
  .badge-copilot {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.3);
    color: #4ade80;
  }
  .badge-creative {
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.3);
    color: #fbbf24;
  }
  .badge-iq {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.35);
    color: #818cf8;
  }

  /* ── Canvas Container ── */
  .canvas-container {
    background: rgba(6,8,16,0.6);
    border: 1px solid rgba(99,102,241,0.12);
    border-radius: 16px;
    margin: 0 24px;
    overflow: hidden;
    position: relative;
  }
  .canvas-label {
    font-family: 'Cinzel', serif;
    font-size: 10px;
    letter-spacing: 0.15em;
    color: #475569;
    text-transform: uppercase;
    padding: 12px 20px 8px;
    border-bottom: 1px solid rgba(99,102,241,0.08);
  }

  /* ── Node Selection Grid ── */
  .node-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
    padding: 20px 24px;
  }
  .node-card {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 12px;
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
  }
  .node-card:hover {
    border-color: rgba(99,102,241,0.5);
    background: rgba(15,23,42,0.95);
    transform: translateY(-2px);
  }
  .node-card.selected {
    border-color: rgba(165,180,252,0.6);
    background: rgba(30,41,74,0.9);
    box-shadow: 0 0 20px rgba(99,102,241,0.15);
  }
  .node-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--node-color, #6366f1);
    opacity: 0.6;
  }
  .node-icon {
    font-size: 1.4rem;
    margin-bottom: 6px;
    display: block;
  }
  .node-name {
    font-size: 12px;
    font-weight: 600;
    color: #e2e8f0;
    line-height: 1.3;
    margin-bottom: 4px;
    word-break: break-word;
  }
  .node-type {
    font-size: 10px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .node-health {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-right: 5px;
    vertical-align: middle;
  }

  /* ── Lore Panel ── */
  .lore-panel {
    background: rgba(8,12,28,0.95);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 28px 32px;
    margin: 0 0 0 0;
    position: relative;
    overflow: hidden;
  }
  .lore-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at top left, rgba(99,102,241,0.05) 0%, transparent 60%);
    pointer-events: none;
  }
  .lore-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(99,102,241,0.12);
  }
  .lore-archetype-badge {
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .lore-scroll-title {
    font-family: 'Cinzel', serif;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: #475569;
    text-transform: uppercase;
    margin-bottom: 16px;
  }
  .lore-narrative {
    font-family: 'Crimson Pro', serif;
    font-size: 1.15rem;
    line-height: 1.85;
    color: #cbd5e1;
    font-weight: 300;
  }
  .lore-narrative em {
    color: #a78bfa;
    font-style: italic;
  }
  .lore-narrative strong {
    color: #e2e8f0;
    font-weight: 600;
  }
  .lore-citation {
    margin-top: 20px;
    padding-top: 14px;
    border-top: 1px solid rgba(99,102,241,0.1);
    font-size: 11px;
    color: #475569;
    font-style: italic;
  }

  /* ── Stats Row ── */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
  }
  .stat-card {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(99,102,241,0.12);
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
  }
  .stat-value {
    font-family: 'Cinzel', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #c7d2fe;
    line-height: 1;
    margin-bottom: 4px;
  }
  .stat-label {
    font-size: 10px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  /* ── Insight Box ── */
  .insight-healthy {
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #86efac;
    margin-top: 16px;
  }
  .insight-warning {
    background: rgba(251,191,36,0.08);
    border: 1px solid rgba(251,191,36,0.25);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #fde68a;
    margin-top: 16px;
  }
  .insight-critical {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #a5b4fc;
    margin-top: 16px;
  }
  .insight-info {
    background: rgba(148,163,184,0.08);
    border: 1px solid rgba(148,163,184,0.2);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #94a3b8;
    margin-top: 16px;
  }

  /* ── Connections Panel ── */
  .connections-row {
    display: flex;
    gap: 12px;
    margin-top: 20px;
  }
  .connection-group {
    flex: 1;
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(99,102,241,0.1);
    border-radius: 10px;
    padding: 14px 16px;
  }
  .connection-label {
    font-size: 10px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
  }
  .connection-item {
    font-size: 12px;
    color: #94a3b8;
    padding: 4px 0;
    border-bottom: 1px solid rgba(99,102,241,0.06);
  }
  .connection-item:last-child { border-bottom: none; }

  /* ── Fabric Canvas SVG ── */
  .fabric-canvas {
    width: 100%;
    background: transparent;
    display: block;
  }

  /* ── Welcome State ── */
  .welcome-state {
    text-align: center;
    padding: 60px 40px;
    color: #475569;
  }
  .welcome-glyph {
    font-size: 3.5rem;
    margin-bottom: 16px;
    opacity: 0.4;
  }
  .welcome-text {
    font-family: 'Crimson Pro', serif;
    font-size: 1.1rem;
    font-style: italic;
    color: #475569;
    max-width: 320px;
    margin: 0 auto;
    line-height: 1.7;
  }

  /* ── Section Dividers ── */
  .section-rule {
    border: none;
    border-top: 1px solid rgba(99,102,241,0.1);
    margin: 24px 0;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ── Load Ontology ──────────────────────────────────────────────────
@st.cache_data
def load_ontology():
    with open(DATA_DIR / "fabric_ontology.json") as f:
        return json.load(f)


ontology = load_ontology()
entities = ontology["entities"]
relationships = ontology["relationships"]


# ── Helper Functions ───────────────────────────────────────────────
def get_node_color(entity_type: str, health: str) -> str:
    if health == "warning":
        return "#f59e0b"
    if health == "idle":
        return "#3b82f6"
    if health == "error":
        return "#ef4444"
    colors = {
        "Lakehouse": "#f59e0b",
        "Dataflow": "#10b981",
        "Semantic Model": "#8b5cf6",
        "Power BI Report": "#e2e8f0",
        "Data Warehouse": "#f59e0b",
        "ML Model": "#6366f1",
        "Event Stream": "#06b6d4"
    }
    return colors.get(entity_type, "#6366f1")


def get_node_icon(entity_type: str) -> str:
    icons = {
        "Lakehouse": "🏛️",
        "Dataflow": "🌊",
        "Semantic Model": "🔮",
        "Power BI Report": "📊",
        "Data Warehouse": "🏰",
        "ML Model": "🧠",
        "Event Stream": "⚡"
    }
    return icons.get(entity_type, "✦")


def get_health_color(health: str) -> str:
    return {
        "healthy": "#22c55e",
        "warning": "#f59e0b",
        "idle": "#3b82f6",
        "error": "#ef4444"
    }.get(health, "#6366f1")


def format_number(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


# ── Build SVG Canvas ──────────────────────────────────────────────
def build_fabric_svg(selected_id: str = None) -> str:
    W, H = 1100, 420
    entity_map = {e["id"]: e for e in entities}

    svg_parts = [
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:100%;background:transparent;">',
        '<defs>',
    ]

    # Gradients and filters
    svg_parts.append('''
      <radialGradient id="bgGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" style="stop-color:#0d1b3e;stop-opacity:0.3"/>
        <stop offset="100%" style="stop-color:#000;stop-opacity:0"/>
      </radialGradient>
      <filter id="glow">
        <feGaussianBlur stdDeviation="4" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <filter id="glow-strong">
        <feGaussianBlur stdDeviation="8" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <filter id="glow-soft">
        <feGaussianBlur stdDeviation="2" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
    ''')

    # Animated gradients for edges
    for i, rel in enumerate(relationships):
        from_e = entity_map.get(rel["from"])
        to_e = entity_map.get(rel["to"])
        if not from_e or not to_e:
            continue
        color = get_node_color(from_e["type"], from_e["activity"]["health_status"])
        svg_parts.append(
            f'<linearGradient id="edgeGrad{i}" x1="0%" y1="0%" x2="100%" y2="0%">'
            f'<stop offset="0%" style="stop-color:{color};stop-opacity:0.1"/>'
            f'<stop offset="50%" style="stop-color:{color};stop-opacity:0.6"/>'
            f'<stop offset="100%" style="stop-color:{color};stop-opacity:0.1"/>'
            f'</linearGradient>'
        )

    # Node gradients
    for e in entities:
        color = get_node_color(e["type"], e["activity"]["health_status"])
        eid = e["id"]
        svg_parts.append(
            f'<radialGradient id="nodeGrad{eid}" cx="50%" cy="50%" r="50%">'
            f'<stop offset="0%" style="stop-color:{color};stop-opacity:0.4"/>'
            f'<stop offset="100%" style="stop-color:{color};stop-opacity:0.05"/>'
            f'</radialGradient>'
        )

    svg_parts.append('</defs>')

    # Background ambient glow
    svg_parts.append(
        f'<ellipse cx="{W//2}" cy="{H//2}" rx="{W//2}" ry="{H//2}" '
        f'fill="url(#bgGlow)"/>'
    )

    # Draw edges first
    for i, rel in enumerate(relationships):
        from_e = entity_map.get(rel["from"])
        to_e = entity_map.get(rel["to"])
        if not from_e or not to_e:
            continue

        x1, y1 = from_e["x"], from_e["y"]
        x2, y2 = to_e["x"], to_e["y"]

        # Bezier control point
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 40

        health = from_e["activity"]["health_status"]
        color = get_node_color(from_e["type"], health)
        is_selected_edge = selected_id in [from_e["id"], to_e["id"]]

        opacity = "0.7" if is_selected_edge else "0.3"
        stroke_w = "2.5" if is_selected_edge else "1.5"
        dash = ""
        if health == "warning":
            dash = 'stroke-dasharray="6,4"'

        throughput = rel.get("throughput", "medium")
        particle_r = {"extreme": 3, "high": 2.5, "medium": 2, "low": 1.5}.get(throughput, 2)

        svg_parts.append(
            f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" '
            f'fill="none" stroke="url(#edgeGrad{i})" '
            f'stroke-width="{stroke_w}" opacity="{opacity}" '
            f'{dash}/>'
        )

        # Particle dots along path (static approximation)
        for t in [0.25, 0.5, 0.75]:
            px = (1-t)**2*x1 + 2*(1-t)*t*mx + t**2*x2
            py = (1-t)**2*y1 + 2*(1-t)*t*my + t**2*y2
            p_opacity = "0.8" if is_selected_edge else "0.4"
            svg_parts.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{particle_r}" '
                f'fill="{color}" opacity="{p_opacity}" '
                f'filter="url(#glow-soft)"/>'
            )

    # Draw nodes
    for e in entities:
        x, y = e["x"], e["y"]
        eid = e["id"]
        color = get_node_color(e["type"], e["activity"]["health_status"])
        health = e["activity"]["health_status"]
        is_selected = (eid == selected_id)

        r_outer = 42 if is_selected else 36
        r_inner = 22 if is_selected else 18
        r_core = 9 if is_selected else 7

        # Outer glow ring
        glow_filter = "url(#glow-strong)" if is_selected else "url(#glow)"
        ring_opacity = "0.35" if is_selected else "0.15"
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r_outer}" '
            f'fill="url(#nodeGrad{eid})" opacity="{ring_opacity}" '
            f'filter="{glow_filter}"/>'
        )

        # Mid ring
        mid_opacity = "0.5" if is_selected else "0.25"
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r_inner}" '
            f'fill="none" stroke="{color}" stroke-width="1" '
            f'opacity="{mid_opacity}"/>'
        )

        # Inner body
        body_opacity = "0.85" if is_selected else "0.7"
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r_inner}" '
            f'fill="rgba(6,8,16,0.8)" stroke="{color}" '
            f'stroke-width="{2.5 if is_selected else 1.5}" '
            f'opacity="{body_opacity}" filter="{glow_filter}"/>'
        )

        # Core dot
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r_core}" '
            f'fill="{color}" opacity="0.9" filter="url(#glow)"/>'
        )

        # Health indicator pulse ring (for warning/error)
        if health == "warning":
            svg_parts.append(
                f'<circle cx="{x}" cy="{y}" r="{r_outer + 6}" '
                f'fill="none" stroke="#f59e0b" stroke-width="1.5" '
                f'opacity="0.3" stroke-dasharray="4,4"/>'
            )
        elif health == "idle":
            svg_parts.append(
                f'<circle cx="{x}" cy="{y}" r="{r_outer + 4}" '
                f'fill="none" stroke="#3b82f6" stroke-width="1" '
                f'opacity="0.2"/>'
            )

        # Entity type icon (text)
        icon = get_node_icon(e["type"])
        svg_parts.append(
            f'<text x="{x}" y="{y - r_inner - 12}" '
            f'text-anchor="middle" font-size="13" opacity="0.7">{icon}</text>'
        )

        # Entity name label
        display_name = e["name"].replace("_", " ")
        words = display_name.split()
        if len(words) > 2:
            line1 = " ".join(words[:2])
            line2 = " ".join(words[2:])
            svg_parts.append(
                f'<text x="{x}" y="{y + r_inner + 18}" '
                f'text-anchor="middle" font-size="9.5" '
                f'font-family="Inter, sans-serif" font-weight="500" '
                f'fill="{color}" opacity="0.85">{line1}</text>'
            )
            svg_parts.append(
                f'<text x="{x}" y="{y + r_inner + 30}" '
                f'text-anchor="middle" font-size="9.5" '
                f'font-family="Inter, sans-serif" font-weight="500" '
                f'fill="{color}" opacity="0.85">{line2}</text>'
            )
        else:
            svg_parts.append(
                f'<text x="{x}" y="{y + r_inner + 18}" '
                f'text-anchor="middle" font-size="9.5" '
                f'font-family="Inter, sans-serif" font-weight="500" '
                f'fill="{color}" opacity="0.85">{display_name}</text>'
            )

        # Selected indicator arc
        if is_selected:
            svg_parts.append(
                f'<circle cx="{x}" cy="{y}" r="{r_outer + 10}" '
                f'fill="none" stroke="{color}" stroke-width="2" '
                f'opacity="0.5" filter="url(#glow-soft)"/>'
            )

    svg_parts.append('</svg>')
    return "".join(svg_parts)


# ── Session State ──────────────────────────────────────────────────
if "selected_entity" not in st.session_state:
    st.session_state.selected_entity = None
if "lore_result" not in st.session_state:
    st.session_state.lore_result = None


# ── HERO HEADER ────────────────────────────────────────────────────
st.markdown("""
<div class="aw-hero">
  <h1 class="aw-title">✦ Aether Weaver</h1>
  <p class="aw-subtitle">The Pulse of Your Data Fabric, Manifested</p>
  <div class="aw-badges">
    <span class="aw-badge badge-fabric">⬡ Fabric IQ</span>
    <span class="aw-badge badge-copilot">◈ GitHub Copilot</span>
    <span class="aw-badge badge-iq">✦ Microsoft IQ</span>
    <span class="aw-badge badge-creative">◆ Creative Apps Track</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── MAIN LAYOUT ────────────────────────────────────────────────────
col_canvas, col_lore = st.columns([3, 2], gap="medium")

with col_canvas:
    # ── Fabric Canvas ──────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 0 12px;">
      <div style="font-family:'Cinzel',serif; font-size:10px;
           letter-spacing:0.15em; color:#475569; text-transform:uppercase;
           margin-bottom:12px;">
        ✦ Fabric IQ — Synthex Enterprise Data Fabric
      </div>
    </div>
    """, unsafe_allow_html=True)

    # SVG Canvas
    svg = build_fabric_svg(st.session_state.selected_entity)
    st.markdown(
        f'<div style="border:1px solid rgba(99,102,241,0.12); '
        f'border-radius:14px; overflow:hidden; '
        f'background:rgba(6,8,16,0.4); margin:0 12px;">'
        f'{svg}</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Node Selection Grid ────────────────────────────────────────
    st.markdown("""
    <div style="padding: 0 12px;">
      <div style="font-family:'Cinzel',serif; font-size:10px;
           letter-spacing:0.15em; color:#475569; text-transform:uppercase;
           margin-bottom:12px;">
        ✦ Select a Node — Awaken the Lore Weaver
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Build node grid using columns
    cols = st.columns(4, gap="small")
    for i, entity in enumerate(entities):
        col = cols[i % 4]
        with col:
            health = entity["activity"]["health_status"]
            color = get_node_color(entity["type"], health)
            health_color = get_health_color(health)
            icon = get_node_icon(entity["type"])
            is_selected = st.session_state.selected_entity == entity["id"]
            display_name = entity["name"].replace("_", " ")

            border_style = (
                f"border: 1.5px solid {color}60"
                if is_selected
                else "border: 1px solid rgba(99,102,241,0.15)"
            )
            bg_style = (
                f"background: rgba(15,23,42,0.95)"
                if is_selected
                else "background: rgba(15,23,42,0.6)"
            )

            st.markdown(
                f'<div style="{bg_style}; {border_style}; '
                f'border-radius:10px; padding:10px 12px; '
                f'margin-bottom:4px; '
                f'border-top: 2px solid {color}80;">'
                f'<div style="font-size:1.1rem; margin-bottom:4px;">{icon}</div>'
                f'<div style="font-size:11px; font-weight:600; '
                f'color:#e2e8f0; line-height:1.3; margin-bottom:3px;">'
                f'{display_name[:22]}{"..." if len(display_name) > 22 else ""}</div>'
                f'<div style="font-size:9px; color:#64748b; '
                f'text-transform:uppercase; letter-spacing:0.06em;">'
                f'<span style="display:inline-block; width:5px; height:5px; '
                f'border-radius:50%; background:{health_color}; '
                f'margin-right:4px; vertical-align:middle;"></span>'
                f'{entity["type"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "✦ Weave" if not is_selected else "✦ Active",
                key=f"node_{entity['id']}",
                use_container_width=True
            ):
                st.session_state.selected_entity = entity["id"]
                with st.spinner("The Lore Weaver awakens..."):
                    st.session_state.lore_result = weave_lore(entity["id"])
                st.rerun()

    # ── Fabric Stats Bar ──────────────────────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    total_reads = sum(e["activity"]["reads_last_24h"] for e in entities)
    healthy_count = sum(
        1 for e in entities if e["activity"]["health_status"] == "healthy"
    )
    warning_count = sum(
        1 for e in entities if e["activity"]["health_status"] == "warning"
    )

    st.markdown(f"""
    <div style="display:grid; grid-template-columns:repeat(4,1fr);
         gap:10px; padding:0 12px; margin-bottom:8px;">
      <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(99,102,241,0.12);
           border-radius:10px;padding:12px 14px;text-align:center;">
        <div style="font-family:'Cinzel',serif;font-size:1.3rem;
             color:#c7d2fe;font-weight:600;">{len(entities)}</div>
        <div style="font-size:9px;color:#475569;text-transform:uppercase;
             letter-spacing:0.08em;margin-top:2px;">Entities</div>
      </div>
      <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(99,102,241,0.12);
           border-radius:10px;padding:12px 14px;text-align:center;">
        <div style="font-family:'Cinzel',serif;font-size:1.3rem;
             color:#86efac;font-weight:600;">{healthy_count}</div>
        <div style="font-size:9px;color:#475569;text-transform:uppercase;
             letter-spacing:0.08em;margin-top:2px;">Healthy</div>
      </div>
      <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(99,102,241,0.12);
           border-radius:10px;padding:12px 14px;text-align:center;">
        <div style="font-family:'Cinzel',serif;font-size:1.3rem;
             color:#fbbf24;font-weight:600;">{warning_count}</div>
        <div style="font-size:9px;color:#475569;text-transform:uppercase;
             letter-spacing:0.08em;margin-top:2px;">Warnings</div>
      </div>
      <div style="background:rgba(15,23,42,0.6);border:1px solid rgba(99,102,241,0.12);
           border-radius:10px;padding:12px 14px;text-align:center;">
        <div style="font-family:'Cinzel',serif;font-size:1.3rem;
             color:#a5b4fc;font-weight:600;">{format_number(total_reads)}</div>
        <div style="font-size:9px;color:#475569;text-transform:uppercase;
             letter-spacing:0.08em;margin-top:2px;">Reads/24h</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── LORE PANEL ─────────────────────────────────────────────────────
with col_lore:
    st.markdown("""
    <div style="padding: 0 8px 0 0;">
      <div style="font-family:'Cinzel',serif; font-size:10px;
           letter-spacing:0.15em; color:#475569; text-transform:uppercase;
           margin-bottom:12px;">
        ✦ The Lore Scroll
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.lore_result is None:
        st.markdown("""
        <div style="background:rgba(8,12,28,0.8);
             border:1px solid rgba(99,102,241,0.15);
             border-radius:14px; padding:48px 32px; text-align:center;
             margin-right:8px;">
          <div style="font-size:3rem; margin-bottom:16px; opacity:0.3;">✦</div>
          <p style="font-family:'Crimson Pro',serif; font-size:1.05rem;
               font-style:italic; color:#475569; line-height:1.8;
               max-width:280px; margin:0 auto;">
            Select a node in the fabric canvas to awaken the Lore Weaver.
            Each entity holds a story waiting to be told.
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        r = st.session_state.lore_result
        color = get_node_color(r["entity_type"], r["health_status"])
        health_color = get_health_color(r["health_status"])
        icon = get_node_icon(r["entity_type"])

        # ── Entity Header ──────────────────────────────────────────
        st.markdown(
            f'<div style="background:rgba(8,12,28,0.9);'
            f'border:1px solid {color}30;'
            f'border-top:2px solid {color}80;'
            f'border-radius:14px; padding:22px 24px;'
            f'margin-right:8px; margin-bottom:12px;">'

            # Header row
            f'<div style="display:flex;align-items:center;gap:12px;'
            f'margin-bottom:16px;padding-bottom:14px;'
            f'border-bottom:1px solid rgba(99,102,241,0.1);">'
            f'<span style="font-size:1.6rem;">{icon}</span>'
            f'<div>'
            f'<div style="font-family:\'Cinzel\',serif;font-size:0.95rem;'
            f'font-weight:600;color:#e2e8f0;line-height:1.2;">'
            f'{r["entity_name"]}</div>'
            f'<div style="font-size:10px;color:#64748b;'
            f'text-transform:uppercase;letter-spacing:0.08em;margin-top:2px;">'
            f'<span style="display:inline-block;width:5px;height:5px;'
            f'border-radius:50%;background:{health_color};'
            f'margin-right:4px;vertical-align:middle;"></span>'
            f'{r["entity_type"]} · {r["health_status"].upper()}</div>'
            f'</div>'
            f'<div style="margin-left:auto;padding:4px 12px;'
            f'background:{color}18;border:1px solid {color}40;'
            f'border-radius:20px;font-size:10px;font-weight:600;'
            f'color:{color};letter-spacing:0.05em;text-transform:uppercase;">'
            f'{r["archetype"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # ── Activity Stats ─────────────────────────────────────────
        stats = r["activity_stats"]
        st.markdown(
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);'
            f'gap:8px;margin-bottom:16px;">'

            f'<div style="background:rgba(15,23,42,0.5);'
            f'border:1px solid rgba(99,102,241,0.1);'
            f'border-radius:8px;padding:10px 12px;text-align:center;">'
            f'<div style="font-family:\'Cinzel\',serif;font-size:1.1rem;'
            f'color:#c7d2fe;font-weight:600;">'
            f'{format_number(stats["reads_24h"])}</div>'
            f'<div style="font-size:9px;color:#475569;'
            f'text-transform:uppercase;letter-spacing:0.06em;margin-top:2px;">'
            f'Reads/24h</div></div>'

            f'<div style="background:rgba(15,23,42,0.5);'
            f'border:1px solid rgba(99,102,241,0.1);'
            f'border-radius:8px;padding:10px 12px;text-align:center;">'
            f'<div style="font-family:\'Cinzel\',serif;font-size:1.1rem;'
            f'color:#c7d2fe;font-weight:600;">'
            f'{format_number(stats["writes_24h"])}</div>'
            f'<div style="font-size:9px;color:#475569;'
            f'text-transform:uppercase;letter-spacing:0.06em;margin-top:2px;">'
            f'Writes/24h</div></div>'

            f'<div style="background:rgba(15,23,42,0.5);'
            f'border:1px solid rgba(99,102,241,0.1);'
            f'border-radius:8px;padding:10px 12px;text-align:center;">'
            f'<div style="font-family:\'Cinzel\',serif;font-size:1.1rem;'
            f'color:{color};font-weight:600;">'
            f'{r["connections"]["upstream_count"]}↑ '
            f'{r["connections"]["downstream_count"]}↓</div>'
            f'<div style="font-size:9px;color:#475569;'
            f'text-transform:uppercase;letter-spacing:0.06em;margin-top:2px;">'
            f'Connections</div></div>'

            f'</div>',
            unsafe_allow_html=True
        )

        # ── Narrative ──────────────────────────────────────────────
        st.markdown(
            f'<div style="font-family:\'Cinzel\',serif;font-size:9px;'
            f'letter-spacing:0.2em;color:#475569;'
            f'text-transform:uppercase;margin-bottom:10px;">'
            f'✦ The Lore Weaver Speaks</div>',
            unsafe_allow_html=True
        )

        # Render narrative — convert markdown bold/italic to HTML tags
        import re as _re
        narrative_html = r["narrative"]
        narrative_html = narrative_html.replace("\n\n", "</p><p>").replace("\n", " ")
        # Convert **bold** → <strong>bold</strong>
        narrative_html = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', narrative_html)
        # Convert *italic* → <em>italic</em>
        narrative_html = _re.sub(r'\*(.+?)\*', r'<em>\1</em>', narrative_html)
        narrative_html = (
            f'<div style="font-family:\'Crimson Pro\',serif;'
            f'font-size:1.05rem;line-height:1.85;color:#cbd5e1;'
            f'font-weight:300;">'
            f'<p style="margin-top:0">{narrative_html}</p>'
            f'</div>'
        )
        st.markdown(narrative_html, unsafe_allow_html=True)

        # ── Insight Box ────────────────────────────────────────────
        insight_type = r["insight_type"]
        insight_colors = {
            "healthy": ("#22c55e", "rgba(34,197,94,0.08)", "rgba(34,197,94,0.25)"),
            "warning": ("#fde68a", "rgba(251,191,36,0.08)", "rgba(251,191,36,0.25)"),
            "critical": ("#a5b4fc", "rgba(99,102,241,0.08)", "rgba(99,102,241,0.25)"),
            "info": ("#94a3b8", "rgba(148,163,184,0.08)", "rgba(148,163,184,0.2)")
        }
        ic, ibg, ibr = insight_colors.get(insight_type, insight_colors["info"])
        st.markdown(
            f'<div style="background:{ibg};border:1px solid {ibr};'
            f'border-radius:8px;padding:10px 14px;'
            f'font-size:12px;color:{ic};margin-top:12px;">'
            f'{"⚠️" if insight_type == "warning" else "◈"} {r["insight"]}'
            f'</div>',
            unsafe_allow_html=True
        )

        # ── Connections ────────────────────────────────────────────
        if (r["connections"]["upstream_names"] or
                r["connections"]["downstream_names"]):
            col_up, col_down = st.columns(2)
            with col_up:
                st.markdown(
                    '<div style="background:rgba(15,23,42,0.5);'
                    'border:1px solid rgba(99,102,241,0.1);'
                    'border-radius:8px;padding:10px 12px;">'
                    '<div style="font-size:9px;color:#475569;'
                    'text-transform:uppercase;letter-spacing:0.1em;'
                    'margin-bottom:7px;">↑ Upstream</div>',
                    unsafe_allow_html=True
                )
                if r["connections"]["upstream_names"]:
                    for name in r["connections"]["upstream_names"]:
                        st.markdown(
                            f'<div style="font-size:11px;color:#94a3b8;'
                            f'padding:3px 0;border-bottom:1px solid '
                            f'rgba(99,102,241,0.06);">{name}</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        '<div style="font-size:11px;color:#334155;'
                        'font-style:italic;">Primal source</div>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            with col_down:
                st.markdown(
                    '<div style="background:rgba(15,23,42,0.5);'
                    'border:1px solid rgba(99,102,241,0.1);'
                    'border-radius:8px;padding:10px 12px;">'
                    '<div style="font-size:9px;color:#475569;'
                    'text-transform:uppercase;letter-spacing:0.1em;'
                    'margin-bottom:7px;">↓ Downstream</div>',
                    unsafe_allow_html=True
                )
                if r["connections"]["downstream_names"]:
                    for name in r["connections"]["downstream_names"]:
                        st.markdown(
                            f'<div style="font-size:11px;color:#94a3b8;'
                            f'padding:3px 0;border-bottom:1px solid '
                            f'rgba(99,102,241,0.06);">{name}</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        '<div style="font-size:11px;color:#334155;'
                        'font-style:italic;">Terminal node</div>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        # ── Citation ───────────────────────────────────────────────
        st.markdown(
            f'<div style="margin-top:14px;padding-top:12px;'
            f'border-top:1px solid rgba(99,102,241,0.08);'
            f'font-size:10px;color:#334155;font-style:italic;">'
            f'📎 {r["citation"]}</div>',
            unsafe_allow_html=True
        )

        # Close the outer div
        st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid rgba(99,102,241,0.08);
     padding:16px 48px; display:flex; align-items:center;
     justify-content:space-between; flex-wrap:wrap; gap:8px;">
  <div style="font-family:'Cinzel',serif;font-size:11px;
       color:#334155;letter-spacing:0.1em;">
    ✦ AETHER WEAVER · MICROSOFT AGENTS LEAGUE 2026
  </div>
  <div style="font-size:11px;color:#334155;">
    Built with GitHub Copilot ·
    <span style="color:#8b5cf6;">Fabric IQ</span> ·
    Creative Apps Track ·
    <span style="color:#334155;font-style:italic;">
    All data is synthetic — for demonstration only</span>
  </div>
</div>
""", unsafe_allow_html=True)
