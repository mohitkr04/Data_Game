# Power BI Modeling & DAX Blueprint

This guide provides step-by-step instructions to recreate the **Data_Game Enterprise Analytics Dashboard** in Power BI Desktop.

---

## 1. Data Connection & Star Schema Architecture

### Connecting Power BI to the SQLite / CSV Engine
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Folder** or **CSV** (or ODBC -> SQLite DSN if connecting to `data_game.db`).
3. Select the `Data_Game/data/raw/` directory to load all 10 raw CSV files:
   - `customers.csv` (Dimension Table)
   - `products.csv` (Dimension Table)
   - `orders.csv` (Fact Table)
   - `warehouse_operations.csv` (Dimension Table)
   - `inventory.csv` (Fact Table)
   - `delivery.csv` (Fact Table)
   - `transactions.csv` (Fact Table)
   - `customer_support.csv` (Fact Table)
   - `marketing_campaign.csv` (Fact Table)
   - `reviews.csv` (Fact Table)

---

## 2. Relational Star Schema Model

In Power BI **Model View**, build the following primary-to-foreign key relationships (1-to-Many, Single Direction):

```
                       ┌────────────────┐
                       │  customers     │ (Dim)
                       └───────┬────────┘
                               │ (1:N)
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼────────┐     ┌───────▼────────┐     ┌───────▼────────┐
│     orders     │     │  transactions  │     │ customer_support│
└───────┬────────┘     └────────────────┘     └────────────────┘
        │ (N:1)
┌───────▼────────┐
│    products    │ (Dim)
└────────────────┘
```

---

## 3. Core Enterprise DAX Measures

Create a dedicated measure table `[All_Measures]` in Power BI and paste the following production DAX formulas:

### Revenue & Profitability Measures
```dax
-- Total Gross Revenue
Gross Revenue = 
SUMX(
    FILTER(orders, orders[order_status] <> "Cancelled" && orders[order_status] <> "Refunded"),
    orders[sales_amount]
)

-- Total Cost of Goods Sold (COGS)
Total COGS = 
SUMX(
    FILTER(orders, orders[order_status] <> "Cancelled" && orders[order_status] <> "Refunded"),
    orders[quantity] * RELATED(products[cost_price])
)

-- Net Profit Margin
Net Profit = [Gross Revenue] - [Total COGS]

Net Profit Margin % = 
DIVIDE([Net Profit], [Gross Revenue], 0) * 100

-- Average Order Value (AOV)
AOV = 
DIVIDE([Gross Revenue], COUNTROWS(FILTER(orders, orders[order_status] <> "Cancelled")), 0)
```

### Customer & Churn DAX Measures
```dax
-- Active Customer Count
Active Customers = 
DISTINCTCOUNT(orders[customer_id])

-- Churn Rate %
Churn Rate % = 
VAR TotalCust = COUNTROWS(customers)
VAR ChurnedCust = CALCULATE(COUNTROWS(customers), FILTER(customers, [Days Since Last Order] > 120))
RETURN DIVIDE(ChurnedCust, TotalCust, 0) * 100
```

### Operations & SLA DAX Measures
```dax
-- Delivery Delay Rate %
Delay Rate % = 
VAR DelayedOrders = CALCULATE(COUNTROWS(delivery), delivery[delivery_status] = "Delayed")
VAR TotalDeliveries = COUNTROWS(delivery)
RETURN DIVIDE(DelayedOrders, TotalDeliveries, 0) * 100

-- Average Warehouse Utilization %
Avg WH Utilization % = 
AVERAGE(warehouse_operations[utilization_rate])
```

---

## 4. Recommended Page Layouts for Power BI

1. **Page 1: C-Suite Executive Overview**
   - KPI Cards: Gross Revenue, Net Profit, Active Customers, AOV.
   - Line Chart: MoM Revenue Growth Trend.
   - Bar Chart: Product Profitability by Category.
2. **Page 2: Customer RFM & Retargeting**
   - Treemap: RFM Customer Segment Breakdown.
   - Scatter Matrix: Recency vs Monetary Value.
3. **Page 3: Operations & Courier SLA**
   - Clustered Bar: Warehouse Utilization vs Daily Capacity.
   - Stacked Bar: Courier Partner Delay Reasons.
4. **Page 4: Risk Analytics & Fraud Monitor**
   - Card: High Fraud Risk Alerts Count.
   - Table: Suspicious Transactions Table (Gateway, Location, Risk Score).
