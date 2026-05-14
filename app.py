import streamlit as st
import time
from agents import (
    orchestrator_agent, search_agent, price_agent,
    review_agent, comparison_agent, recommender_agent
)

st.set_page_config(
    page_title="AI Multi-Agent Shopping System",
    page_icon="🛒",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 32px;
    text-align: center;
    border: 1px solid #334155;
}
.hero h1 { color: #f1f5f9; font-size: 32px; font-weight: 700; margin-bottom: 8px; }
.hero p { color: #94a3b8; font-size: 16px; margin-bottom: 16px; }

.badge {
    display: inline-block;
    background: #1e293b;
    color: #64748b;
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
}
.badge.blue { border-color: #3b82f6; color: #60a5fa; }
.badge.green { border-color: #22c55e; color: #4ade80; }
.badge.purple { border-color: #8b5cf6; color: #a78bfa; }

.agent-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    min-height: 80px;
    transition: all 0.3s;
}
.agent-card.running { border-color: #3b82f6; background: #0f172a; }
.agent-card.done { border-color: #22c55e; }
.agent-card.error { border-color: #ef4444; }

.agent-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.agent-name { color: #f1f5f9; font-weight: 600; font-size: 14px; }
.agent-role { color: #64748b; font-size: 12px; }
.agent-output { color: #94a3b8; font-size: 13px; line-height: 1.6; margin-top: 10px; padding-top: 10px; border-top: 1px solid #334155; }

.status-waiting { background: #1e293b; color: #64748b; border: 1px solid #475569; border-radius: 6px; padding: 2px 8px; font-size: 11px; font-weight: 600; }
.status-running { background: #1e3a5f; color: #60a5fa; border: 1px solid #3b82f6; border-radius: 6px; padding: 2px 8px; font-size: 11px; font-weight: 600; }
.status-done { background: #14532d; color: #4ade80; border: 1px solid #22c55e; border-radius: 6px; padding: 2px 8px; font-size: 11px; font-weight: 600; }
.status-error { background: #450a0a; color: #f87171; border: 1px solid #ef4444; border-radius: 6px; padding: 2px 8px; font-size: 11px; font-weight: 600; }

.final-card {
    background: linear-gradient(135deg, #052e16, #14532d);
    border: 2px solid #22c55e;
    border-radius: 16px;
    padding: 24px;
    margin-top: 24px;
}
.final-card h3 { color: #4ade80; font-size: 18px; margin-bottom: 12px; }
.final-card p { color: #d1fae5; font-size: 15px; line-height: 1.8; white-space: pre-wrap; }

.metric-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.metric-label { color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.metric-val { color: #f1f5f9; font-size: 28px; font-weight: 700; }

.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin-bottom: 24px;
    flex-wrap: wrap;
}
.pdot {
    width: 40px; height: 40px; border-radius: 50%;
    background: #1e293b; border: 1px solid #475569;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; color: #64748b;
}
</style>
""", unsafe_allow_html=True)

# ─── HERO ───
st.markdown("""
<div class="hero">
    <h1>🛒 AI Multi-Agent Shopping System</h1>
    <p>6 specialized AI agents collaborate in real-time to find your perfect product</p>
    <span class="badge blue">🐍 Python</span>
    <span class="badge purple">🤖 Multi-Agent AI</span>
    <span class="badge green">✨ Claude Sonnet 4</span>
    <span class="badge">🚀 Live Demo</span>
</div>
""", unsafe_allow_html=True)

# ─── SEARCH ───
col_input, col_btn = st.columns([5, 1])
with col_input:
    query = st.text_input("", placeholder="e.g. best gaming laptop under ₹70,000 for college", label_visibility="collapsed")
with col_btn:
    run = st.button("▶ Run Agents", type="primary", use_container_width=True)

st.markdown("---")

# ─── AGENT DEFINITIONS ───
AGENTS = [
    {"id": "orchestrator", "name": "🧠 Orchestrator",      "role": "Plans the shopping strategy"},
    {"id": "search",       "name": "🔍 Search Agent",      "role": "Discovers relevant products"},
    {"id": "price",        "name": "💰 Price Analyst",     "role": "Finds best deals & prices"},
    {"id": "review",       "name": "⭐ Review Agent",      "role": "Analyzes customer reviews"},
    {"id": "compare",      "name": "⚖️ Comparison Agent", "role": "Compares top options"},
    {"id": "recommender",  "name": "🎯 Recommender",       "role": "Delivers final recommendation"},
]

# ─── METRICS ROW ───
m1, m2, m3 = st.columns(3)
active_ph  = m1.empty()
done_ph    = m2.empty()
time_ph    = m3.empty()

def render_metric(ph, label, val):
    ph.markdown(f"""<div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-val">{val}</div>
    </div>""", unsafe_allow_html=True)

render_metric(active_ph, "Active Agents", "0")
render_metric(done_ph,   "Completed",     "0")
render_metric(time_ph,   "Time (s)",      "—")

st.markdown("<br>", unsafe_allow_html=True)

# ─── AGENT CARDS ───
left_col, right_col = st.columns(2)
card_placeholders = {}
for i, agent in enumerate(AGENTS):
    col = left_col if i % 2 == 0 else right_col
    with col:
        card_placeholders[agent["id"]] = st.empty()

def render_card(ph, agent, status="waiting", output=""):
    status_html = f'<span class="status-{status}">{status.upper()}</span>'
    out_html = f'<div class="agent-output">{output}</div>' if output else f'<div class="agent-role">{agent["role"]}</div>'
    ph.markdown(f"""<div class="agent-card {status}">
        <div class="agent-header">
            <span class="agent-name">{agent["name"]}</span>
            {status_html}
        </div>
        {out_html}
    </div>""", unsafe_allow_html=True)

for agent in AGENTS:
    render_card(card_placeholders[agent["id"]], agent)

final_ph = st.empty()

# ─── RUN PIPELINE ───
if run and query.strip():
    accumulated = ""
    done_count = 0
    start_time = time.time()

    # Reset cards
    for agent in AGENTS:
        render_card(card_placeholders[agent["id"]], agent)
    final_ph.empty()

    agent_funcs = {
        "orchestrator": lambda q: orchestrator_agent(q),
        "search":       lambda q: search_agent(q),
        "price":        lambda q: price_agent(q, accumulated),
        "review":       lambda q: review_agent(q, accumulated),
        "compare":      lambda q: comparison_agent(q, accumulated),
        "recommender":  lambda q: recommender_agent(q, accumulated),
    }

    for agent in AGENTS:
        render_card(card_placeholders[agent["id"]], agent, "running", "Analyzing...")
        render_metric(active_ph, "Active Agents", "1")

        try:
            result = agent_funcs[agent["id"]](query)
            accumulated += f"\n[{agent['name']}]: {result}"
            done_count += 1
            render_card(card_placeholders[agent["id"]], agent, "done", result)

            elapsed = round(time.time() - start_time, 1)
            render_metric(active_ph, "Active Agents", "0")
            render_metric(done_ph,   "Completed",     done_count)
            render_metric(time_ph,   "Time (s)",      elapsed)

            if agent["id"] == "recommender":
                final_ph.markdown(f"""<div class="final-card">
                    <h3>🎯 Final AI Recommendation</h3>
                    <p>{result}</p>
                </div>""", unsafe_allow_html=True)
        except Exception as e:
            render_card(card_placeholders[agent["id"]], agent, "error", f"Error: {str(e)[:100]}")

elif run and not query.strip():
    st.warning("Please enter what you want to buy!")
