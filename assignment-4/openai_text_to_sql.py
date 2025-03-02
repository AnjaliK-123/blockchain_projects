import openai
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

# retrieve rpc credentials 
RPC_URL = os.getenv('RPC_URL')
USERNAME = os.getenv('RPC_USER')
PASSWORD = os.getenv('RPC_PASSWORD')

# RPC call
def bitcoin_rpc_call(method, params):
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }
    response = requests.post(RPC_URL, json=data, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    return response.json()

# Generate schema from RPC call
def generate_sql_schema(api_key):
    openai.api_key = api_key
    

    best_block_hash_response = bitcoin_rpc_call("getbestblockhash", [])
    best_block_hash = best_block_hash_response['result']
    

    latest_block_response = bitcoin_rpc_call("getblock", [best_block_hash, 2])  # Verbosity level 2
    latest_block_value = latest_block_response['result']

    transactions = latest_block_value.get('tx', [])
    
    limited_transactions = transactions[:1] # limit transaction to 1

    verbosity2_json_object = {
        "tx": limited_transactions,
        "tx_count": len(limited_transactions)
    }

    # Define models
    OPENAI_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo-preview"
    ]

    # Define prompt for OpenAI
    prompt = f"""
    You are a Python developer with expertise in SQLite databases and working with JSON data. I need you to generate Python code that accomplishes the following tasks:

    Write code to make an RPC call (get rpc credentials from .env file) to retrieve the latest blocks from the Bitcoin network using the getblock method with verbosity=2.
    Parse the returned JSON object to extract the necessary data for database operations.
    Connect to a SQLite database named bitcoin.db.
    Sample create table function -
    def create_database():
        conn = sqlite3.connect('bitcoin.db')
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS transactions;')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            txid TEXT PRIMARY KEY,
            hash TEXT,
            version INTEGER,
            size INTEGER,
            vsize INTEGER,
            weight INTEGER,
            locktime INTEGER,
            vin TEXT,
            vout TEXT,
            fee REAL,
            hex TEXT,
            sequence INTEGER
        );
        ''')

        conn.commit()
        conn.close()

    Sample insert table function - 
    def insert_data_into_db():
        conn = sqlite3.connect('bitcoin.db')
        cursor = conn.cursor()
        best_block_hash_response = bitcoin_rpc_call("getbestblockhash", [])
        best_block_hash = best_block_hash_response['result']
        latest_block_response = bitcoin_rpc_call("getblock", [best_block_hash, 2])  # Verbosity level 2
        latest_block_value = latest_block_response['result']
        transactions = latest_block_value.get('tx', [])
        print(transactions)

        for transaction in transactions:
            if isinstance(transaction, dict):
                txid = transaction.get('txid')
                hash_value = transaction.get('hash')
                version = transaction.get('version')
                size = transaction.get('size')
                vsize = transaction.get('vsize')
                weight = transaction.get('weight')
                locktime = transaction.get('locktime')
                vin = json.dumps(transaction.get('vin'))
                vout = json.dumps(transaction.get('vout'))
                fee = transaction.get('fee')
                hex_value = transaction.get('hex')


    # Insert transaction into the database
    cursor.execute('''
    INSERT OR REPLACE INTO transactions (txid, hash, version, size, vsize, weight, locktime, vin, vout, fee, hex)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (txid, hash_value, version, size, vsize, weight, locktime, vin, vout, fee, hex_value))


    Insert the data into these tables using the JSON object received from the RPC call. The structure of the JSON object is as follows:
    {verbosity2_json_object}

    Please provide the complete Python code that accomplishes these tasks.
    """

    # Chat completion request
    for model in OPENAI_MODELS:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Python developer with expertise in SQLite databases and working with JSON data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000 
        )
        
        sql_schema = response.choices[0].message.content.strip()
        clean_sql_schema = sql_schema.replace("```sql", "").replace("```", "").strip()
        return clean_sql_schema 


if __name__ == "__main__":
    result = generate_sql_schema(os.getenv('API_KEY'))
    print(result)