import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
os.makedirs(DATA_DIR, exist_ok=True)

print("Starting generation of 10 enterprise datasets for Data_Game...")

# Configuration for Data Scale
NUM_CUSTOMERS = 3500
NUM_PRODUCTS = 250
NUM_WAREHOUSES = 8
NUM_ORDERS = 15000
NUM_TRANSACTIONS = 18000
NUM_CAMPAIGNS = 4000
NUM_SUPPORT_TICKETS = 3000
NUM_REVIEWS = 4500

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 6, 30)

# Helper function to generate random dates
def random_dates(start, end, n):
    delta = end - start
    return [start + timedelta(seconds=random.randint(0, int(delta.total_seconds()))) for _ in range(n)]

# ---------------------------------------------------------
# 1. CUSTOMERS DATASET
# ---------------------------------------------------------
print("1/10 Generating customers.csv...")
countries = ['United States', 'United Kingdom', 'Germany', 'Canada', 'Australia', 'France', 'Japan']
cities_by_country = {
    'United States': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'United Kingdom': ['London', 'Manchester', 'Birmingham', 'Edinburgh'],
    'Germany': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary'],
    'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth'],
    'France': ['Paris', 'Lyon', 'Marseille'],
    'Japan': ['Tokyo', 'Osaka', 'Nagoya']
}

customer_types = ['B2C Individual', 'B2B Small Business', 'Corporate Account']
loyalty_statuses = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Regular']
channels = ['Organic Search', 'Paid Search', 'Social Media', 'Email Referral', 'Direct Market']

customer_ids = [f"CUST-{i:05d}" for i in range(1, NUM_CUSTOMERS + 1)]
signup_dates = random_dates(START_DATE, END_DATE - timedelta(days=90), NUM_CUSTOMERS)

cust_country = np.random.choice(countries, NUM_CUSTOMERS, p=[0.4, 0.15, 0.12, 0.13, 0.08, 0.07, 0.05])
cust_city = [random.choice(cities_by_country[c]) for c in cust_country]

customers_df = pd.DataFrame({
    'customer_id': customer_ids,
    'signup_date': [d.strftime('%Y-%m-%d') for d in signup_dates],
    'age': np.random.randint(18, 70, NUM_CUSTOMERS),
    'gender': np.random.choice(['Male', 'Female', 'Non-Binary', 'Prefer Not to Say'], NUM_CUSTOMERS, p=[0.48, 0.48, 0.02, 0.02]),
    'country': cust_country,
    'city': cust_city,
    'customer_type': np.random.choice(customer_types, NUM_CUSTOMERS, p=[0.75, 0.18, 0.07]),
    'loyalty_status': np.random.choice(loyalty_statuses, NUM_CUSTOMERS, p=[0.40, 0.30, 0.18, 0.07, 0.05]),
    'acquisition_channel': np.random.choice(channels, NUM_CUSTOMERS, p=[0.30, 0.25, 0.20, 0.15, 0.10])
})
customers_df.to_csv(os.path.join(DATA_DIR, 'customers.csv'), index=False)


# ---------------------------------------------------------
# 2. PRODUCTS DATASET
# ---------------------------------------------------------
print("2/10 Generating products.csv...")
categories = {
    'Electronics': ['Smartphones', 'Laptops', 'Audio & Headphones', 'Wearables', 'Accessories'],
    'Apparel & Fashion': ['Men Clothing', 'Women Clothing', 'Footwear', 'Watches', 'Bags'],
    'Home & Kitchen': ['Furniture', 'Cookware', 'Home Decor', 'Bedding', 'Lighting'],
    'Beauty & Health': ['Skincare', 'Haircare', 'Personal Care', 'Fitness Equipment'],
    'Office & Toys': ['Office Supplies', 'Board Games', 'Educational Toys', 'Stationery']
}

product_list = []
prod_id_counter = 1
suppliers = ['TechSupply Co', 'GlobalFashion Ltd', 'HomeComfort Inc', 'AuraBeauty Group', 'Apex Logistics Pro']

for cat, subcats in categories.items():
    for subcat in subcats:
        num_in_sub = random.randint(8, 14)
        for _ in range(num_in_sub):
            p_id = f"PROD-{prod_id_counter:04d}"
            cost_price = round(float(np.random.uniform(5.0, 450.0)), 2)
            markup = float(np.random.uniform(1.2, 2.5))
            selling_price = round(cost_price * markup, 2)
            margin_pct = round(((selling_price - cost_price) / selling_price) * 100, 2)
            
            product_list.append({
                'product_id': p_id,
                'category': cat,
                'sub_category': subcat,
                'supplier': random.choice(suppliers),
                'cost_price': cost_price,
                'selling_price': selling_price,
                'margin_percentage': margin_pct
            })
            prod_id_counter += 1

products_df = pd.DataFrame(product_list)
products_df.to_csv(os.path.join(DATA_DIR, 'products.csv'), index=False)


# ---------------------------------------------------------
# 3. ORDERS DATASET
# ---------------------------------------------------------
print("3/10 Generating orders.csv...")
order_ids = [f"ORD-{i:06d}" for i in range(1, NUM_ORDERS + 1)]

# Assign orders across dates
order_dates = sorted(random_dates(START_DATE, END_DATE, NUM_ORDERS))
order_cust_ids = np.random.choice(customers_df['customer_id'], NUM_ORDERS)
order_prod_ids = np.random.choice(products_df['product_id'], NUM_ORDERS)

prod_price_map = dict(zip(products_df['product_id'], products_df['selling_price']))

quantities = np.random.choice([1, 2, 3, 4, 5, 10], NUM_ORDERS, p=[0.55, 0.25, 0.10, 0.05, 0.03, 0.02])
discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.30], NUM_ORDERS, p=[0.50, 0.20, 0.15, 0.08, 0.05, 0.02])

sales_amounts = []
for p_id, q, d in zip(order_prod_ids, quantities, discounts):
    base_price = prod_price_map[p_id]
    amount = round(base_price * q * (1 - d), 2)
    sales_amounts.append(amount)

payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Bank Transfer', 'BNPL (Klarna)']
order_statuses = ['Completed', 'Completed', 'Completed', 'Completed', 'Shipped', 'Cancelled', 'Refunded']

orders_df = pd.DataFrame({
    'order_id': order_ids,
    'customer_id': order_cust_ids,
    'product_id': order_prod_ids,
    'order_date': [d.strftime('%Y-%m-%d %H:%M:%S') for d in order_dates],
    'quantity': quantities,
    'discount': discounts,
    'sales_amount': sales_amounts,
    'payment_method': np.random.choice(payment_methods, NUM_ORDERS, p=[0.40, 0.25, 0.15, 0.10, 0.05, 0.05]),
    'order_status': np.random.choice(order_statuses, NUM_ORDERS, p=[0.70, 0.10, 0.05, 0.05, 0.04, 0.03, 0.03])
})
orders_df.to_csv(os.path.join(DATA_DIR, 'orders.csv'), index=False)


# ---------------------------------------------------------
# 4. WAREHOUSE OPERATIONS DATASET
# ---------------------------------------------------------
print("4/10 Generating warehouse_operations.csv...")
warehouse_ids = [f"WH-{i:02d}" for i in range(1, NUM_WAREHOUSES + 1)]
wh_locations = ['New Jersey Hub', 'Dallas Mega-Center', 'Chicago Midwest', 'LA Logistics', 'Seattle North', 'Atlanta South', 'Frankfurt EU Central', 'Tokyo East']

wh_ops_list = []
for i, wh_id in enumerate(warehouse_ids):
    emp_cnt = random.randint(45, 220)
    capacity = emp_cnt * random.randint(40, 60)
    proc_time = round(random.uniform(2.1, 8.5), 2) # Hours
    util_rate = round(random.uniform(62.0, 96.5), 2) # Percentage
    wh_ops_list.append({
        'warehouse_id': wh_id,
        'warehouse_name': wh_locations[i],
        'employee_count': emp_cnt,
        'daily_capacity': capacity,
        'processing_time': proc_time,
        'utilization_rate': util_rate
    })

wh_ops_df = pd.DataFrame(wh_ops_list)
wh_ops_df.to_csv(os.path.join(DATA_DIR, 'warehouse_operations.csv'), index=False)


# ---------------------------------------------------------
# 5. INVENTORY DATASET
# ---------------------------------------------------------
print("5/10 Generating inventory.csv...")
inventory_list = []
for p_id in products_df['product_id']:
    wh_id = random.choice(warehouse_ids)
    stk_avail = random.randint(10, 800)
    stk_res = random.randint(0, min(150, stk_avail))
    reorder_lvl = random.randint(30, 100)
    cost = products_df.loc[products_df['product_id'] == p_id, 'cost_price'].values[0]
    inv_cost = round(stk_avail * cost, 2)
    
    inventory_list.append({
        'product_id': p_id,
        'warehouse_id': wh_id,
        'stock_available': stk_avail,
        'stock_reserved': stk_res,
        'reorder_level': reorder_lvl,
        'inventory_cost': inv_cost
    })

inventory_df = pd.DataFrame(inventory_list)
inventory_df.to_csv(os.path.join(DATA_DIR, 'inventory.csv'), index=False)


# ---------------------------------------------------------
# 6. DELIVERY PERFORMANCE DATASET
# ---------------------------------------------------------
print("6/10 Generating delivery.csv...")
couriers = ['FedEx Express', 'DHL Supply Chain', 'UPS Ground', 'Amazon Logistics', 'USPS Priority']
delay_reasons = ['None', 'Weather Disruption', 'Customs Delay', 'Warehouse Bottleneck', 'Traffic & Vehicle Breakdown', 'Incorrect Address']

delivery_list = []
completed_shipped_orders = orders_df[orders_df['order_status'].isin(['Completed', 'Shipped'])]

for idx, row in completed_shipped_orders.iterrows():
    o_id = row['order_id']
    wh_id = random.choice(warehouse_ids)
    courier = np.random.choice(couriers, p=[0.30, 0.25, 0.20, 0.15, 0.10])
    
    order_dt = datetime.strptime(row['order_date'], '%Y-%m-%d %H:%M:%S')
    ship_dt = order_dt + timedelta(hours=random.randint(4, 48))
    
    # Introduce courier-specific delay distribution
    is_delayed = random.random() < (0.28 if courier == 'USPS Priority' else 0.12)
    if is_delayed:
        del_dt = ship_dt + timedelta(days=random.randint(4, 10))
        reason = random.choice(delay_reasons[1:])
        status = 'Delayed'
    else:
        del_dt = ship_dt + timedelta(days=random.randint(1, 3))
        reason = 'None'
        status = 'Delivered'
        
    delivery_list.append({
        'order_id': o_id,
        'warehouse_id': wh_id,
        'courier_partner': courier,
        'shipping_date': ship_dt.strftime('%Y-%m-%d %H:%M:%S'),
        'delivery_date': del_dt.strftime('%Y-%m-%d %H:%M:%S'),
        'delay_reason': reason,
        'delivery_status': status
    })

delivery_df = pd.DataFrame(delivery_list)
delivery_df.to_csv(os.path.join(DATA_DIR, 'delivery.csv'), index=False)


# ---------------------------------------------------------
# 7. PAYMENT TRANSACTION DATASET
# ---------------------------------------------------------
print("7/10 Generating transactions.csv...")
gateways = ['Stripe', 'Adyen', 'PayPal Gateway', 'Square', 'Authorize.Net']
device_types = ['Mobile iOS', 'Mobile Android', 'Desktop Windows', 'Desktop MacOS', 'Tablet']
locations = ['US-East', 'US-West', 'EU-Central', 'APAC-East', 'LATAM-South']
tx_statuses = ['Approved', 'Approved', 'Approved', 'Approved', 'Declined', 'Flagged_Fraud', 'Chargeback']

tx_list = []
tx_id_counter = 1

# Generate normal and suspicious transactions
for i in range(NUM_TRANSACTIONS):
    t_id = f"TXN-{tx_id_counter:07d}"
    c_id = random.choice(customer_ids)
    gateway = random.choice(gateways)
    device = random.choice(device_types)
    loc = random.choice(locations)
    
    # Fraud pattern simulation
    is_fraud_sample = random.random() < 0.04
    if is_fraud_sample:
        amount = round(float(np.random.uniform(800.0, 5000.0)), 2)
        status = np.random.choice(['Flagged_Fraud', 'Chargeback', 'Declined'], p=[0.50, 0.30, 0.20])
    else:
        amount = round(float(np.random.exponential(scale=120.0) + 10.0), 2)
        status = np.random.choice(['Approved', 'Declined'], p=[0.94, 0.06])
        
    tx_list.append({
        'transaction_id': t_id,
        'customer_id': c_id,
        'transaction_amount': amount,
        'payment_gateway': gateway,
        'device_type': device,
        'location': loc,
        'transaction_status': status
    })
    tx_id_counter += 1

transactions_df = pd.DataFrame(tx_list)
transactions_df.to_csv(os.path.join(DATA_DIR, 'transactions.csv'), index=False)


# ---------------------------------------------------------
# 8. CUSTOMER SUPPORT DATASET
# ---------------------------------------------------------
print("8/10 Generating customer_support.csv...")
issue_types = ['Late Delivery', 'Damaged Item', 'Wrong Item Sent', 'Payment Issue', 'Refund Inquiry', 'Account Security']

ticket_list = []
for i in range(1, NUM_SUPPORT_TICKETS + 1):
    tk_id = f"TCK-{i:06d}"
    c_id = random.choice(customer_ids)
    issue = np.random.choice(issue_types, p=[0.35, 0.20, 0.15, 0.12, 0.10, 0.08])
    
    # Correlation: Late delivery & Damaged item have higher resolution time & refund requests
    if issue in ['Late Delivery', 'Damaged Item']:
        res_time = round(float(np.random.uniform(12.0, 72.0)), 1) # hours
        sat_score = np.random.choice([1, 2, 3, 4, 5], p=[0.35, 0.30, 0.20, 0.10, 0.05])
        refund_req = np.random.choice(['Yes', 'No'], p=[0.65, 0.35])
    else:
        res_time = round(float(np.random.uniform(1.0, 24.0)), 1)
        sat_score = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.10, 0.25, 0.35, 0.25])
        refund_req = np.random.choice(['Yes', 'No'], p=[0.20, 0.80])
        
    ticket_list.append({
        'ticket_id': tk_id,
        'customer_id': c_id,
        'issue_type': issue,
        'resolution_time': res_time,
        'satisfaction_score': sat_score,
        'refund_requested': refund_req
    })

customer_support_df = pd.DataFrame(ticket_list)
customer_support_df.to_csv(os.path.join(DATA_DIR, 'customer_support.csv'), index=False)


# ---------------------------------------------------------
# 9. MARKETING CAMPAIGN DATASET
# ---------------------------------------------------------
print("9/10 Generating marketing_campaign.csv...")
campaign_types = ['Email Retargeting', 'Google PPC', 'Meta Paid Ads', 'Influencer Sponsor', 'Affiliate Promo']

campaign_list = []
for i in range(1, NUM_CAMPAIGNS + 1):
    cmp_id = f"CMP-{i:05d}"
    c_id = random.choice(customer_ids)
    cmp_type = np.random.choice(campaign_types, p=[0.30, 0.25, 0.20, 0.15, 0.10])
    cost = round(float(np.random.uniform(5.0, 85.0)), 2)
    
    converted = random.random() < 0.22
    conv_status = 'Converted' if converted else 'Not Converted'
    rev_gen = round(cost * float(np.random.uniform(2.5, 8.0)), 2) if converted else 0.0
    
    campaign_list.append({
        'campaign_id': cmp_id,
        'customer_id': c_id,
        'campaign_type': cmp_type,
        'marketing_cost': cost,
        'conversion_status': conv_status,
        'revenue_generated': rev_gen
    })

marketing_df = pd.DataFrame(campaign_list)
marketing_df.to_csv(os.path.join(DATA_DIR, 'marketing_campaign.csv'), index=False)


# ---------------------------------------------------------
# 10. CUSTOMER REVIEWS DATASET
# ---------------------------------------------------------
print("10/10 Generating reviews.csv...")
positive_texts = [
    "Extremely satisfied with this purchase! Highly recommended.",
    "Great product quality and fast shipping. Will buy again.",
    "Exceeded my expectations! Excellent customer service.",
    "Very reliable product, works perfectly as described.",
    "Top notch quality and premium packaging."
]

negative_texts = [
    "Item arrived late and damaged. Dissatisfied with quality.",
    "Not worth the price. Stopped working after 3 days.",
    "Customer service was slow to respond to my refund query.",
    "Poor packaging and wrong color sent.",
    "Would not recommend. Cheap materials used."
]

reviews_list = []
for i in range(1, NUM_REVIEWS + 1):
    rev_id = f"REV-{i:06d}"
    c_id = random.choice(customer_ids)
    p_id = random.choice(products_df['product_id'])
    
    rating = np.random.choice([1, 2, 3, 4, 5], p=[0.10, 0.12, 0.18, 0.32, 0.28])
    if rating <= 2:
        text = random.choice(negative_texts)
    elif rating >= 4:
        text = random.choice(positive_texts)
    else:
        text = "Average product. Does the job but nothing extraordinary."
        
    reviews_list.append({
        'review_id': rev_id,
        'customer_id': c_id,
        'product_id': p_id,
        'rating': rating,
        'review_text': text
    })

reviews_df = pd.DataFrame(reviews_list)
reviews_df.to_csv(os.path.join(DATA_DIR, 'reviews.csv'), index=False)

print("\nSUCCESS! All 10 enterprise datasets successfully generated in 'data/raw/':")
for fname in os.listdir(DATA_DIR):
    fpath = os.path.join(DATA_DIR, fname)
    size_mb = os.path.getsize(fpath) / (1024 * 1024)
    print(f" - {fname} ({size_mb:.2f} MB)")
