import requests
import rich
from agents import Agent, Runner, function_tool
from connection import config

# ----------------------------
# Tool: Get Products
# ----------------------------
@function_tool
def get_products():
    """
    Get product list from template6-six API.
    """
    url = "https://template6-six.vercel.app/api/products"
    try:
        res = requests.get(url)
        res.raise_for_status()
        products = res.json()

        # simple info return
        return [
            {
                "title": p.get("title"),
                "price": p.get("price"),
                "discount": p.get("discountPercentage"),
                "category": ", ".join(p.get("tags", [])),
            }
            for p in products
        ]
    except Exception as e:
        return {"error": str(e)}

# ----------------------------
# Agent
# ----------------------------
shopping_agent = Agent(
    name="Shopping Agent",
    instructions="You are a helpful shopping assistant. Use get_products to suggest items.",
    tools=[get_products],
)

# ----------------------------
# Example Queries
# ----------------------------
queries = [
    "Show me all products.",
    "Which products are new?",
    "Suggest something for home decor.",
    "Any budget-friendly chairs?",
]
# "Show me all products in the store."

# "Which products are new arrivals?"

# "Can you recommend something under 200?"

# "What are the best discounts available right now?"

# "Suggest me a stylish chair."

# "Do you have anything for home decoration?"

# "Show me cozy furniture for living room."

# "Which products are good for birthday gifts?"

# "What electronic items are available?"

# "Suggest me something modern and elegant."
# ----------------------------
# Run Agent
# ----------------------------
for q in queries:
    rich.print(f"\n[b cyan]🧑 User:[/b cyan] {q}")
    result = Runner.run_sync(
        shopping_agent,
        input=q,
        run_config=config
    )
    rich.print(f"[yellow]🤖 Agent:[/yellow] {result.final_output}")
