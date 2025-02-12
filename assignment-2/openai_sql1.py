from openai import OpenAI

def generate_sql_query(api_key):
    client = OpenAI(api_key=api_key)
# defined models
    OPENAI_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo-preview"
    ]
# defined prompt
    prompt = """
    You are an expert SQL query generator specialized in blockchain data analysis.

    Database Schema:
    CREATE TABLE blocks (
        id SERIAL PRIMARY KEY,
        block_number INT,
        transactions_count INT
    );

    Specific Task: Generate a SQL query to count the number of blocks in the blockchain.
    """
# chat completion request
    for model in OPENAI_MODELS:

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert SQL query generator for blockchain data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50 
            )
            

            sql_query = response.choices[0].message.content.strip()
            return sql_query 


# Main execution
if __name__ == "__main__":

    API_KEY = "sk-svcacct-eEkvPft3X6NtmgSt_IRJeFlRpuE9D-kVxwg0x3pzS9Lym7InULk2H6XEAVxl4O9E3p6l8pRovXVwCgsKT3BlbkFJsH6qyJd09aIquFAm4bQqS-x5d3orV2tGIwLKZw3Y10BhbiW5J5M32qG7dJKyJc2Hpc4AFVLl2DWaw_EA"
    
    result = generate_sql_query(API_KEY)
    
    print("\nSQL Query Generation Result:")
    print(result)