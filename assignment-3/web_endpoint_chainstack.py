import requests
from requests.auth import HTTPBasicAuth

# RPC URL and credentials 
RPC_URL = "https://bitcoin-mainnet.core.chainstack.com" 
USERNAME = "suspicious-fermi" 
PASSWORD = "spew-slit-curly-even-unify-grunge"

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


# Function to get the current block count
def get_block_count():
    response = bitcoin_rpc_call("getblockcount", [])
    if 'error' in response and response['error']:
        print("Error fetching block count:", response['error'])
        return None
    return response['result']

    
# Function to get the blockchain information
def get_blockchain_info():
    response = bitcoin_rpc_call("getblockchaininfo", [])
    if 'error' in response and response['error']:
        print("Error fetching blockchain info:", response['error'])
        return None
    return response['result']  

if __name__ == "__main__":
    # Fetch and print the current block count
    block_count = get_block_count()
    print("Current Block Count:", block_count)

    # Fetch and print blockchain info
    blockchain_info = get_blockchain_info()
    print("Blockchain Info:", blockchain_info)