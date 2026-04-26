"""
LLM Bias Detector — Streamlit Dashboard
Analyzes LLM-generated text for biases using Google Gemini API.
"""

import streamlit as st
import plotly.graph_objects as go
from bias_analyzer import BiasAnalyzer, BiasAnalysisError

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LLM Bias Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

/* ── Main container ── */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* ── Hero header ── */
.hero-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.hero-header h1 {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7C3AED 0%, #EC4899 50%, #F59E0B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}
.hero-header p {
    font-size: 1.1rem;
    color: #94A3B8;
    font-weight: 300;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(145deg, #1E293B 0%, #334155 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.15);
}
.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0.3rem 0;
}
.metric-label {
    font-size: 0.85rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

/* ── Bias card ── */
.bias-card {
    background: linear-gradient(145deg, #1E293B 0%, #1a2536 100%);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #7C3AED;
    transition: transform 0.15s ease;
}
.bias-card:hover {
    transform: translateX(4px);
}

/* Severity badges */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-critical { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.3); }
.badge-high     { background: rgba(249, 115, 22, 0.2); color: #FB923C; border: 1px solid rgba(249, 115, 22, 0.3); }
.badge-medium   { background: rgba(234, 179, 8, 0.2);  color: #FACC15; border: 1px solid rgba(234, 179, 8, 0.3);  }
.badge-low      { background: rgba(34, 197, 94, 0.2);  color: #4ADE80; border: 1px solid rgba(34, 197, 94, 0.3);  }

/* Excerpt highlight */
.excerpt-box {
    background: rgba(124, 58, 237, 0.08);
    border-left: 3px solid #7C3AED;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.8rem 0;
    font-style: italic;
    color: #CBD5E1;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Suggestion box */
.suggestion-box {
    background: rgba(34, 197, 94, 0.06);
    border-left: 3px solid #4ADE80;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.8rem 0;
    color: #A7F3D0;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Section headers */
.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #E2E8F0;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(124, 58, 237, 0.3);
}

/* Summary box */
.summary-box {
    background: linear-gradient(145deg, rgba(124, 58, 237, 0.08) 0%, rgba(236, 72, 153, 0.05) 100%);
    border: 1px solid rgba(124, 58, 237, 0.2);
    border-radius: 14px;
    padding: 1.5rem;
    font-size: 1.05rem;
    line-height: 1.7;
    color: #CBD5E1;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
}

/* Button styling */
.stButton>button {
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #6D28D9 0%, #5B21B6 100%) !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* Text area */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    background: #1E293B !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    transition: border-color 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
}

/* Spinner */
.stSpinner > div { border-top-color: #7C3AED !important; }

/* Animated entrance */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeInUp 0.5s ease-out forwards; }
</style>
""", unsafe_allow_html=True)


# ── Example texts ────────────────────────────────────────────────────────────
EXAMPLES = {
    "🏢 Biased Job Description": (
        "We are looking for a young, energetic salesman to join our dynamic team. "
        "The ideal candidate is a natural-born leader with a strong work ethic — "
        "someone who graduated from a top-tier Ivy League university and has "
        "connections in high-society circles. We need a guy who can handle pressure "
        "and isn't afraid of long hours. Older applicants need not apply as this "
        "role requires someone who is tech-savvy and up-to-date with modern trends."
    ),
    "📰 Biased News Article": (
        "The crime rate in inner-city neighborhoods continues to rise, largely due "
        "to the influx of immigrants who refuse to integrate into American society. "
        "These communities, predominantly populated by minorities, have shown little "
        "interest in education or self-improvement. Meanwhile, suburban families "
        "continue to thrive thanks to their strong traditional values and hard work. "
        "Experts suggest that the solution lies in stricter immigration policies."
    ),
    "✅ Neutral / Unbiased Text": (
        "Photosynthesis is the process by which green plants and some other organisms "
        "use sunlight to synthesize foods from carbon dioxide and water. The process "
        "involves the green pigment chlorophyll and generates oxygen as a by-product. "
        "It is one of the most important biochemical pathways on Earth, as it provides "
        "the foundation for most food chains and produces the oxygen that aerobic "
        "organisms need to survive."
    ),
}


# ── Helper functions ─────────────────────────────────────────────────────────
def get_score_color(score: int) -> str:
    """Return a color based on the bias score."""
    if score <= 15:
        return "#4ADE80"  # green
    elif score <= 40:
        return "#FACC15"  # yellow
    elif score <= 70:
        return "#FB923C"  # orange
    else:
        return "#F87171"  # red


def get_score_label(score: int) -> str:
    """Return a human-readable label for the bias score."""
    if score <= 15:
        return "Minimal Bias"
    elif score <= 40:
        return "Moderate Bias"
    elif score <= 70:
        return "Significant Bias"
    else:
        return "Severe Bias"


def create_gauge_chart(score: int) -> go.Figure:
    """Create a Plotly gauge chart for the overall bias score."""
    color = get_score_color(score)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 56, "color": color, "family": "Inter"}, "suffix": ""},
        title={"text": get_score_label(score), "font": {"size": 18, "color": "#94A3B8", "family": "Inter"}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 2,
                "tickcolor": "#334155",
                "tickfont": {"color": "#64748B", "size": 11},
            },
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "#1E293B",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 15], "color": "rgba(74, 222, 128, 0.1)"},
                {"range": [15, 40], "color": "rgba(250, 204, 21, 0.1)"},
                {"range": [40, 70], "color": "rgba(251, 146, 60, 0.1)"},
                {"range": [70, 100], "color": "rgba(248, 113, 113, 0.1)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.8,
                "value": score,
            },
        },
    ))

    fig.update_layout(
        height=280,
        margin=dict(l=30, r=30, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter"},
    )
    return fig


def create_category_chart(biases: list) -> go.Figure:
    """Create a horizontal bar chart of bias categories and their severity."""
    severity_map = {"low": 25, "medium": 50, "high": 75, "critical": 100}
    color_map = {
        "low": "#4ADE80",
        "medium": "#FACC15",
        "high": "#FB923C",
        "critical": "#F87171",
    }

    categories = [b["category"] for b in biases]
    values = [severity_map.get(b.get("severity", "low"), 25) for b in biases]
    colors = [color_map.get(b.get("severity", "low"), "#4ADE80") for b in biases]

    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(width=0),
            cornerradius=6,
        ),
        text=[b.get("severity", "").upper() for b in biases],
        textposition="inside",
        textfont=dict(color="white", size=11, family="Inter"),
        hovertemplate="<b>%{y}</b><br>Severity: %{text}<extra></extra>",
    ))

    fig.update_layout(
        height=max(180, len(biases) * 55 + 60),
        margin=dict(l=10, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, 110],
        ),
        yaxis=dict(
            tickfont=dict(color="#CBD5E1", size=12, family="Inter"),
            autorange="reversed",
        ),
        bargap=0.35,
        font={"family": "Inter"},
    )
    return fig


def render_bias_card(bias: dict, index: int):
    """Render a single bias finding card."""
    severity = bias.get("severity", "low")
    category = bias.get("category", "Unknown")
    excerpt = bias.get("excerpt", "")
    explanation = bias.get("explanation", "")
    suggestion = bias.get("suggestion", "")

    border_colors = {
        "critical": "#F87171",
        "high": "#FB923C",
        "medium": "#FACC15",
        "low": "#4ADE80",
    }
    border = border_colors.get(severity, "#7C3AED")

    st.markdown(f"""
    <div class="bias-card animate-in" style="border-left-color: {border}; animation-delay: {index * 0.1}s;">
        <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem;">
            <span style="font-size: 1.1rem; font-weight: 600; color: #E2E8F0;">{category}</span>
            <span class="badge badge-{severity}">{severity}</span>
        </div>
        <div class="excerpt-box">"{excerpt}"</div>
        <p style="color: #CBD5E1; font-size: 0.92rem; line-height: 1.6; margin: 0.5rem 0;">
            <strong style="color: #E2E8F0;">Analysis:</strong> {explanation}
        </p>
        {f'<div class="suggestion-box">💡 <strong>Suggestion:</strong> {suggestion}</div>' if suggestion else ''}
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
        <h2 style="font-size: 1.3rem; font-weight: 700; color: #E2E8F0; margin: 0;">
            LLM Bias Detector
        </h2>
        <p style="color: #64748B; font-size: 0.85rem; margin-top: 0.3rem;">
            Powered by Google Gemini
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # API Key input
    st.markdown('<p style="color: #94A3B8; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">🔑 Gemini API Key</p>', unsafe_allow_html=True)
    api_key_input = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your GEMINI_API_KEY here",
        label_visibility="collapsed",
        key="api_key_input",
    )
    if api_key_input:
        st.session_state["gemini_api_key"] = api_key_input
        st.markdown("""
        <div style="background: rgba(74, 222, 128, 0.08); border: 1px solid rgba(74, 222, 128, 0.2);
                    border-radius: 10px; padding: 0.6rem; text-align: center; margin-top: 0.5rem;">
            <span style="color: #4ADE80; font-weight: 600; font-size: 0.85rem;">✓ API Key Set</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(248, 113, 113, 0.08); border: 1px solid rgba(248, 113, 113, 0.2);
                    border-radius: 10px; padding: 0.6rem; text-align: center; margin-top: 0.5rem;">
            <span style="color: #F87171; font-weight: 600; font-size: 0.85rem;">Enter key to get started</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Example texts
    st.markdown('<p style="color: #94A3B8; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">📋 Try an Example</p>', unsafe_allow_html=True)

    for name, text in EXAMPLES.items():
        if st.button(name, key=f"example_{name}", use_container_width=True):
            st.session_state["input_text"] = text

    st.divider()

    st.markdown("""
    <div style="padding: 0.8rem; background: rgba(124, 58, 237, 0.06);
                border-radius: 10px; border: 1px solid rgba(124, 58, 237, 0.15);">
        <p style="color: #94A3B8; font-size: 0.8rem; line-height: 1.6; margin: 0;">
            <strong style="color: #C4B5FD;">How it works:</strong><br>
            1. Paste any LLM response<br>
            2. Gemini analyzes for 10+ bias types<br>
            3. Get severity scores & suggestions
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── Main Content ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>LLM Bias Detector</h1>
    <p>Paste any LLM-generated text below and let Gemini analyze it for hidden biases</p>
</div>
""", unsafe_allow_html=True)

# Text input
input_text = st.text_area(
    "Paste LLM response here",
    value=st.session_state.get("input_text", ""),
    height=200,
    placeholder="Paste the text you want to analyze for bias...",
    label_visibility="collapsed",
)

# Analyze button
col_left, col_btn, col_right = st.columns([1, 1, 1])
with col_btn:
    analyze_clicked = st.button("🔍  Analyze for Bias", type="primary", use_container_width=True)

# ── Analysis ─────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not input_text.strip():
        st.warning("⚠️ Please paste some text to analyze.", icon="⚠️")
    else:
        user_key = st.session_state.get("gemini_api_key", "")
        if not user_key:
            st.error("❌ Please enter your Gemini API key in the sidebar first.", icon="🔑")
        else:
            with st.spinner("🧠 Gemini is analyzing your text for biases..."):
                try:
                    analyzer = BiasAnalyzer(api_key=user_key)
                    result = analyzer.analyze(input_text)
                    st.session_state["result"] = result
                    st.session_state["analyzed_text"] = input_text
                except BiasAnalysisError as e:
                    st.error(f"❌ {e}", icon="🚨")
                    st.stop()

# ── Results Dashboard ────────────────────────────────────────────────────────
if "result" in st.session_state:
    result = st.session_state["result"]
    score = result.get("overall_bias_score", 0)
    biases = result.get("biases", [])
    summary = result.get("summary", "")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Metrics Row ──
    col1, col2, col3 = st.columns(3)

    with col1:
        score_color = get_score_color(score)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Bias Score</div>
            <div class="metric-value" style="color: {score_color};">{score}</div>
            <div style="color: #64748B; font-size: 0.8rem;">out of 100</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Biases Found</div>
            <div class="metric-value" style="color: #C4B5FD;">{len(biases)}</div>
            <div style="color: #64748B; font-size: 0.8rem;">unique instances</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        if biases:
            max_sev = max(biases, key=lambda b: severity_order.get(b.get("severity", "low"), 0))
            max_sev_text = max_sev.get("severity", "low").upper()
            sev_colors = {"CRITICAL": "#F87171", "HIGH": "#FB923C", "MEDIUM": "#FACC15", "LOW": "#4ADE80"}
            sev_color = sev_colors.get(max_sev_text, "#4ADE80")
        else:
            max_sev_text = "NONE"
            sev_color = "#4ADE80"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Highest Severity</div>
            <div class="metric-value" style="color: {sev_color}; font-size: 1.8rem;">{max_sev_text}</div>
            <div style="color: #64748B; font-size: 0.8rem;">severity level</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary ──
    st.markdown('<div class="section-header">📝 Summary</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row ──
    if biases:
        chart_col1, chart_col2 = st.columns([1, 1])

        with chart_col1:
            st.markdown('<div class="section-header">📊 Bias Score</div>', unsafe_allow_html=True)
            st.plotly_chart(create_gauge_chart(score), use_container_width=True, config={"displayModeBar": False})

        with chart_col2:
            st.markdown('<div class="section-header">📈 Bias Breakdown</div>', unsafe_allow_html=True)
            st.plotly_chart(create_category_chart(biases), use_container_width=True, config={"displayModeBar": False})

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Detailed Findings ──
        st.markdown(f'<div class="section-header">🔎 Detailed Findings ({len(biases)})</div>', unsafe_allow_html=True)

        for i, bias in enumerate(biases):
            render_bias_card(bias, i)
    else:
        # No biases found — show a success state
        st.markdown("<br>", unsafe_allow_html=True)
        chart_col1, chart_col2, chart_col3 = st.columns([1, 1, 1])
        with chart_col2:
            st.plotly_chart(create_gauge_chart(score), use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div style="text-align: center; padding: 2rem; animation: fadeInUp 0.5s ease-out;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">✅</div>
            <h3 style="color: #4ADE80; font-weight: 600;">No Significant Biases Detected</h3>
            <p style="color: #94A3B8;">The analyzed text appears to be fair and balanced.</p>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 1.5rem; border-top: 1px solid #1E293B;">
    <p style="color: #475569; font-size: 0.8rem; margin: 0;">
        Built with ❤️ using Streamlit & Google Gemini API  •
        Bias detection is AI-assisted and may not catch every nuance
    </p>
</div>
""", unsafe_allow_html=True)
