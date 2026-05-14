from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

AGENTS = [
    {"id": "orchestrator", "name": "Orchestrator"},
    {"id": "search",       "name": "Search Agent"},
    {"id": "price",        "name": "Price Analyst"},
    {"id": "review",       "name": "Review Agent"},
    {"id": "compare",      "name": "Comparison Agent"},
    {"id": "recommender",  "name": "Recommender"},
]

SYSTEM_PROMPTS = {
    "orchestrator": "You are the Orchestrator Agent in an AI Multi-Agent Shopping System. Analyze the shopping query and create a brief strategy. List 4 key focus areas. Under 80 words.",
    "search":       "You are the Search Agent. Find 3 specific products with exact model names, key specs, and prices in INR. Be realistic and specific. Under 100 words.",
    "price":        "You are the Price Analyst. Give budget/mid-range/premium price ranges in INR, best platforms to buy from (Amazon, Flipkart, etc). Under 90 words.",
    "review":       "You are the Review Agent. Give 3 common pros and 2 common cons based on typical user reviews. Be specific. Under 90 words.",
    "compare":      "You are the Comparison Agent. Compare top 3 options on Performance, Value for money, and Build quality. Plain text format. Under 100 words.",
    "recommender":  "You are the Recommender Agent. Give ONE specific product: exact model, best price in INR, where to buy, 2 key reasons. End with 'Confidence: XX%'. Under 100 words.",
}

class QueryRequest(BaseModel):
    query: str

def run_agent(agent_id: str, query: str, context: str) -> str:
    user_messages = {
        "orchestrator": f'Shopping query: "{query}"',
        "search":       f'Find products for: "{query}"',
        "price":        f'Products found: {context[:400]}\nQuery: "{query}"',
        "review":       f'Products context: {context[:400]}\nQuery: "{query}"',
        "compare":      f'All data: {context[:600]}\nQuery: "{query}"',
        "recommender":  f'All agent findings: {context[:800]}\nUser wants: "{query}"',
    }

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPTS[agent_id],
        messages=[{"role": "user", "content": user_messages[agent_id]}]
    )
    return message.content[0].text

@app.get("/")
def root():
    return {"status": "AI Multi-Agent Shopping System is running!"}

@app.post("/analyze")
def analyze(request: QueryRequest):
    results = {}
    context = ""

    for agent in AGENTS:
        try:
            output = run_agent(agent["id"], request.query, context)
            results[agent["id"]] = {"status": "done", "output": output}
            context += f'\n[{agent["name"]}]: {output}'
        except Exception as e:
            results[agent["id"]] = {"status": "error", "output": str(e)}

    return {"results": results}
