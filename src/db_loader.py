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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()

    # Load raw datasets
    csv_files = [
        'customers.csv', 'products.csv', 'orders.csv', 
        'warehouse_operations.csv', 'inventory.csv', 'delivery.csv', 
        'transactions.csv', 'customer_support.csv', 
        'marketing_campaign.csv', 'reviews.csv'
    ]

    for csv_file in csv_files:
        table_name = csv_file.replace('.csv', '')
        file_path = os.path.join(DATA_RAW_DIR, csv_file)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Apply indexes and analytical views
    with open(INDEXES_PATH, 'r') as f:
        indexes_sql = f.read()
    cursor.executescript(indexes_sql)
    conn.commit()

    with open(ADV_QUERIES_PATH, 'r') as f:
        adv_sql = f.read()
    cursor.executescript(adv_sql)
    conn.commit()

    print("Database built and views created successfully.")
    conn.close()

if __name__ == '__main__':
    run_db_loader()
