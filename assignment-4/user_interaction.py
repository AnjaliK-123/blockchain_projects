import sqlite3
import os
import openai
from dotenv import load_dotenv


load_dotenv() # load .env

openai.api_key = os.getenv("API_KEY")

def get_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Retrieve tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema = ""
    for table in tables:
        table_name = table[0]
        schema += f"Table: {table_name}\n"
        cursor.execute(f"PRAGMA table_info({table_name});") # Retrieve columns
        columns = cursor.fetchall()
        for column in columns:
            schema += f"  Column: {column[1]}, Type: {column[2]}\n"  # Adjusted to include column details
    conn.close()
    return schema

def generate_sql_from_natural_language(question, db_path):
    schema = get_schema(db_path)
    prompt = f"""
    You are a SQL developer that is expert in Bitcoin and you answer natural language questions about the bitcoind database in a sqlite database. You always only respond with SQL statements that are correct.
    
    Schema:
    {schema}
    
    Question: {question}
    SQL Statement:
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    
    sql_query = response.choices[0].message['content'].strip()
    return sql_query

def execute_query(db_path, sql_query):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    question = input("Enter your natural language question: ")
    db_path = input("Enter the absolute path to the SQLite database: ")
    
    sql_query = generate_sql_from_natural_language(question, db_path)
    print(f"Generated SQL Query: {sql_query}")
    
    results = execute_query(db_path, sql_query)
    print(f"Results: {results}")