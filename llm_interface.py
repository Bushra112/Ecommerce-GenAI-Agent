import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma:2b"

def ask_llm(schema, question):
    prompt = f"""

You are a highly reliable SQLite expert assistant designed to help analyze an e-commerce database.

Your goal is to generate **only valid SQLite queries** using the schema provided below. The queries must never reference non-existent tables or columns. Focus on **accuracy, validity, and robustness**, even if the query is simple.

====================
VALID SCHEMA:
Table: ad_sales (alias: a)
- a.date (TIMESTAMP)
- a.item_id (INTEGER)
- a.ad_sales (REAL)
- a.impressions (INTEGER)
- a.ad_spend (REAL)
- a.clicks (INTEGER)
- a.units_sold (INTEGER)

Table: total_sales (alias: t)
- t.date (TIMESTAMP)
- t.item_id (INTEGER)
- t.total_sales (REAL)
- t.total_units_ordered (INTEGER)

Table: eligibility (alias: e)
- e.eligibility_datetime_utc (TIMESTAMP)
- e.item_id (INTEGER)
- e.eligibility (INTEGER)
- e.message (TEXT)
====================

🚫 DO NOT:
- Reference columns like `e.date`, `item_name`, `customer_id`, etc. — they do NOT exist.
- Use any table or alias not defined above.
- Generate DDL (CREATE, DROP, etc.) or INSERT statements — only SELECT statements are allowed.

✅ RULES:
- Always fully qualify columns with their table aliases (e.g., `a.item_id`, `t.date`, etc.).
- To join `eligibility`, use: `DATE(e.eligibility_datetime_utc) = DATE(t.date)`
- Use `JOIN` only between tables listed above.
- Use `CASE WHEN` or `WHERE` clauses to avoid division by zero. E.g., `WHERE a.clicks > 0`.
- Use `SUM()` or `ROUND()` as needed for aggregated metrics.
- Use `GROUP BY` only when required (e.g., for daily/item-level breakdowns).
- Use LIMIT to avoid overly large results when applicable.
- Keep the query simple and safe. Prioritize correctness over complexity.

Examples of derived metrics:
- CPC = `a.ad_spend * 1.0 / a.clicks` with `WHERE a.clicks > 0`
- ROAS = `SUM(t.total_sales) * 1.0 / SUM(a.ad_spend)` with check: `CASE WHEN SUM(a.ad_spend) > 0 THEN ...`
- To join total_sales and ad_sales: use both `item_id` and `date`
- To join eligibility, use: DATE(e.eligibility_datetime_utc) = DATE(t.date)
- DATE(e.eligibility_datetime_utc) = DATE(a.date)



Now, write a valid SQLite query (no markdown, no explanation) to answer this natural language question:

Question: {question}
"""


    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        raise Exception(f"Ollama Error: {response.text}")


    response_text = response.json()['response'].strip()

    # Remove markdown SQL formatting if present
    if response_text.startswith("```"):
        response_text = response_text.strip("`")  # removes all backticks
        response_text = response_text.replace("sql", "").strip()

    return response_text