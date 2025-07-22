import sqlite3

def get_schema(db_path):
    """Reads the schema of the database and returns a string."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = ""
    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema += f"Table: {table_name}\n"
        for col in columns:
            schema += f" - {col[1]} ({col[2]})\n"
        schema += "\n"

    conn.close()
    return schema.strip()

def execute_query(db_path, sql_query):
    """Executes a SQL query and returns the results or an error."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # ✅ Enable row-to-dict mapping
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]  # ✅ Convert rows to dicts
        conn.close()
        return result
    except Exception as e:
        return str(e)
