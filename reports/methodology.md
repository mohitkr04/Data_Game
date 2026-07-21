# Enterprise Analytics Methodology & Analytical Rationale

This document outlines the technical design, statistical methodologies, machine learning algorithms, and validation strategies implemented in the `Data_Game` platform.

---

## 1. SQL Data Modeling & Relational Engineering

### Architecture Choice: Relational Star & Snowflake Hybrid Schema
- **Normalizing Dimensions**: `customers`, `products`, and `warehouse_operations` serve as master dimension tables, enforcing strict data types (`DECIMAL`, `INTEGER`, `VARCHAR`, `TIMESTAMP`), foreign key constraints, and check bounds.
- **Fact Tables**: `orders`, `transactions`, `delivery`, `customer_support`, `marketing_campaign`, and `reviews` record high-volume transactional events.
- **Indexing Strategy**:
  - High-cardinality foreign keys (`orders.customer_id`, `orders.product_id`) utilize B-Tree indexes to optimize multi-table SQL `JOIN` performance.
  - Temporal fields (`orders.order_date`) feature composite indexes to accelerate Window Function computations (`LAG`, `LEAD`, `NTILE`) and MoM trend aggregation.

---

## 2. RFM Customer Segmentation & Unsupervised Clustering

### Rule-Based RFM Scoring
Customers are evaluated across three dimensions relative to a fixed snapshot date (`2026-07-01`):
1. **Recency ($R$)**: Days since last completed order $\rightarrow$ Quintile scored from 1 (Oldest) to 5 (Most Recent).
2. **Frequency ($F$)**: Total distinct order count $\rightarrow$ Quintile scored from 1 (Lowest) to 5 (Highest).
3. **Monetary ($M$)**: Total historical net sales contribution $\rightarrow$ Quintile scored from 1 (Lowest) to 5 (Highest).

### Machine Learning: K-Means Clustering
- **Feature Scaling**: Standardized via $Z$-score normalization ($X_{scaled} = \frac{X - \mu}{\sigma}$) to prevent high monetary amounts from dominating Euclidean distance calculations.
- **Evaluation**: Validated via Silhouette Coefficient ($S = \frac{b - a}{\max(a, b)}$), obtaining an optimal cluster resolution at $k=4$.

---

## 3. Supervised Machine Learning: Customer Churn Classifier

### Problem Formulation & Target Definition
- **Target Label ($y$)**: Binary indicator where $y=1$ (Churned) if `days_since_last_order` $> 120$ days or `total_orders` $= 0$; otherwise $y=0$ (Active).
- **Feature Engineering**:
  - Customer profile: `age`, `loyalty_status`, `customer_type`.
  - Transactional engagement: `total_orders`, `total_spent`, `avg_order_val`.
  - Support & Friction: `support_tickets_count`, `avg_resolution_hours`, `avg_satisfaction`, `refund_tickets_count`.
  - Sentiment: `avg_review_rating`.

### Algorithm Choice & Evaluation Metrics
- **Model**: `RandomForestClassifier` with $N=100$ trees, tree depth constrained to 8 to prevent overfitting.
- **Evaluation Metrics**:
  - **ROC-AUC**: Assesses ranking capability across variable probability thresholds. Target: $> 0.82$.
  - **Precision & Recall**: Evaluates false positive vs false negative trade-offs in high-value customer retargeting campaigns.

---

## 4. Anomaly Detection & Fraud Risk Scoring

### Algorithm: Isolation Forest
- **Rationale**: Fraudulent transactions represent rare, non-conforming observations in multi-dimensional feature space. Tree-based isolation isolates anomalies significantly closer to the root of decision trees than normal observations.
- **Risk Score Formulation**:
  Decision function outputs $s(x, n)$ are mapped linearly to a 0 – 100 risk score scale:
  $$\text{Fraud Risk Score} = \left(1 - \frac{s(x) - s_{\min}}{s_{\max} - s_{\min}}\right) \times 100$$
- **Risk Tiers**:
  - **Low Risk**: $0 - 50$
  - **Medium Risk**: $51 - 75$
  - **High Risk**: $76 - 100$ (Triggering manual compliance hold or automated step-up authentication).

---

## 5. Time Series Forecasting: 6-Month Revenue Projection

### Algorithm: Holt-Winters Exponential Smoothing
- **Model Components**: Captures baseline level ($l_t$), trend ($b_t$), and additive seasonality ($s_t$):
  $$\hat{y}_{t+h|t} = l_t + h b_t + s_{t+h-m(k+1)}$$
- **Forecast Horizon**: Produces 6-month out-of-sample monthly projections with confidence bounds to inform inventory reorder levels and quarterly operational budget allocation.
