-- =========================================================
-- Enterprise Analytics Database Schema
-- Platform: E-Commerce Intelligence, Operations Optimization & Risk Analytics
-- Project: Data_Game
-- =========================================================

-- 1. CUSTOMERS MASTER TABLE
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    signup_date DATE NOT NULL,
    age INT CHECK (age >= 18 AND age <= 100),
    gender VARCHAR(20),
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    customer_type VARCHAR(30) NOT NULL,
    loyalty_status VARCHAR(20) NOT NULL,
    acquisition_channel VARCHAR(30) NOT NULL
);

-- 2. PRODUCTS CATALOG TABLE
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    supplier VARCHAR(50) NOT NULL,
    cost_price DECIMAL(10, 2) NOT NULL CHECK (cost_price >= 0),
    selling_price DECIMAL(10, 2) NOT NULL CHECK (selling_price >= 0),
    margin_percentage DECIMAL(5, 2) NOT NULL
);

-- 3. ORDERS TRANSACTION TABLE
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    order_date TIMESTAMP NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    discount DECIMAL(4, 2) DEFAULT 0.00 CHECK (discount >= 0 AND discount <= 1),
    sales_amount DECIMAL(10, 2) NOT NULL CHECK (sales_amount >= 0),
    payment_method VARCHAR(30) NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 4. WAREHOUSE OPERATIONS TABLE
CREATE TABLE IF NOT EXISTS warehouse_operations (
    warehouse_id VARCHAR(20) PRIMARY KEY,
    warehouse_name VARCHAR(50) NOT NULL,
    employee_count INT NOT NULL CHECK (employee_count > 0),
    daily_capacity INT NOT NULL CHECK (daily_capacity > 0),
    processing_time DECIMAL(5, 2) NOT NULL CHECK (processing_time >= 0),
    utilization_rate DECIMAL(5, 2) NOT NULL CHECK (utilization_rate >= 0)
);

-- 5. INVENTORY OPTIMIZATION TABLE
CREATE TABLE IF NOT EXISTS inventory (
    product_id VARCHAR(20) NOT NULL,
    warehouse_id VARCHAR(20) NOT NULL,
    stock_available INT NOT NULL CHECK (stock_available >= 0),
    stock_reserved INT DEFAULT 0 CHECK (stock_reserved >= 0),
    reorder_level INT NOT NULL CHECK (reorder_level >= 0),
    inventory_cost DECIMAL(12, 2) NOT NULL CHECK (inventory_cost >= 0),
    PRIMARY KEY (product_id, warehouse_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouse_operations(warehouse_id)
);

-- 6. DELIVERY PERFORMANCE TABLE
CREATE TABLE IF NOT EXISTS delivery (
    order_id VARCHAR(20) PRIMARY KEY,
    warehouse_id VARCHAR(20) NOT NULL,
    courier_partner VARCHAR(50) NOT NULL,
    shipping_date TIMESTAMP NOT NULL,
    delivery_date TIMESTAMP,
    delay_reason VARCHAR(100),
    delivery_status VARCHAR(30) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouse_operations(warehouse_id)
);

-- 7. PAYMENT TRANSACTION TABLE (RISK ANALYTICS)
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(25) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    transaction_amount DECIMAL(10, 2) NOT NULL CHECK (transaction_amount >= 0),
    payment_gateway VARCHAR(30) NOT NULL,
    device_type VARCHAR(30) NOT NULL,
    location VARCHAR(30) NOT NULL,
    transaction_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 8. CUSTOMER SUPPORT TABLE
CREATE TABLE IF NOT EXISTS customer_support (
    ticket_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    issue_type VARCHAR(50) NOT NULL,
    resolution_time DECIMAL(5, 1) NOT NULL CHECK (resolution_time >= 0),
    satisfaction_score INT CHECK (satisfaction_score BETWEEN 1 AND 5),
    refund_requested VARCHAR(3) CHECK (refund_requested IN ('Yes', 'No')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 9. MARKETING CAMPAIGN TABLE
CREATE TABLE IF NOT EXISTS marketing_campaign (
    campaign_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    campaign_type VARCHAR(40) NOT NULL,
    marketing_cost DECIMAL(8, 2) NOT NULL CHECK (marketing_cost >= 0),
    conversion_status VARCHAR(20) NOT NULL,
    revenue_generated DECIMAL(10, 2) DEFAULT 0.00 CHECK (revenue_generated >= 0),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 10. CUSTOMER REVIEWS TABLE
CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
