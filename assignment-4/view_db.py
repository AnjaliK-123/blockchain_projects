import sqlite3
import pandas as pd


db_path = 'bitcoin_data.db'
conn = sqlite3.connect(db_path) # connect to db
query = "SELECT * FROM transactions"

# load db on pandas dataframe
df = pd.read_sql(query, conn)

conn.close()

print(df) # view db
