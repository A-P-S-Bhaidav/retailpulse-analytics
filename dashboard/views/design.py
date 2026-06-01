"""RetailPulse — Shared design tokens used across all dashboard views."""

# ── Color palette ─────────────────────────────────────────────────────────────
C = {
    # Brand
    "navy":        "#0F2B4C",   # darkest brand blue — headers, sidebar
    "blue":        "#1D4ED8",   # links, accent highlights
    "teal":        "#0891B2",   # chart primary series

    # Semantic
    "green":       "#059669",   # positive / success
    "amber":       "#D97706",   # warning / reorder trigger
    "red":         "#DC2626",   # danger / stockout / high risk

    # Neutrals — high contrast on white/light bg
    "text_h":      "#0F172A",   # headings: near-black
    "text_b":      "#1E293B",   # body text: very dark slate
    "text_sub":    "#334155",   # sub-labels: dark slate (WCAG AAA)
    "text_hint":   "#475569",   # hints / captions: medium-dark

    # Backgrounds
    "bg_page":     "#EEF2F7",   # page background
    "bg_card":     "#FFFFFF",   # card surface
    "border":      "#CBD5E1",   # card/table borders
    "bg_subtle":   "#F8FAFC",   # subtle alternating row tint
}

# ── Chart template ────────────────────────────────────────────────────────────
LAYOUT = dict(
    template="plotly_white",
    font=dict(
        family="Inter, Helvetica Neue, Arial, sans-serif",
        size=12,
        color=C["text_b"],
    ),
    title_font=dict(size=14, color=C["text_h"], family="Inter, sans-serif"),
    margin=dict(l=12, r=12, t=44, b=12),
    paper_bgcolor=C["bg_card"],
    plot_bgcolor=C["bg_card"],
    hoverlabel=dict(
        bgcolor=C["bg_card"],
        font_color=C["text_b"],
        font_size=12,
        bordercolor=C["border"],
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor="#E2E8F0",
        gridwidth=1,
        linecolor=C["border"],
        tickfont=dict(color=C["text_sub"], size=11),
        title_font=dict(color=C["text_b"], size=12, family="Inter"),
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#E2E8F0",
        gridwidth=1,
        linecolor=C["border"],
        tickfont=dict(color=C["text_sub"], size=11),
        title_font=dict(color=C["text_b"], size=12, family="Inter"),
    ),
    legend=dict(
        font=dict(color=C["text_b"], size=11),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor=C["border"],
        borderwidth=1,
    ),
)

# ── Reusable card component ───────────────────────────────────────────────────
def kpi_card(col, label, value, sub="", value_color=None):
    """Render a KPI card in the given Streamlit column."""
    import streamlit as st
    v_color = value_color or C["text_h"]
    col.markdown(f"""
    <div style="
      background:{C['bg_card']};
      border:1px solid {C['border']};
      border-radius:10px;
      padding:20px 14px;
      text-align:center;
      box-shadow:0 1px 4px rgba(15,23,42,0.07);
    ">
      <div style="
        font-size:0.7rem;
        font-weight:700;
        color:{C['text_sub']};
        text-transform:uppercase;
        letter-spacing:0.07em;
        margin-bottom:8px;
      ">{label}</div>
      <div style="
        font-size:1.75rem;
        font-weight:700;
        color:{v_color};
        line-height:1.1;
        margin-bottom:5px;
      ">{value}</div>
      <div style="
        font-size:0.78rem;
        color:{C['text_hint']};
        font-weight:500;
      ">{sub}</div>
    </div>""", unsafe_allow_html=True)


def page_header(module_num, title, subtitle):
    """Render the top dark banner for each page."""
    import streamlit as st
    st.markdown(f"""
    <div style="
      background:linear-gradient(135deg, {C['navy']} 0%, #1A3D6B 100%);
      border-radius:12px;
      padding:26px 32px;
      margin-bottom:28px;
      box-shadow:0 2px 8px rgba(15,23,42,0.15);
    ">
      <div style="
        color:rgba(203,213,225,0.9);
        font-size:0.72rem;
        font-weight:700;
        letter-spacing:0.12em;
        text-transform:uppercase;
        margin-bottom:6px;
      ">Module {module_num} of 4</div>
      <div style="
        color:#FFFFFF;
        font-size:1.75rem;
        font-weight:700;
        letter-spacing:-0.01em;
        margin-bottom:4px;
      ">{title}</div>
      <div style="
        color:#94A3B8;
        font-size:0.88rem;
        font-weight:400;
      ">{subtitle}</div>
    </div>""", unsafe_allow_html=True)


def section_title(text):
    """Render a section subheading with high contrast."""
    import streamlit as st
    st.markdown(f"""
    <div style="
      font-size:0.95rem;
      font-weight:700;
      color:{C['text_h']};
      margin:8px 0 12px 0;
      padding-bottom:6px;
      border-bottom:2px solid #E2E8F0;
      letter-spacing:-0.01em;
    ">{text}</div>""", unsafe_allow_html=True)
