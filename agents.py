import anthropic
import streamlit as st

MODEL = "claude-sonnet-4-20250514"


def get_client():
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        api_key = None
    return anthropic.Anthropic(api_key=api_key)


def call_claude(system_prompt: str, user_message: str, max_tokens: int = 600) -> str:
    client = get_client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def orchestrator_agent(query: str) -> str:
    system = """You are the Orchestrator Agent in an AI Multi-Agent Shopping System.
Analyze the shopping query and create a brief strategy plan.
List 4 key tasks for other agents. Be concise. Under 80 words."""
    return call_claude(system, f'Shopping query: "{query}"')


def search_agent(query: str) -> str:
    system = """You are the Search Agent. Find 3 specific products with exact model names,
key specs, and prices in INR. Be realistic and specific. Under 100 words."""
    return call_claude(system, f'Find products for: "{query}"')


def price_agent(query: str, search_result: str) -> str:
    system = """You are the Price Analyst Agent. Give budget/mid-range/premium price ranges in INR,
best platforms to buy (Amazon, Flipkart, etc), and any deals. Under 90 words."""
    return call_claude(system, f'Products: {search_result[:400]}\nQuery: "{query}"')


def review_agent(query: str, search_result: str) -> str:
    system = """You are the Review Agent. Give 3 common pros and 2 common cons from
typical customer reviews for these products. Be specific. Under 90 words."""
    return call_claude(system, f'Products: {search_result[:400]}\nQuery: "{query}"')


def comparison_agent(query: str, accumulated: str) -> str:
    system = """You are the Comparison Agent. Compare top 3 products on Performance,
Value for money, and Build quality. Plain text format. Under 100 words."""
    return call_claude(system, f'All data: {accumulated[:600]}\nQuery: "{query}"')


def recommender_agent(query: str, accumulated: str) -> str:
    system = """You are the Final Recommender Agent. Give ONE specific product recommendation:
exact model name, best price in INR, top platform to buy, and 2 key reasons.
End with 'Confidence: XX%'. Under 100 words."""
    return call_claude(system, f'All agent findings: {accumulated[:800]}\nUser wants: "{query}"')
