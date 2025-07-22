from llm_interface import ask_llm
from database import get_schema, execute_query

def main():
    db_path = "C:/Users/BUSHRA/Ecommerce-GenAI-Agent/ecommerce.db"  # Your SQLite database file
    schema = get_schema(db_path)
    print("\n🔍 Database Schema:\n")
    print(schema)

    print("Schema loaded. Ask a question (type 'exit' to quit):\n")

    while True:
        question = input("Ask your question: ")
        if question.lower() == 'exit':
            break

        print("\nGenerating SQL query...\n")
        sql_query = ask_llm(schema, question)


        print("✅ Generated SQL:")
        print(sql_query)
        

        # Clean LLM formatting if it includes markdown backticks
        cleaned_query = sql_query.strip("`").replace("sql", "").strip()

        print("\nExecuting query...\n")
        result = execute_query(db_path, cleaned_query)

        if isinstance(result, str):
            print("📊 Result:\nError executing SQL:", result)
        else:
            print("📊 Result:")
            if not result:
                print("No results found.")
            else:
                for row in result:
                    print(row)
        


if __name__ == "__main__":
    main()
