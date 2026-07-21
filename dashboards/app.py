import os
import sqlite3
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import plotly.express as px
import plotly.graph_objects as gg
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Data_Game | Enterprise Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data_game.db')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

@st.cache_data
def load_data():
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

# Load Data
orders, customers, products, wh_ops, delivery, transactions, support = load_data()

# Custom CSS for Executive Dashboard Theme
st.markdown("""
<style>
    .main-header { font-size: 2.3rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.1rem; color: #64748B; margin-bottom: 1.5rem; }
    .kpi-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.2rem; text-align: center; }
    .kpi-title { font-size: 0.9rem; color: #64748B; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #0F172A; }
</style>
""", unsafe_allow_html=True)

# Title Banner
st.markdown('<div class="main-header">🎯 Enterprise Analytics & Risk Optimization Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Executive Dashboard for E-Commerce Intelligence, Operations & Risk Management | Data_Game</div>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/analytics.png", width=70)
st.sidebar.title("Data_Game Navigation")
navigation = st.sidebar.radio(
    "Select Business Domain",
    [
        "📈 Executive Overview",
        "👥 Customer Analytics & RFM",
        "🔮 Predictive ML (Churn & Forecast)",
        "🚚 Operations & Logistics SLA",
        "🛡️ Fraud Risk Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Change parameters in the sidebar to dynamically re-filter all metrics and Plotly visualizations in real-time.")

# ---------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# ---------------------------------------------------------
if navigation == "📈 Executive Overview":
    st.header("Executive Performance Summary")
    
    # Calculate Core KPIs
    valid_orders = orders[~orders['order_status'].isin(['Cancelled', 'Refunded'])]
    total_revenue = valid_orders['sales_amount'].sum()
    total_orders_cnt = len(valid_orders)
    avg_order_val = total_revenue / total_orders_cnt if total_orders_cnt > 0 else 0
    total_cust = len(customers)
    
    # Display KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Gross Revenue</div><div class="kpi-value">${total_revenue:,.2f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Orders</div><div class="kpi-value">{total_orders_cnt:,}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Avg Order Value (AOV)</div><div class="kpi-value">${avg_order_val:,.2f}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Customers</div><div class="kpi-value">{total_cust:,}</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations: Revenue Trend & Category Breakdown
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        st.subheader("Monthly Revenue Trend")
        orders['order_month'] = pd.to_datetime(orders['order_date']).dt.to_period('M').astype(str)
        monthly_rev = orders[~orders['order_status'].isin(['Cancelled', 'Refunded'])].groupby('order_month')['sales_amount'].sum().reset_index()
        fig_trend = px.line(monthly_rev, x='order_month', y='sales_amount', labels={'sales_amount': 'Revenue ($)', 'order_month': 'Month'}, markers=True, color_discrete_sequence=['#2563EB'])
        fig_trend.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        st.subheader("Revenue by Category")
        orders_prod = orders.merge(products, on='product_id')
        cat_rev = orders_prod.groupby('category')['sales_amount'].sum().reset_index().sort_values(by='sales_amount', ascending=False)
        fig_cat = px.bar(cat_rev, x='sales_amount', y='category', orientation='h', color='sales_amount', color_continuous_scale='Viridis')
        fig_cat.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_cat, use_container_width=True)


# ---------------------------------------------------------
# TAB 2: CUSTOMER ANALYTICS & RFM
# ---------------------------------------------------------
elif navigation == "👥 Customer Analytics & RFM":
    st.header("Customer Analytics & RFM Segmentation")
    
    rfm_file = os.path.join(PROCESSED_DIR, 'rfm_segmented_customers.csv')
    if os.path.exists(rfm_file):
        rfm_df = pd.read_csv(rfm_file)
        
        col1, col2 = st.columns([5, 5])
        with col1:
            st.subheader("Customer Segment Distribution")
            seg_counts = rfm_df['rfm_segment'].value_counts().reset_index()
            seg_counts.columns = ['Segment', 'Customer Count']
            fig_pie = px.pie(seg_counts, names='Segment', values='Customer Count', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(height=380)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.subheader("Monetary vs Recency by Segment")
            fig_scatter = px.scatter(rfm_df, x='recency', y='monetary', color='rfm_segment', size='frequency', hover_data=['customer_id'], labels={'recency': 'Recency (Days)', 'monetary': 'Monetary Value ($)'})
            fig_scatter.update_layout(height=380)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        st.subheader("Segment Data Inspector")
        selected_seg = st.selectbox("Filter Segment:", ['All'] + list(rfm_df['rfm_segment'].unique()))
        if selected_seg != 'All':
            st.dataframe(rfm_df[rfm_df['rfm_segment'] == selected_seg].head(50), use_container_width=True)
        else:
            st.dataframe(rfm_df.head(50), use_container_width=True)
    else:
        st.warning("RFM Segmentation data not generated yet. Run `python src/rfm_segmentation.py` first!")


# ---------------------------------------------------------
# TAB 3: PREDICTIVE ML (CHURN & FORECAST)
# ---------------------------------------------------------
elif navigation == "🔮 Predictive ML (Churn & Forecast)":
    st.header("Predictive Analytics: Customer Churn & 6-Month Sales Forecast")
    
    tab_churn, tab_forecast = st.tabs(["⚡ Churn Machine Learning Model", "📈 6-Month Revenue Forecast"])
    
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
                st.metric("Average Churn Rate Probability", f"{avg_prob*100:.1f}%")
            with c3:
                at_risk_spend = churn_df[churn_df['churn_risk_level'] == 'High']['total_spent'].sum()
                st.metric("Revenue at Risk", f"${at_risk_spend:,.2f}")
                
            fig_hist = px.histogram(churn_df, x='churn_probability', color='churn_risk_level', nbins=30, title="Churn Risk Score Distribution")
            st.plotly_chart(fig_hist, use_container_width=True)
            
            st.subheader("Top High-Risk Churn Candidates for Retargeting")
            st.dataframe(churn_df[churn_df['churn_risk_level'] == 'High'][['customer_id', 'total_orders', 'total_spent', 'days_since_last_order', 'avg_satisfaction', 'churn_probability']].sort_values(by='churn_probability', ascending=False).head(20), use_container_width=True)
        else:
            st.info("Run `python src/churn_model.py` to generate ML predictions!")
            
    with tab_forecast:
        forecast_file = os.path.join(PROCESSED_DIR, 'sales_forecast.csv')
        if os.path.exists(forecast_file):
            fc_df = pd.read_csv(forecast_file)
            fig_fc = px.line(fc_df, x='forecast_month', y='projected_revenue', color='type', markers=True, title="Historical vs 6-Month Projected Revenue Forecast ($)")
            st.plotly_chart(fig_fc, use_container_width=True)
        else:
            st.info("Run `python src/sales_forecasting.py` to generate forecast!")


# ---------------------------------------------------------
# TAB 4: OPERATIONS & LOGISTICS SLA
# ---------------------------------------------------------
elif navigation == "🚚 Operations & Logistics SLA":
    st.header("Operations & Logistics SLA Optimization")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Warehouse Capacity & Utilization")
        fig_wh = px.bar(wh_ops, x='warehouse_name', y='utilization_rate', color='utilization_rate', color_continuous_scale='Reds', title="Warehouse Utilization Rate (%)")
        st.plotly_chart(fig_wh, use_container_width=True)
        
    with c2:
        st.subheader("Courier Partner Delay Breakdown")
        del_courier = delivery.groupby(['courier_partner', 'delivery_status']).size().reset_index(name='count')
        fig_courier = px.bar(del_courier, x='courier_partner', y='count', color='delivery_status', barmode='stack', title="Delivery Status by Courier Partner")
        st.plotly_chart(fig_courier, use_container_width=True)


# ---------------------------------------------------------
# TAB 5: FRAUD RISK ANALYTICS
# ---------------------------------------------------------
elif navigation == "🛡️ Fraud Risk Analytics":
    st.header("Transaction Fraud & Anomaly Risk Dashboard")
    
    fraud_file = os.path.join(PROCESSED_DIR, 'fraud_risk_scored_transactions.csv')
    if os.path.exists(fraud_file):
        fraud_df = pd.read_csv(fraud_file)
        
        c1, c2 = st.columns(2)
        with c1:
            high_fraud_cnt = len(fraud_df[fraud_df['risk_tier'] == 'High'])
            st.metric("High Fraud Risk Alerts", f"{high_fraud_cnt:,}")
        with c2:
            high_fraud_vol = fraud_df[fraud_df['risk_tier'] == 'High']['transaction_amount'].sum()
            st.metric("Suspicious Transaction Volume", f"${high_fraud_vol:,.2f}")
            
        fig_fraud = px.scatter(fraud_df, x='transaction_amount', y='fraud_risk_score', color='risk_tier', hover_data=['transaction_id', 'customer_id', 'payment_gateway'], title="Transaction Amount vs Fraud Risk Score")
        st.plotly_chart(fig_fraud, use_container_width=True)
        
        st.subheader("Recent Suspicious Fraud Alerts")
        st.dataframe(fraud_df[fraud_df['risk_tier'] == 'High'][['transaction_id', 'customer_id', 'transaction_amount', 'payment_gateway', 'device_type', 'location', 'fraud_risk_score']].head(25), use_container_width=True)
    else:
        st.info("Run `python src/fraud_detection.py` to generate fraud risk scores!")
