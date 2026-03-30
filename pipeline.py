import pandas as pd
import json
import duckdb
import os

with open('data/bronze/raw_scrape.json', 'r') as f:
    bronze = json.load(f)

df = pd.DataFrame(bronze)

df['name'] = df['name'].str.strip()
df = df.drop_duplicates(subset=['site', 'name'])
df = df[df['name'].notna() & (df['name'] != '')]

os.makedirs('data/silver', exist_ok=True)
df.to_csv('data/silver/cleaned_data.csv', index=False)

gold = df.groupby('site').size().reset_index(name='product_count')
os.makedirs('data/gold', exist_ok=True)
gold.to_csv('data/gold/aggregated_metrics.csv', index=False)

conn = duckdb.connect('data/cfdb.duckdb')
conn.execute("CREATE OR REPLACE TABLE silver AS SELECT * FROM df")
conn.execute("CREATE OR REPLACE TABLE gold AS SELECT * FROM gold")
conn.close()

print("Pipeline completed successfully")
print(f"Silver: {len(df)} rows saved to data/silver/cleaned_data.csv")
print(f"Gold: {len(gold)} rows saved to data/gold/aggregated_metrics.csv")
