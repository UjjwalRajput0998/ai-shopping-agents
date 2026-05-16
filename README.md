# 🛒 AI Multi-Agent Shopping System

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-red?style=flat-square&logo=streamlit)
![Claude AI](https://img.shields.io/badge/Claude-Sonnet%204-orange?style=flat-square)
![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-purple?style=flat-square)

> 6 specialized AI agents collaborate in real-time to find you the best product deal — built with Python + Streamlit + Claude AI.

🔗 **[Live Demo →](https://ai-shopping-agents.streamlit.app)**

---

## 🤖 The 6 Agents

| Agent | Role |
|-------|------|
| 🧠 Orchestrator | Plans the shopping strategy |
| 🔍 Search Agent | Discovers relevant products |
| 💰 Price Analyst | Finds best deals & price ranges |
| ⭐ Review Agent | Analyzes customer reviews |
| ⚖️ Comparison Agent | Compares top options |
| 🎯 Recommender | Final recommendation + confidence score |

---

## 🏗️ Architecture

```
User Query
    ↓
Orchestrator Agent (plans strategy)
    ↓
Search Agent → Price Analyst → Review Agent → Comparison Agent
    ↓
Recommender Agent (final decision)
```

Each agent passes context to the next — building a complete shopping analysis.

---

## 🚀 Tech Stack

- **Language**: Python 3.10+
- **UI Framework**: Streamlit
- **AI Engine**: Anthropic Claude Sonnet 4
- **Pattern**: Sequential Multi-Agent Pipeline
- **Deploy**: Streamlit Community Cloud (Free)

---

## ⚙️ Run Locally

```bash
# 1. Clone repo
git clone https://github.com/yourusername/ai-shopping-agents.git
cd ai-shopping-agents

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your Anthropic API key

# 4. Run
streamlit run app.py
```

Get free API key at: [console.anthropic.com](https://console.anthropic.com)

---

## 🌐 Deploy Free on Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. In **App Settings → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Click Deploy → get live URL!

---

## 🧠 Concepts Demonstrated

- Multi-Agent Architecture (single responsibility per agent)
- Prompt Engineering (specialized system prompts)
- Context Passing (agents build on each other's output)
- Agent Orchestration Pattern
- Real-time UI with live status updates

---

## 📁 Project Structure

```
ai-shopping-agents/
├── app.py              # Streamlit UI
├── agents.py           # 6 AI agent functions
├── requirements.txt    # Python dependencies
├── .streamlit/
│   ├── config.toml     # Theme config
│   └── secrets.toml    # API key (not committed to GitHub)
└── README.md
```

---

MIT License | Built with Anthropic Claude AI ⭐
