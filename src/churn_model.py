import os
import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data_game.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def train_churn_model():
    conn = sqlite3.connect(DB_PATH)
    
    query = """
    SELECT 
        c.customer_id,
        c.age,
        c.customer_type,
        c.loyalty_status,
        c.acquisition_channel,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(o.sales_amount) AS total_spent,
        AVG(o.sales_amount) AS avg_order_val,
        MAX(o.order_date) AS max_order_date,
        COUNT(DISTINCT cs.ticket_id) AS support_tickets_count,
        AVG(cs.resolution_time) AS avg_resolution_hours,
        AVG(cs.satisfaction_score) AS avg_satisfaction,
        SUM(CASE WHEN cs.refund_requested = 'Yes' THEN 1 ELSE 0 END) AS refund_tickets_count,
        AVG(r.rating) AS avg_review_rating
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.order_status NOT IN ('Cancelled', 'Refunded')
    LEFT JOIN customer_support cs ON c.customer_id = cs.customer_id
    LEFT JOIN reviews r ON c.customer_id = r.customer_id
    GROUP BY c.customer_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['total_orders'] = df['total_orders'].fillna(0)
    df['total_spent'] = df['total_spent'].fillna(0.0)
    df['avg_order_val'] = df['avg_order_val'].fillna(0.0)
    df['support_tickets_count'] = df['support_tickets_count'].fillna(0)
    df['avg_resolution_hours'] = df['avg_resolution_hours'].fillna(12.0)
    df['avg_satisfaction'] = df['avg_satisfaction'].fillna(3.5)
    df['refund_tickets_count'] = df['refund_tickets_count'].fillna(0)
    df['avg_review_rating'] = df['avg_review_rating'].fillna(3.5)
    
    snapshot_date = pd.to_datetime('2026-07-01')
    df['max_order_date'] = pd.to_datetime(df['max_order_date'])
    df['days_since_last_order'] = (snapshot_date - df['max_order_date']).dt.days.fillna(999)
    
    df['is_churned'] = np.where((df['days_since_last_order'] > 120) | (df['total_orders'] == 0), 1, 0)
    
    feature_cols = [
        'age', 'total_orders', 'total_spent', 'avg_order_val',
        'support_tickets_count', 'avg_resolution_hours', 'avg_satisfaction',
        'refund_tickets_count', 'avg_review_rating', 'days_since_last_order'
    ]
    
    X = df[feature_cols]
    y = df['is_churned']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    rf_clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    rf_clf.fit(X_train, y_train)
    
    y_pred = rf_clf.predict(X_test)
    y_prob = rf_clf.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    
    df['churn_probability'] = rf_clf.predict_proba(X)[:, 1]
    df['churn_risk_level'] = pd.cut(df['churn_probability'], bins=[-0.01, 0.3, 0.7, 1.0], labels=['Low', 'Medium', 'High'])
    
    output_path = os.path.join(PROCESSED_DIR, 'churn_predictions.csv')
    df.to_csv(output_path, index=False)
    print(f"Churn Model trained. Accuracy: {acc:.4f}, AUC: {auc:.4f}")
    return df

if __name__ == '__main__':
    train_churn_model()
