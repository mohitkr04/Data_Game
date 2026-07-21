-- =========================================================
-- Advanced Analytical SQL Suite
-- Project: Data_Game
-- Key Features: CTEs, Window Functions, Complex Joins, Views
-- =========================================================

-- ---------------------------------------------------------
-- 1. REVENUE GROWTH & MOM TREND ANALYSIS (CTE + Window Functions)
-- ---------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_monthly_revenue_performance AS
WITH MonthlyMetrics AS (
    SELECT 
        STRFTIME('%Y-%m', order_date) AS order_month,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS active_customers,
        SUM(sales_amount) AS total_revenue,
        ROUND(AVG(sales_amount), 2) AS average_order_value
    FROM orders
    WHERE order_status NOT IN ('Cancelled', 'Refunded')
    GROUP BY 1
)
SELECT 
    order_month,
    total_orders,
    active_customers,
    total_revenue,
    average_order_value,
    LAG(total_revenue, 1) OVER (ORDER BY order_month) AS previous_month_revenue,
    ROUND(
        (total_revenue - LAG(total_revenue, 1) OVER (ORDER BY order_month)) 
        / LAG(total_revenue, 1) OVER (ORDER BY order_month) * 100, 2
    ) AS mom_growth_percentage
FROM MonthlyMetrics;


-- ---------------------------------------------------------
-- 2. PRODUCT PROFITABILITY & MARGIN LEADERBOARD
-- ---------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_product_profitability AS
WITH ProductSales AS (
    SELECT 
        p.product_id,
        p.category,
        p.sub_category,
        p.cost_price,
        p.selling_price,
        COUNT(o.order_id) AS total_units_sold,
        SUM(o.sales_amount) AS gross_revenue,
        SUM(o.quantity * p.cost_price) AS total_cost_of_goods_sold
    FROM products p
    JOIN orders o ON p.product_id = o.product_id
    WHERE o.order_status NOT IN ('Cancelled', 'Refunded')
    GROUP BY p.product_id, p.category, p.sub_category, p.cost_price, p.selling_price
)
SELECT 
    product_id,
    category,
    sub_category,
    total_units_sold,
    gross_revenue,
    total_cost_of_goods_sold,
    ROUND(gross_revenue - total_cost_of_goods_sold, 2) AS net_profit,
    ROUND((gross_revenue - total_cost_of_goods_sold) / gross_revenue * 100, 2) AS net_profit_margin_pct,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY (gross_revenue - total_cost_of_goods_sold) DESC) AS category_profit_rank
FROM ProductSales;


-- ---------------------------------------------------------
-- 3. SQL-BASED RFM SEGMENTATION ENGINE (NTILE Window Functions)
-- ---------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_rfm_customer_segments AS
WITH CustomerRFM AS (
    SELECT 
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(order_id) AS frequency,
        SUM(sales_amount) AS monetary,
        CAST(JULIANDAY('2026-07-01') - JULIANDAY(MAX(order_date)) AS INT) AS recency_days
    FROM orders
    WHERE order_status NOT IN ('Cancelled', 'Refunded')
    GROUP BY customer_id
),
RFMScores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM CustomerRFM
)
SELECT 
    customer_id,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) AS total_rfm_score,
    CASE 
        WHEN (r_score >= 4 AND f_score >= 4 AND m_score >= 4) THEN 'VIP Champion'
        WHEN (r_score >= 3 AND f_score >= 3) THEN 'Loyal Customer'
        WHEN (r_score >= 4 AND f_score <= 2) THEN 'New Customer'
        WHEN (r_score <= 2 AND f_score >= 3) THEN 'At-Risk High Value'
        ELSE 'Hibernating / Lost'
    END AS rfm_segment
FROM RFMScores;


-- ---------------------------------------------------------
-- 4. WAREHOUSE & COURIER SLA DELAY BOTTLENECK ANALYSIS
-- ---------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_delivery_sla_bottlenecks AS
SELECT 
    d.courier_partner,
    w.warehouse_name,
    COUNT(d.order_id) AS total_shipments,
    SUM(CASE WHEN d.delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND(SUM(CASE WHEN d.delivery_status = 'Delayed' THEN 1 ELSE 0 END) * 100.0 / COUNT(d.order_id), 2) AS delay_rate_pct,
    d.delay_reason,
    ROUND(AVG(w.processing_time), 2) AS avg_wh_processing_hours
FROM delivery d
JOIN warehouse_operations w ON d.warehouse_id = w.warehouse_id
GROUP BY d.courier_partner, w.warehouse_name, d.delay_reason;


-- ---------------------------------------------------------
-- 5. SUSPICIOUS HIGH-RISK FRAUD DETECTION QUERY
-- ---------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_high_risk_fraud_alerts AS
WITH CustomerRiskStats AS (
    SELECT 
        customer_id,
        COUNT(transaction_id) AS total_tx_count,
        SUM(CASE WHEN transaction_status IN ('Flagged_Fraud', 'Chargeback') THEN 1 ELSE 0 END) AS fraud_chargeback_count,
        SUM(transaction_amount) AS total_spend,
        MAX(transaction_amount) AS max_single_tx
    FROM transactions
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    c.country,
    c.customer_type,
    r.total_tx_count,
    r.fraud_chargeback_count,
    r.total_spend,
    r.max_single_tx,
    ROUND(r.fraud_chargeback_count * 100.0 / r.total_tx_count, 2) AS fraud_rate_pct,
    CASE 
        WHEN r.fraud_chargeback_count >= 2 OR r.max_single_tx > 3000 THEN 'HIGH RISK'
        WHEN r.fraud_chargeback_count = 1 THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END AS risk_tier
FROM CustomerRiskStats r
JOIN customers c ON r.customer_id = c.customer_id
WHERE r.fraud_chargeback_count > 0 OR r.max_single_tx > 3000
ORDER BY r.fraud_chargeback_count DESC, r.max_single_tx DESC;
