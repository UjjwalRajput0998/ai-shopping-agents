import streamlit as st
from groq import Groq

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Multi-Agent Shopping System",
    page_icon="🛒",
    layout="wide"
)

# ── Groq client ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

MODEL = "llama-3.3-70b-versatile"

# ── Agent definitions ─────────────────────────────────────────────────────────
AGENTS = [
    {"id": "orchestrator", "name": "🧠 Orchestrator",      "role": "Plans shopping strategy"},
    {"id": "search",       "name": "🔍 Search Agent",      "role": "Discovers relevant products"},
    {"id": "price",        "name": "💰 Price Analyst",     "role": "Finds best deals & prices"},
    {"id": "review",       "name": "⭐ Review Agent",      "role": "Analyzes customer reviews"},
    {"id": "compare",      "name": "⚖️ Comparison Agent", "role": "Compares top options"},
    {"id": "recommender",  "name": "🎯 Recommender",       "role": "Delivers final recommendation"},
]

SYSTEM_PROMPTS = {
    "orchestrator": "You are the Orchestrator Agent in an AI Multi-Agent Shopping System. Analyze the shopping query and create a brief strategy. List 4 key focus areas. Under 80 words.",
    "search":       "You are the Search Agent. Find 3 specific products with exact model names, key specs, and prices in INR. Be realistic. Under 100 words.",
    "price":        "You are the Price Analyst. Give budget/mid-range/premium price ranges in INR, best platforms (Amazon, Flipkart etc), and any deals. Under 90 words.",
    "review":       "You are the Review Agent. Give 3 common pros and 2 common cons from typical user reviews. Be specific. Under 90 words.",
    "compare":      "You are the Comparison Agent. Compare top 3 options on Performance, Value for money, and Build quality. Plain text. Under 100 words.",
    "recommender":  "You are the Recommender Agent. Give ONE specific product: exact model, best price in INR, top platform to buy, 2 key reasons. End with 'Confidence: XX%'. Under 100 words.",
}

def run_agent(agent_id: str, query: str, context: str) -> str:
    user_msgs = {
        "orchestrator": f'Shopping query: "{query}"',
        "search":       f'Find products for: "{query}"',
        "price":        f'Products found: {context[:400]}\nQuery: "{query}"',
        "review":       f'Products context: {context[:400]}\nQuery: "{query}"',
        "compare":      f'All data: {context[:600]}\nQuery: "{query}"',
        "recommender":  f'All agent findings: {context[:800]}\nUser wants: "{query}"',
    }
    client = get_client()
    resp = client.chat.completions.create(
        model=MODEL,
        max_tokens=500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[agent_id]},
            {"role": "user",   "content": user_msgs[agent_id]},
        ],
    )
    return resp.choices[0].message.content

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0d0d12; }
[data-testid="stHeader"] { background: transparent; }
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.3rem;
}
.sub-title {
    text-align: center;
    color: #888899;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}
.badges {
    display: flex; gap: 10px; justify-content: center;
    flex-wrap: wrap; margin-bottom: 2rem;
}
.badge {
    padding: 5px 14px; border-radius: 20px; font-size: 13px;
    font-weight: 600; border: 1.5px solid;
}
.badge-blue  { color:#4f9eff; border-color:#4f9eff; background:rgba(79,158,255,0.1); }
.badge-green { color:#4ade80; border-color:#4ade80; background:rgba(74,222,128,0.1); }
.badge-purple{ color:#a78bfa; border-color:#a78bfa; background:rgba(167,139,250,0.1); }
.badge-gray  { color:#888899; border-color:#555566; background:rgba(255,255,255,0.05); }
.agent-card {
    background: #14141c;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    min-height: 80px;
}
.agent-card.running { border-color: #4f9eff; }
.agent-card.done    { border-color: #4ade80; }
.agent-card.error   { border-color: #f87171; }
.agent-name { font-size: 15px; font-weight: 600; color: #f0f0f5; }
.agent-role { font-size: 12px; color: #555566; margin-top: 2px; }
.agent-output { font-size: 13px; color: #888899; margin-top: 10px; line-height: 1.6; }
.final-box {
    background: #14141c;
    border: 2px solid #4ade80;
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1rem;
}
.final-title { font-size: 18px; font-weight: 700; color: #f0f0f5; margin-bottom: 10px; }
.final-body  { font-size: 14px; color: #888899; line-height: 1.8; }
.metric-box {
    background: #14141c;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-label { font-size: 11px; color: #555566; text-transform: uppercase; letter-spacing: 1px; }
.metric-val   { font-size: 28px; font-weight: 700; color: #f0f0f5; }
</style>
""", unsafe_allow_html=True)

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🛒 AI Multi-Agent Shopping System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">6 specialized AI agents collaborate in real-time to find your perfect product</div>', unsafe_allow_html=True)
st.markdown("""
<div class="badges">
  <span class="badge badge-blue">🐍 Python</span>
  <span class="badge badge-purple">🤖 Multi-Agent AI</span>
  <span class="badge badge-green">⚡ Groq LLaMA 3.3</span>
  <span class="badge badge-gray">🚀 Live Demo</span>
</div>
""", unsafe_allow_html=True)

query = st.text_input("", placeholder="e.g. best gaming laptop under ₹70,000 for college", label_visibility="collapsed")
run = st.button("▶ Run Agents", use_container_width=True, type="primary")

# Metrics
col1, col2, col3 = st.columns(3)
m_active = col1.empty()
m_done   = col2.empty()
m_time   = col3.empty()

def show_metrics(active=0, done=0, time_s="—"):
    m_active.markdown(f'<div class="metric-box"><div class="metric-label">Active Agents</div><div class="metric-val">{active}</div></div>', unsafe_allow_html=True)
    m_done.markdown(  f'<div class="metric-box"><div class="metric-label">Completed</div><div class="metric-val">{done}</div></div>',       unsafe_allow_html=True)
    m_time.markdown(  f'<div class="metric-box"><div class="metric-label">Time (s)</div><div class="metric-val">{time_s}</div></div>',       unsafe_allow_html=True)

show_metrics()

st.markdown("---")

# Agent placeholders
agent_slots = {}
cols = st.columns(2)
for i, agent in enumerate(AGENTS):
    with cols[i % 2]:
        agent_slots[agent["id"]] = st.empty()
        agent_slots[agent["id"]].markdown(
            f'<div class="agent-card"><div class="agent-name">{agent["name"]}</div><div class="agent-role">{agent["role"]}</div><div class="agent-output" style="color:#333344">⏳ Waiting...</div></div>',
            unsafe_allow_html=True
        )

final_slot = st.empty()

# ── Run agents ────────────────────────────────────────────────────────────────
if run and query:
    import time
    context = ""
    done_count = 0
    start = time.time()

    for agent in AGENTS:
        # Mark as running
        agent_slots[agent["id"]].markdown(
            f'<div class="agent-card running"><div class="agent-name">{agent["name"]} <span style="color:#4f9eff;font-size:11px">● RUNNING</span></div><div class="agent-role">{agent["role"]}</div><div class="agent-output" style="color:#4f9eff">🔄 Analyzing...</div></div>',
            unsafe_allow_html=True
        )
        show_metrics(active=1, done=done_count, time_s=f"{time.time()-start:.1f}")

        try:
            output = run_agent(agent["id"], query, context)
            context += f'\n[{agent["name"]}]: {output}'
            done_count += 1

            agent_slots[agent["id"]].markdown(
                f'<div class="agent-card done"><div class="agent-name">{agent["name"]} <span style="color:#4ade80;font-size:11px">✓ DONE</span></div><div class="agent-role">{agent["role"]}</div><div class="agent-output">{output}</div></div>',
                unsafe_allow_html=True
            )

            if agent["id"] == "recommender":
                final_slot.markdown(
                    f'<div class="final-box"><div class="final-title">🎯 Final AI Recommendation</div><div class="final-body">{output}</div></div>',
                    unsafe_allow_html=True
                )

        except Exception as e:
            agent_slots[agent["id"]].markdown(
                f'<div class="agent-card error"><div class="agent-name">{agent["name"]} <span style="color:#f87171;font-size:11px">✗ ERROR</span></div><div class="agent-role">{agent["role"]}</div><div class="agent-output" style="color:#f87171">{str(e)}</div></div>',
                unsafe_allow_html=True
            )

        show_metrics(active=0, done=done_count, time_s=f"{time.time()-start:.1f}")

    st.success(f"✅ All agents completed in {time.time()-start:.1f} seconds!")

elif run and not query:
    st.warning("⚠️ Please enter a product to search!")
