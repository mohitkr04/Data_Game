# Data_Game Enterprise Data Dictionary

This document defines the schema, field types, constraints, and business definitions for all 10 datasets in the `Data_Game` platform.

---

## 1. Customer Master Dataset (`customers.csv`)
- **Primary Key**: `customer_id`
- **Purpose**: Customer demographics, signup history, and acquisition attributes.

| Field Name | Data Type | Constraint / Format | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | VARCHAR(20) | PRIMARY KEY, `CUST-XXXXX` | Unique identifier for each registered customer. |
| `signup_date` | DATE | `YYYY-MM-DD` | Date the customer registered on the platform. |
| `age` | INT | `18 <= age <= 100` | Customer age in years. |
| `gender` | VARCHAR(20) | Categorical | Gender self-identification. |
| `country` | VARCHAR(50) | NOT NULL | Country of residence. |
| `city` | VARCHAR(50) | NOT NULL | Primary shipping city. |
| `customer_type` | VARCHAR(30) | Categorical | `B2C Individual`, `B2B Small Business`, `Corporate Account`. |
| `loyalty_status`| VARCHAR(20) | Categorical | `Bronze`, `Silver`, `Gold`, `Platinum`, `Regular`. |
| `acquisition_channel` | VARCHAR(30)| Categorical | Marketing channel through which customer converted. |

---

## 2. Order Transaction Dataset (`orders.csv`)
- **Primary Key**: `order_id`
- **Foreign Keys**: `customer_id` -> `customers.customer_id`, `product_id` -> `products.product_id`

| Field Name | Data Type | Constraint / Format | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR(20) | PRIMARY KEY, `ORD-XXXXXX` | Unique identifier for each order. |
| `customer_id` | VARCHAR(20) | FK -> `customers` | Customer placing the order. |
| `product_id` | VARCHAR(20) | FK -> `products` | Product purchased. |
| `order_date` | TIMESTAMP | `YYYY-MM-DD HH:MM:SS` | Timestamp of order placement. |
| `quantity` | INT | `quantity > 0` | Units of product ordered. |
| `discount` | DECIMAL(4,2) | `0.00 <= discount <= 1.00`| Promotional discount percentage applied. |
| `sales_amount` | DECIMAL(10,2)| `sales_amount >= 0` | Net monetary value of order after discount. |
| `payment_method` | VARCHAR(30)| Categorical | `Credit Card`, `Debit Card`, `PayPal`, `BNPL`, etc. |
| `order_status` | VARCHAR(20) | Categorical | `Completed`, `Shipped`, `Cancelled`, `Refunded`. |

---

## 3. Product Catalog Dataset (`products.csv`)
- **Primary Key**: `product_id`

| Field Name | Data Type | Constraint / Format | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | VARCHAR(20) | PRIMARY KEY, `PROD-XXXX` | Unique product stock-keeping unit (SKU). |
| `category` | VARCHAR(50) | NOT NULL | Top-level product category. |
| `sub_category` | VARCHAR(50) | NOT NULL | Specific product sub-category. |
| `supplier` | VARCHAR(50) | NOT NULL | Authorized manufacturer or supplier. |
| `cost_price` | DECIMAL(10,2)| `cost_price >= 0` | Unit cost price paid to supplier. |
| `selling_price`| DECIMAL(10,2)| `selling_price >= 0` | Standard retail selling price. |
| `margin_percentage` | DECIMAL(5,2)| Percentage | Gross profit margin percentage. |

---

## 4. Inventory Dataset (`inventory.csv`)
- **Primary Key**: (`product_id`, `warehouse_id`)

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `product_id` | VARCHAR(20) | Product SKU. |
| `warehouse_id` | VARCHAR(20) | Fulfilling warehouse facility ID. |
| `stock_available`| INT | Current physical units available in stock. |
| `stock_reserved` | INT | Units reserved for pending orders. |
| `reorder_level` | INT | Minimum threshold triggering stock reorder. |
| `inventory_cost` | DECIMAL(12,2)| Total holding cost of available stock (`stock_available * cost_price`). |

---

## 5. Warehouse Operations Dataset (`warehouse_operations.csv`)
- **Primary Key**: `warehouse_id`

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `warehouse_id` | VARCHAR(20) | Warehouse facility code (`WH-XX`). |
| `warehouse_name` | VARCHAR(50) | Facility location name. |
| `employee_count` | INT | Total active warehouse operations staff. |
| `daily_capacity` | INT | Maximum daily order processing capacity. |
| `processing_time` | DECIMAL(5,2)| Average order processing & fulfillment time (hours). |
| `utilization_rate`| DECIMAL(5,2)| Percentage of maximum capacity currently utilized. |

---

## 6. Delivery Performance Dataset (`delivery.csv`)
- **Primary Key**: `order_id`

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `order_id` | VARCHAR(20) | Order ID linked to delivery shipment. |
| `warehouse_id` | VARCHAR(20) | Origin warehouse facility. |
| `courier_partner`| VARCHAR(50) | Logistics courier (`FedEx`, `DHL`, `UPS`, etc.). |
| `shipping_date` | TIMESTAMP | Departure timestamp from warehouse. |
| `delivery_date` | TIMESTAMP | Delivery timestamp at customer location. |
| `delay_reason` | VARCHAR(100)| Root cause of delay (`Weather`, `Customs`, `Bottleneck`, etc.). |
| `delivery_status`| VARCHAR(30) | Status (`Delivered`, `Delayed`). |

---

## 7. Payment Transaction Dataset (`transactions.csv`)
- **Primary Key**: `transaction_id`

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `transaction_id` | VARCHAR(25) | Payment transaction reference. |
| `customer_id` | VARCHAR(20) | Customer initiating transaction. |
| `transaction_amount` | DECIMAL(10,2)| Total monetary transaction value. |
| `payment_gateway` | VARCHAR(30) | Gateway used (`Stripe`, `Adyen`, `PayPal`, etc.). |
| `device_type` | VARCHAR(30) | Operating device (`iOS`, `Android`, `Windows`). |
| `location` | VARCHAR(30) | Geographical IP transaction region. |
| `transaction_status` | VARCHAR(20) | `Approved`, `Declined`, `Flagged_Fraud`, `Chargeback`. |

---

## 8. Customer Support Dataset (`customer_support.csv`)
- **Primary Key**: `ticket_id`

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `ticket_id` | VARCHAR(20) | Support ticket reference ID. |
| `customer_id` | VARCHAR(20) | Customer submitting ticket. |
| `issue_type` | VARCHAR(50) | Category (`Late Delivery`, `Damaged Item`, `Refund Inquiry`, etc.). |
| `resolution_time` | DECIMAL(5,1)| Hours taken to resolve ticket. |
| `satisfaction_score`| INT | Post-resolution CSAT score (1 - 5). |
| `refund_requested` | VARCHAR(3) | Whether a monetary refund was demanded (`Yes`, `No`). |

---

## 9. Marketing Campaign Dataset (`marketing_campaign.csv`)
- **Primary Key**: `campaign_id`

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `campaign_id` | VARCHAR(20) | Marketing touchpoint ID. |
| `customer_id` | VARCHAR(20) | Targeted customer. |
| `campaign_type` | VARCHAR(40) | Medium (`Email`, `Google PPC`, `Meta Ads`, `Influencer`). |
| `marketing_cost` | DECIMAL(8,2) | Cost of campaign execution. |
| `conversion_status`| VARCHAR(20) | `Converted`, `Not Converted`. |
| `revenue_generated`| DECIMAL(10,2)| Revenue attributed to campaign conversion. |

---

## 10. Customer Reviews Dataset (`reviews.csv`)
- **Primary Key**: `review_id`

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `review_id` | VARCHAR(20) | Customer feedback review ID. |
| `customer_id` | VARCHAR(20) | Review author. |
| `product_id` | VARCHAR(20) | Product reviewed. |
| `rating` | INT | Numerical star rating (1 to 5). |
| `review_text` | TEXT | Qualitative review sentiment text. |
