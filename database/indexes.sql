-- =========================================================
-- Enterprise Analytics Indexing Strategy
-- Project: Data_Game
-- Goal: Query Optimization for High-Scale Reporting
-- =========================================================

-- Index on Orders Date and Customer ID for fast temporal and user-level aggregation
CREATE INDEX IF NOT EXISTS idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX IF NOT EXISTS idx_orders_product ON orders(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status);

-- Index on Delivery Performance for Warehouse Bottleneck & Courier Analysis
CREATE INDEX IF NOT EXISTS idx_delivery_warehouse_courier ON delivery(warehouse_id, courier_partner);
CREATE INDEX IF NOT EXISTS idx_delivery_status ON delivery(delivery_status);

-- Index on Transactions for Risk & Fraud Scoring
CREATE INDEX IF NOT EXISTS idx_transactions_customer_status ON transactions(customer_id, transaction_status);
CREATE INDEX IF NOT EXISTS idx_transactions_amount ON transactions(transaction_amount);

-- Index on Inventory Reorder Level Alerts
CREATE INDEX IF NOT EXISTS idx_inventory_reorder ON inventory(stock_available, reorder_level);

-- Index on Customer Support Issue Types & Satisfaction
CREATE INDEX IF NOT EXISTS idx_support_issue_score ON customer_support(issue_type, satisfaction_score);

-- Index on Marketing Campaigns for ROI Metrics
CREATE INDEX IF NOT EXISTS idx_marketing_conversion ON marketing_campaign(campaign_type, conversion_status);
