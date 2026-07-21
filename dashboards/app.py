import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Path configuration
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

DB_PATH = os.path.join(BASE_DIR, 'data_game.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')

def initialize_data_if_needed():
    if not os.path.exists(DB_PATH) or not os.path.exists(os.path.join(RAW_DIR, 'customers.csv')):
        with st.spinner("Loading analytical database..."):
            import data_generator
            import db_loader
            db_loader.run_db_loader()

initialize_data_if_needed()

# Page Configuration
st.set_page_config(
    page_title="Data_Game Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_dataset():
    conn = sqlite3.connect(DB_PATH)
    orders = pd.read_sql_query("SELECT * FROM orders", conn)
    customers = pd.read_sql_query("SELECT * FROM customers", conn)
    products = pd.read_sql_query("SELECT * FROM products", conn)
    wh_ops = pd.read_sql_query("SELECT * FROM warehouse_operations", conn)
    delivery = pd.read_sql_query("SELECT * FROM delivery", conn)
    transactions = pd.read_sql_query("SELECT * FROM transactions", conn)
    support = pd.read_sql_query("SELECT * FROM customer_support", conn)
    conn.close()
    return orders, customers, products, wh_ops, delivery, transactions, support

orders, customers, products, wh_ops, delivery, transactions, support = load_dataset()

# Custom Styling
st.markdown("""
<style>
    .header-title { font-size: 2.1rem; font-weight: 700; color: #1E293B; margin-bottom: 0.1rem; }
    .header-subtitle { font-size: 1.0rem; color: #64748B; margin-bottom: 1.2rem; }
    .metric-container { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 1rem; text-align: center; }
    .metric-label { font-size: 0.85rem; color: #64748B; font-weight: 600; text-transform: uppercase; }
    .metric-val { font-size: 1.7rem; font-weight: 700; color: #0F172A; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">Enterprise Analytics & Risk Optimization</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">E-Commerce Intelligence, Logistics SLA & Fraud Risk Management Dashboard</div>', unsafe_allow_html=True)

# Navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio(
    "Select View",
    [
        "Executive Summary",
        "Customer Analytics & RFM",
        "Predictive Modeling (Churn & Forecast)",
        "Operations & Logistics SLA",
        "Fraud Risk Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Data_Game Platform | Operational Analytics Suite")

# ---------------------------------------------------------
# VIEW 1: EXECUTIVE SUMMARY
# ---------------------------------------------------------
if navigation == "Executive Summary":
    st.subheader("Business Performance Metrics")
    
    valid_orders = orders[~orders['order_status'].isin(['Cancelled', 'Refunded'])].copy()
    total_revenue = valid_orders['sales_amount'].sum()
    total_orders_cnt = len(valid_orders)
    avg_order_val = total_revenue / total_orders_cnt if total_orders_cnt > 0 else 0
    total_cust = len(customers)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-container"><div class="metric-label">Gross Revenue</div><div class="metric-val">${total_revenue:,.2f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-container"><div class="metric-label">Completed Orders</div><div class="metric-val">{total_orders_cnt:,}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-container"><div class="metric-label">Average Order Value</div><div class="metric-val">${avg_order_val:,.2f}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-container"><div class="metric-label">Active Customers</div><div class="metric-val">{total_cust:,}</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        st.write("##### Monthly Revenue Trend")
        valid_orders['order_month'] = pd.to_datetime(valid_orders['order_date']).dt.to_period('M').astype(str)
        monthly_rev = valid_orders.groupby('order_month')['sales_amount'].sum().reset_index()
        fig_trend = px.line(monthly_rev, x='order_month', y='sales_amount', labels={'sales_amount': 'Revenue ($)', 'order_month': 'Month'}, markers=True, color_discrete_sequence=['#2563EB'])
        fig_trend.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        st.write("##### Revenue Breakdown by Category")
        orders_prod = valid_orders.merge(products, on='product_id')
        cat_rev = orders_prod.groupby('category')['sales_amount'].sum().reset_index().sort_values(by='sales_amount', ascending=False)
        fig_cat = px.bar(cat_rev, x='sales_amount', y='category', orientation='h', color='sales_amount', color_continuous_scale='Blues')
        fig_cat.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_cat, use_container_width=True)

# ---------------------------------------------------------
# VIEW 2: CUSTOMER ANALYTICS & RFM
# ---------------------------------------------------------
elif navigation == "Customer Analytics & RFM":
    st.subheader("Customer Segmentation & RFM Analysis")
    
    rfm_file = os.path.join(PROCESSED_DIR, 'rfm_segmented_customers.csv')
    if os.path.exists(rfm_file):
        rfm_df = pd.read_csv(rfm_file)
        
        col1, col2 = st.columns([5, 5])
        with col1:
            st.write("##### Customer Segment Distribution")
            seg_counts = rfm_df['rfm_segment'].value_counts().reset_index()
            seg_counts.columns = ['Segment', 'Count']
            fig_pie = px.pie(seg_counts, names='Segment', values='Count', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
            fig_pie.update_layout(height=360)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.write("##### Monetary vs Recency Matrix")
            fig_scatter = px.scatter(rfm_df, x='recency', y='monetary', color='rfm_segment', size='frequency', hover_data=['customer_id'], labels={'recency': 'Recency (Days)', 'monetary': 'Monetary Value ($)'})
            fig_scatter.update_layout(height=360)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        st.write("##### Segment Explorer")
        selected_seg = st.selectbox("Filter Segment:", ['All'] + list(rfm_df['rfm_segment'].unique()))
        if selected_seg != 'All':
            st.dataframe(rfm_df[rfm_df['rfm_segment'] == selected_seg].head(50), use_container_width=True)
        else:
            st.dataframe(rfm_df.head(50), use_container_width=True)

# ---------------------------------------------------------
# VIEW 3: PREDICTIVE MODELING
# ---------------------------------------------------------
elif navigation == "Predictive Modeling (Churn & Forecast)":
    st.subheader("Predictive Analytics")
    
    tab_churn, tab_forecast = st.tabs(["Churn Model", "Sales Forecast"])
    
    with tab_churn:
        churn_file = os.path.join(PROCESSED_DIR, 'churn_predictions.csv')
        if os.path.exists(churn_file):
            churn_df = pd.read_csv(churn_file)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                high_risk_cnt = len(churn_df[churn_df['churn_risk_level'] == 'High'])
                st.metric("High Churn Risk Customers", f"{high_risk_cnt:,}")
            with c2:
                avg_prob = churn_df['churn_probability'].mean()
                st.metric("Average Churn Probability", f"{avg_prob*100:.1f}%")
            with c3:
                at_risk_spend = churn_df[churn_df['churn_risk_level'] == 'High']['total_spent'].sum()
                st.metric("Annual Revenue at Risk", f"${at_risk_spend:,.2f}")
                
            fig_hist = px.histogram(churn_df, x='churn_probability', color='churn_risk_level', nbins=30, title="Churn Risk Probability Distribution")
            st.plotly_chart(fig_hist, use_container_width=True)
            
            st.write("##### High Risk Accounts")
            st.dataframe(churn_df[churn_df['churn_risk_level'] == 'High'][['customer_id', 'total_orders', 'total_spent', 'days_since_last_order', 'avg_satisfaction', 'churn_probability']].sort_values(by='churn_probability', ascending=False).head(25), use_container_width=True)
            
    with tab_forecast:
        forecast_file = os.path.join(PROCESSED_DIR, 'sales_forecast.csv')
        if os.path.exists(forecast_file):
            fc_df = pd.read_csv(forecast_file)
            fig_fc = px.line(fc_df, x='forecast_month', y='projected_revenue', color='type', markers=True, title="Revenue History & 6-Month Projection ($)")
            st.plotly_chart(fig_fc, use_container_width=True)

# ---------------------------------------------------------
# VIEW 4: OPERATIONS & LOGISTICS SLA
# ---------------------------------------------------------
elif navigation == "Operations & Logistics SLA":
    st.subheader("Logistics & SLA Optimization")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("##### Warehouse Utilization Rates (%)")
        fig_wh = px.bar(wh_ops, x='warehouse_name', y='utilization_rate', color='utilization_rate', color_continuous_scale='Reds')
        st.plotly_chart(fig_wh, use_container_width=True)
        
    with c2:
        st.write("##### Courier Partner Performance")
        del_courier = delivery.groupby(['courier_partner', 'delivery_status']).size().reset_index(name='count')
        fig_courier = px.bar(del_courier, x='courier_partner', y='count', color='delivery_status', barmode='stack')
        st.plotly_chart(fig_courier, use_container_width=True)

# ---------------------------------------------------------
# VIEW 5: FRAUD RISK ANALYTICS
# ---------------------------------------------------------
elif navigation == "Fraud Risk Analytics":
    st.subheader("Transaction Anomaly & Fraud Risk Monitoring")
    
    fraud_file = os.path.join(PROCESSED_DIR, 'fraud_risk_scored_transactions.csv')
    if os.path.exists(fraud_file):
        fraud_df = pd.read_csv(fraud_file)
        
        c1, c2 = st.columns(2)
        with c1:
            high_fraud_cnt = len(fraud_df[fraud_df['risk_tier'] == 'High'])
            st.metric("High Fraud Risk Alerts", f"{high_fraud_cnt:,}")
        with c2:
            high_fraud_vol = fraud_df[fraud_df['risk_tier'] == 'High']['transaction_amount'].sum()
            st.metric("Flagged Volume", f"${high_fraud_vol:,.2f}")
            
        fig_fraud = px.scatter(fraud_df, x='transaction_amount', y='fraud_risk_score', color='risk_tier', hover_data=['transaction_id', 'customer_id', 'payment_gateway'], title="Transaction Value vs Fraud Risk Score")
        st.plotly_chart(fig_fraud, use_container_width=True)
        
        st.write("##### Flagged Suspicious Transactions")
        st.dataframe(fraud_df[fraud_df['risk_tier'] == 'High'][['transaction_id', 'customer_id', 'transaction_amount', 'payment_gateway', 'device_type', 'location', 'fraud_risk_score']].head(25), use_container_width=True)
