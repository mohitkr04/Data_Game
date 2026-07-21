import os
import sqlite3
import pandas as pd
import numpy as np
from statsmodels.tsa.api import ExponentialSmoothing

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data_game.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def run_sales_forecasting():
    print("--------------------------------------------------")
    print("Executing 6-Month Revenue & Sales Forecasting Engine...")
    print("--------------------------------------------------")
    
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        STRFTIME('%Y-%m', order_date) AS order_month,
        SUM(sales_amount) AS monthly_revenue,
        COUNT(DISTINCT order_id) AS monthly_orders
    FROM orders
    WHERE order_status NOT IN ('Cancelled', 'Refunded')
    GROUP BY 1
    ORDER BY 1 ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['order_month'] = pd.to_datetime(df['order_month'] + '-01')
    df.set_index('order_month', inplace=True)
    
    print(f"Loaded {len(df)} historical monthly time-series records.")
    print("Historical Monthly Revenue Summary:")
    print(df.tail(6))
    
    # Fit Holt-Winters Exponential Smoothing Model
    model = ExponentialSmoothing(
        df['monthly_revenue'], 
        trend='add', 
        seasonal=None, 
        initialization_method='estimated'
    )
    fit_model = model.fit()
    
    # Forecast next 6 months
    forecast_steps = 6
    future_dates = pd.date_range(start=df.index[-1] + pd.DateOffset(months=1), periods=forecast_steps, freq='MS')
    forecast_values = fit_model.forecast(forecast_steps)
    
    forecast_df = pd.DataFrame({
        'forecast_month': future_dates.strftime('%Y-%m'),
        'projected_revenue': np.round(forecast_values, 2),
        'type': '6-Month Forecast'
    })
    
    hist_df = pd.DataFrame({
        'forecast_month': df.index.strftime('%Y-%m'),
        'projected_revenue': np.round(df['monthly_revenue'].values, 2),
        'type': 'Historical'
    })
    
    combined_forecast = pd.concat([hist_df, forecast_df], ignore_index=True)
    
    print("\n--- 6-Month Projected Revenue Forecast ---")
    print(forecast_df)
    
    output_path = os.path.join(PROCESSED_DIR, 'sales_forecast.csv')
    combined_forecast.to_csv(output_path, index=False)
    print(f"\nExported 6-Month Sales Forecast to '{output_path}'")
    return combined_forecast

if __name__ == '__main__':
    run_sales_forecasting()
