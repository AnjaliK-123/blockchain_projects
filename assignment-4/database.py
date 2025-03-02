import sqlite3
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def bitcoin_rpc_call(method, params):
    rpc_user = os.getenv("RPC_USER")
    rpc_password = os.getenv("RPC_PASSWORD")
    rpc_url = os.getenv("RPC_URL")

    data = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 1
    }

    response = requests.post(rpc_url, json=data, auth=(rpc_user, rpc_password))
    return response.json()


def create_database():
    conn = sqlite3.connect('bitcoin_data.db')
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

def insert_data_into_db():
    conn = sqlite3.connect('bitcoin_data.db')
    cursor = conn.cursor()
    best_block_hash_response = bitcoin_rpc_call("getbestblockhash", [])
    best_block_hash = best_block_hash_response['result']
    latest_block_response = bitcoin_rpc_call("getblock", [best_block_hash, 2])
    latest_block_value = latest_block_response['result']
    transactions = latest_block_value.get('tx', [])

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

            cursor.execute('''
            INSERT OR REPLACE INTO transactions (txid, hash, version, size, vsize, weight, locktime, vin, vout, fee, hex)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (txid, hash_value, version, size, vsize, weight, locktime, vin, vout, fee, hex_value))

    conn.commit()
    conn.close()

create_database()
insert_data_into_db()