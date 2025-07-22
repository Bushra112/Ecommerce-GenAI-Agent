import pandas as pd
import sqlite3

# Connect to a new SQLite database (will create if it doesn't exist)
conn = sqlite3.connect("C:/Users/BUSHRA/Ecommerce-GenAI-Agent/ecommerce.db")
cursor = conn.cursor()

# Load Excel files
ad_sales = pd.read_excel("C:/Users/BUSHRA/Ecommerce-GenAI-Agent/data/Product-Level Ad Sales and Metrics (mapped).xlsx")
total_sales = pd.read_excel("C:/Users/BUSHRA/Ecommerce-GenAI-Agent/data/Product-Level Total Sales and Metrics (mapped).xlsx")
eligibility = pd.read_excel("C:/Users/BUSHRA/Ecommerce-GenAI-Agent/data/Product-Level Eligibility Table (mapped).xlsx")

# Store as SQL tables
ad_sales.to_sql("ad_sales", conn, if_exists="replace", index=False)
total_sales.to_sql("total_sales", conn, if_exists="replace", index=False)
eligibility.to_sql("eligibility", conn, if_exists="replace", index=False)

print("Excel files loaded into ecommerce.db successfully!")

# Print first 3 rows from each table to confirm
for table in ["ad_sales", "total_sales", "eligibility"]:
    print(f"/nPreview from table: {table}")
    for row in cursor.execute(f"SELECT * FROM {table} LIMIT 3"):
        print(row)

conn.close()
