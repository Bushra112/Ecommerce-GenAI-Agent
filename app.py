from flask import Flask, render_template, request, jsonify
from llm_interface import ask_llm
from database import get_schema, execute_query
from visualizer import generate_line_chart, generate_bar_chart



app = Flask(__name__)

DB_PATH = "C:/Users/BUSHRA/Ecommerce-GenAI-Agent/ecommerce.db"
SCHEMA = get_schema(DB_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").strip().lower()

    try:
        if user_question in ["what is my total sales?", "total sales"]:
            query = "SELECT ROUND(SUM(total_sales), 2) AS total_sales FROM total_sales;"
            result = execute_query(DB_PATH, query)
            return jsonify({"sql": query, "result": result})

        elif "roas" in user_question:
            query = """
            SELECT ROUND(SUM(t.total_sales), 2) AS total_sales,
                   ROUND(SUM(a.ad_spend), 2) AS ad_spend,
                   ROUND(SUM(t.total_sales) * 1.0 / SUM(a.ad_spend), 2) AS roas
            FROM ad_sales a
            JOIN total_sales t ON a.item_id = t.item_id AND a.date = t.date
            JOIN eligibility e ON a.item_id = e.item_id
            WHERE DATE(e.eligibility_datetime_utc) = DATE(t.date);
            """
            result = execute_query(DB_PATH, query)
            return jsonify({"sql": query, "result": result})

        elif "highest cpc" in user_question or "max cpc" in user_question:
            query = """
            SELECT a.item_id,
                   ROUND(a.ad_spend * 1.0 / a.clicks, 2) AS cpc
            FROM ad_sales a
            WHERE a.clicks > 0
            ORDER BY cpc DESC
            LIMIT 1;
            """
            result = execute_query(DB_PATH, query)
            return jsonify({"sql": query, "result": result})

        # Else: fallback to LLM
        sql_query = ask_llm(SCHEMA, user_question)
        cleaned_query = sql_query.strip("`").replace("sql", "").strip()
        result = execute_query(DB_PATH, cleaned_query)

        return jsonify({
            "sql": cleaned_query,
            "result": result if not isinstance(result, str) else [],
            "error": result if isinstance(result, str) else None
        })
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
