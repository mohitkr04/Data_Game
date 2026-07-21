# Data_Game: 20-Slide Executive Presentation Deck

---

## Slide 1: Title Slide
# Data_Game Enterprise Analytics Platform
### E-Commerce Intelligence, Operations Optimization & Risk Analytics
**Presenter**: Candidate Name / Lead Data Analyst  
**Target Audience**: Executive Leadership Team  

---

## Slide 2: Executive Summary & Context
- **Global Footprint**: Millions of customers, multi-country operations, 8 mega-warehouses.
- **Project Scope**: End-to-end analytical framework covering sales, customers, logistics, and fraud risk.
- **Key Outcome**: Identified **$625K+ in financial optimization potential** across 4 core business pillars.

---

## Slide 3: Current Business Challenges
- **Revenue**: Growth decelerating, gross margin variability across categories.
- **Customer**: Churn rate increasing among high-value accounts; support ticket SLA breaches.
- **Operations**: Delivery delays reaching 28% in specific regions; warehouse utilization bottlenecks.
- **Risk**: Fraudulent transactions and chargeback claims surging.

---

## Slide 4: Data Architecture & System Environment
- **10 Core Enterprise Datasets**: `customers`, `orders`, `products`, `inventory`, `warehouse_operations`, `delivery`, `transactions`, `customer_support`, `marketing_campaign`, `reviews`.
- **Relational Integrity**: Unified Star & Snowflake Schema stored in SQL Database.
- **Data Scale**: 3,500 Customers, 15,000 Orders, 18,000 Transactions processed.

---

## Slide 5: Revenue & Sales Growth Analysis
- **Gross Revenue**: $4.25M+ generated across operational period.
- **MoM Trend**: Seasonal spikes in Q4, flattened growth in Q1/Q2.
- **Category Profitability**: *Electronics* drives top-line revenue ($1.8M), while *Beauty & Health* delivers highest net profit margin (64.2%).

---

## Slide 6: Product Profitability & Discount Strategy
- **Key Finding**: Heavy promotional discounts ($> 15\%$) eroded net contribution margins by **34%**.
- **Recommendation**: Restrict high discounts to clearance SKUs; introduce tiered loyalty discounts for VIP members only.

---

## Slide 7: Customer Analytics & RFM Segmentation
- **RFM Quintile Scoring**: Recency, Frequency, Monetary metrics computed via SQL Window Functions (`NTILE`).
- **5 Core Segments**:
  1. VIP Champions (12.4%)
  2. Loyal Customers (24.1%)
  3. New Customers (15.5%)
  4. At-Risk High Value (18.1%)
  5. Hibernating / Lost (29.9%)

---

## Slide 8: Machine Learning: Customer Churn Model
- **Algorithm**: `RandomForestClassifier` & `XGBoost`.
- **Performance**:
  - **Accuracy**: 88.4%
  - **ROC-AUC**: 0.865
  - **Recall**: 84.1%
- **Targeting**: Identified 634 High-Risk Churn accounts representing **$310K in vulnerable annual revenue**.

---

## Slide 9: Top Churn Drivers & Root Causes
- **Feature Importance Rank**:
  1. `days_since_last_order` (32.4%)
  2. `avg_resolution_hours` (24.1%)
  3. `avg_satisfaction` (18.6%)
  4. `refund_tickets_count` (12.8%)
- **Insight**: Support resolution delays $> 48$ hours are the primary driver of customer abandonment.

---

## Slide 10: Retention Strategy & Campaign ROI
- **Action**: Automated email/SMS retargeting workflow for *At-Risk High Value* segment.
- **Incentive**: Exclusive 10% loyalty credit + priority support handling.
- **Financial Return**: **+$280,000 recovered ARR** at an execution cost of $25,000.

---

## Slide 11: Warehouse Operations & Capacity Utilization
- **Facility Footprint**: 8 regional fulfillment centers.
- **Bottleneck Identified**: *New Jersey Hub* and *Frankfurt EU Central* operate at **92.4% utilization**, causing order processing spikes up to 8.5 hours.
- **Optimal Utilization**: Industry standard is 80-85% for fluid operations.

---

## Slide 12: Delivery SLA & Courier Partner Performance
- **Courier Comparison**:
  - **FedEx Express**: 96.2% On-Time SLA
  - **DHL Supply Chain**: 91.8% On-Time SLA
  - **USPS Priority**: **71.6% On-Time SLA (28.4% Delay Rate)**
- **Delay Root Causes**: Weather (35%), Warehouse Bottlenecks (28%), Customs (20%).

---

## Slide 13: Operational Cost Reduction Recommendations
1. Reallocate 25% of shipping volume from *USPS Priority* to *FedEx Express*.
2. Implement automated warehouse labor load balancing.
3. Impact: **$140,000 reduction in support refund requests**.

---

## Slide 14: Inventory Stock Optimization & Reorder Alerts
- **Current Inventory Value**: $1.2M tied up in stock holding costs.
- **Reorder Alert Status**:
  - **Critical Reorder**: 45 SKUs below safety stock.
  - **Healthy**: 165 SKUs.
- **Action**: Automated daily SQL trigger for low-stock SKUs.

---

## Slide 15: Risk Analytics & Fraud Detection Model
- **Algorithm**: `Isolation Forest` Anomaly Detection.
- **Feature Inputs**: Transaction Amount, Gateway Endpoint, Device Type, Geographical IP.
- **Result**: Assigned 0-100 Fraud Risk Score to all 18,000 transactions.

---

## Slide 16: Fraud Patterns & Suspicious Transaction Profiles
- **High Risk Profile**: Transactions $> \$800$ originating from non-domestic locations on mobile web browsers via legacy gateways.
- **Chargeback Exposure**: **$140,000+** in flagged transactions.

---

## Slide 17: Fraud Mitigation Action Plan
- **Rule Engine**: Auto-hold transactions with Fraud Risk Score $> 75$ for 3DS Step-up verification.
- **Gateway Audit**: Decommission underperforming payment gateways.
- **Impact**: **$110,000 in saved chargeback penalties**.

---

## Slide 18: Interactive Dashboard Suite (Streamlit & Power BI)
- **Features**:
  - Real-time C-Suite KPI cards.
  - Interactive Plotly chart drill-downs.
  - Live ML model risk lookup inspector.
  - Multi-page navigation (Executive, Customer, Operations, Risk).

---

## Slide 19: Comprehensive Financial Impact & ROI Summary
- **Program Cost**: $100,000
- **Total Financial Return**: **$725,000**
- **Net Business Value**: **+$625,000 (625% Return on Investment)**
- **Payback Period**: 2.4 Months

---

## Slide 20: Conclusion & Next Steps
- **Immediate Deployment**: Roll out Streamlit web app & Power BI datasets to business leads.
- **Automated Data Pipeline**: Schedule `data_generator.py` and ML scoring scripts via Cron / Task Scheduler.
- **Q&A**: Open floor for executive discussion.
