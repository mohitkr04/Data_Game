import os
import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data_game.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def run_fraud_detection():
    print("--------------------------------------------------")
    print("Executing Transaction Fraud & Anomaly Risk Engine...")
    print("--------------------------------------------------")
    
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        t.transaction_id,
        t.customer_id,
        t.transaction_amount,
        t.payment_gateway,
        t.device_type,
        t.location,
        t.transaction_status,
        c.customer_type,
        c.age
    FROM transactions t
    JOIN customers c ON t.customer_id = c.customer_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print(f"Loaded {len(df)} transactions for fraud risk scoring.")
    
    # One-Hot Encoding & Feature Engineering
    df['is_flagged'] = np.where(df['transaction_status'].isin(['Flagged_Fraud', 'Chargeback']), 1, 0)
    df['is_declined'] = np.where(df['transaction_status'] == 'Declined', 1, 0)
    
    # Features for Anomaly Detection
    X_num = df[['transaction_amount', 'is_flagged', 'is_declined']].copy()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_num)
    
    # Train Isolation Forest Anomaly Detector
    iso = IsolationForest(contamination=0.04, random_state=42)
    df['anomaly_score'] = iso.fit_predict(X_scaled) # -1 for anomaly, 1 for normal
    raw_scores = iso.decision_function(X_scaled)
    
    # Convert decision function to 0 - 100 Risk Score Scale
    min_s, max_s = raw_scores.min(), raw_scores.max()
    df['fraud_risk_score'] = np.round((1 - (raw_scores - min_s) / (max_s - min_s)) * 100, 1)
    
    # Assign Risk Tier
    df['risk_tier'] = pd.cut(df['fraud_risk_score'], bins=[-1, 50, 75, 100], labels=['Low', 'Medium', 'High'])
    
    print("\nFraud Risk Tier Distribution:")
    print(df['risk_tier'].value_counts())
    
    # High-Risk Suspicious Transactions Summary
    high_risk = df[df['risk_tier'] == 'High']
    print(f"\nIdentified {len(high_risk)} HIGH RISK transactions.")
    print(high_risk[['transaction_id', 'customer_id', 'transaction_amount', 'payment_gateway', 'fraud_risk_score', 'transaction_status']].head(10))
    
    output_path = os.path.join(PROCESSED_DIR, 'fraud_risk_scored_transactions.csv')
    df.to_csv(output_path, index=False)
    print(f"\nExported Fraud Risk Scored Transactions to '{output_path}'")
    return df

if __name__ == '__main__':
    run_fraud_detection()
