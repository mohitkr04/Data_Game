import os
import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data_game.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

def run_rfm_segmentation():
    print("--------------------------------------------------")
    print("Starting RFM & K-Means Customer Segmentation...")
    print("--------------------------------------------------")
    
    conn = sqlite3.connect(DB_PATH)
    
    # Query customer order aggregations
    query = """
    SELECT 
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(order_id) AS frequency,
        SUM(sales_amount) AS monetary
    FROM orders
    WHERE order_status NOT IN ('Cancelled', 'Refunded')
    GROUP BY customer_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Calculate Recency in days relative to snapshot date '2026-07-01'
    df['last_order_date'] = pd.to_datetime(df['last_order_date'])
    snapshot_date = pd.to_datetime('2026-07-01')
    df['recency'] = (snapshot_date - df['last_order_date']).dt.days
    
    print(f"Loaded {len(df)} customer records for RFM analysis.")
    print("RFM Summary Stats:")
    print(df[['recency', 'frequency', 'monetary']].describe())
    
    # 1. Rule-Based RFM Scoring (1 to 5 scale)
    df['r_score'] = pd.qcut(df['recency'], 5, labels=[5, 4, 3, 2, 1])
    df['f_score'] = pd.qcut(df['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    df['m_score'] = pd.qcut(df['monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    
    df['r_score'] = df['r_score'].astype(int)
    df['f_score'] = df['f_score'].astype(int)
    df['m_score'] = df['m_score'].astype(int)
    df['rfm_combined'] = df['r_score'].astype(str) + df['f_score'].astype(str) + df['m_score'].astype(str)
    
    # Segment Assignment Strategy
    def assign_segment(row):
        r, f, m = row['r_score'], row['f_score'], row['m_score']
        if r >= 4 and f >= 4 and m >= 4:
            return 'VIP Champions'
        elif r >= 3 and f >= 3:
            return 'Loyal Customers'
        elif r >= 4 and f <= 2:
            return 'New / Recent Customers'
        elif r <= 2 and f >= 3:
            return 'At-Risk High Value'
        else:
            return 'Hibernating / Lost'
            
    df['rfm_segment'] = df.apply(assign_segment, axis=1)
    
    # 2. Machine Learning: K-Means Clustering
    X = df[['recency', 'frequency', 'monetary']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Optimal clusters with Silhouette Score
    best_k = 4
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    df['kmeans_cluster'] = kmeans.fit_predict(X_scaled)
    sil_score = silhouette_score(X_scaled, df['kmeans_cluster'])
    print(f"\nK-Means Clustering Completed (k={best_k}). Silhouette Score: {sil_score:.4f}")
    
    # Export results
    output_path = os.path.join(PROCESSED_DIR, 'rfm_segmented_customers.csv')
    df.to_csv(output_path, index=False)
    print(f"Exported segmented customers to '{output_path}'")
    
    # Print Segment Breakdown
    print("\nCustomer Segment Distribution:")
    print(df['rfm_segment'].value_counts())
    return df

if __name__ == '__main__':
    run_rfm_segmentation()
