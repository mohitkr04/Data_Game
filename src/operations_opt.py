import os
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data_game.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def run_operations_optimization():
    print("--------------------------------------------------")
    print("Executing Operations & Logistics Optimization Engine...")
    print("--------------------------------------------------")
    
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Courier Delivery SLA & Delay Root Cause Analysis
    courier_query = """
    SELECT 
        d.courier_partner,
        COUNT(d.order_id) AS total_deliveries,
        SUM(CASE WHEN d.delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_count,
        ROUND(SUM(CASE WHEN d.delivery_status = 'Delayed' THEN 1 ELSE 0 END) * 100.0 / COUNT(d.order_id), 2) AS delay_rate_pct,
        d.delay_reason
    FROM delivery d
    GROUP BY d.courier_partner, d.delay_reason
    ORDER BY delay_rate_pct DESC
    """
    courier_df = pd.read_sql_query(courier_query, conn)
    
    # 2. Warehouse Efficiency & Utilization Analysis
    wh_query = """
    SELECT 
        w.warehouse_id,
        w.warehouse_name,
        w.employee_count,
        w.daily_capacity,
        w.processing_time,
        w.utilization_rate,
        COUNT(d.order_id) AS processed_orders_count
    FROM warehouse_operations w
    LEFT JOIN delivery d ON w.warehouse_id = d.warehouse_id
    GROUP BY w.warehouse_id, w.warehouse_name, w.employee_count, w.daily_capacity, w.processing_time, w.utilization_rate
    """
    wh_df = pd.read_sql_query(wh_query, conn)
    
    # 3. Inventory Stock-out Risk & Reorder Optimization
    inv_query = """
    SELECT 
        i.product_id,
        p.category,
        p.sub_category,
        i.warehouse_id,
        i.stock_available,
        i.stock_reserved,
        i.reorder_level,
        i.inventory_cost,
        CASE 
            WHEN i.stock_available <= i.reorder_level THEN 'CRITICAL REORDER'
            WHEN i.stock_available <= (i.reorder_level * 1.5) THEN 'WARNING LOW STOCK'
            ELSE 'HEALTHY'
        END AS stock_status
    FROM inventory i
    JOIN products p ON i.product_id = p.product_id
    """
    inv_df = pd.read_sql_query(inv_query, conn)
    conn.close()
    
    print("\n--- Warehouse Efficiency Highlights ---")
    print(wh_df[['warehouse_name', 'employee_count', 'processing_time', 'utilization_rate']])
    
    print("\n--- Inventory Reorder Alerts Breakdown ---")
    print(inv_df['stock_status'].value_counts())
    
    # Export Operational Reports
    courier_df.to_csv(os.path.join(PROCESSED_DIR, 'courier_sla_analysis.csv'), index=False)
    wh_df.to_csv(os.path.join(PROCESSED_DIR, 'warehouse_efficiency.csv'), index=False)
    inv_df.to_csv(os.path.join(PROCESSED_DIR, 'inventory_reorder_alerts.csv'), index=False)
    
    print(f"\nExported Operational Optimization reports to '{PROCESSED_DIR}'")
    return wh_df, courier_df, inv_df

if __name__ == '__main__':
    run_operations_optimization()
