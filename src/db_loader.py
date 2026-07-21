import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
DB_PATH = os.path.join(BASE_DIR, 'data_game.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')
INDEXES_PATH = os.path.join(BASE_DIR, 'database', 'indexes.sql')
ADV_QUERIES_PATH = os.path.join(BASE_DIR, 'database', 'advanced_queries.sql')

def run_db_loader():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Execute DDL Schema
    print("Executing DDL Schema (database/schema.sql)...")
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()

    # 2. Ingest CSV Files
    csv_files = [
        'customers.csv', 'products.csv', 'orders.csv', 
        'warehouse_operations.csv', 'inventory.csv', 'delivery.csv', 
        'transactions.csv', 'customer_support.csv', 
        'marketing_campaign.csv', 'reviews.csv'
    ]

    print("\nIngesting raw CSV files into database tables...")
    for csv_file in csv_files:
        table_name = csv_file.replace('.csv', '')
        file_path = os.path.join(DATA_RAW_DIR, csv_file)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # Append data to table
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f" Loaded {len(df):>6} rows into table '{table_name}'")
        else:
            print(f" WARNING: File {csv_file} not found!")

    # 3. Apply Indexing Strategy
    print("\nApplying Indexing Strategy (database/indexes.sql)...")
    with open(INDEXES_PATH, 'r') as f:
        indexes_sql = f.read()
    cursor.executescript(indexes_sql)
    conn.commit()

    # 4. Create Analytical SQL Views
    print("\nCreating Advanced Analytical SQL Views (database/advanced_queries.sql)...")
    with open(ADV_QUERIES_PATH, 'r') as f:
        adv_sql = f.read()
    cursor.executescript(adv_sql)
    conn.commit()

    print("\nDatabase initialization complete! Database ready for SQL queries and analytics.")
    conn.close()

if __name__ == '__main__':
    run_db_loader()
