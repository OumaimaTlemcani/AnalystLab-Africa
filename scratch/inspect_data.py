import pandas as pd
import numpy as np
import os

raw_dir = r"c:\Users\HyperX\Desktop\analystLab\Week1_MachineLearning\data\raw"
orders = pd.read_csv(os.path.join(raw_dir, "Orders.csv"))
items = pd.read_csv(os.path.join(raw_dir, "Order_Items.csv"))
returns = pd.read_csv(os.path.join(raw_dir, "Returns.csv"))
products = pd.read_csv(os.path.join(raw_dir, "Products.csv"))
customers = pd.read_csv(os.path.join(raw_dir, "Customers.csv"))
stores = pd.read_csv(os.path.join(raw_dir, "Stores.csv"))

print("=== CHECKING ORDERS vs ORDER_ITEMS ===")
print("Orders shape:", orders.shape)
print("Items shape:", items.shape)
print("Order_ID 1:1 match:", (orders['Order_ID'] == items['Order_ID']).all())

# Check how Order_Total or Line_Total relates
diff_line = (items['Quantity'] * items['Unit_Price'] - items['Discount']) - items['Line_Total']
print("Max abs difference between (Qty*Price - Discount) and Line_Total:", diff_line.abs().max())

# Check if Order_Total is Line_Total or Line_Total + Shipping_Cost
# In the prompt: Task C says 'target Order_Total'
# Let's check returns
print("\n=== RETURNS CHECK ===")
ret_orders = returns.merge(orders, on='Order_ID').merge(items, on='Order_ID')
print("Returned orders count:", len(returns))
print("Sample refunds vs Line_Total vs Shipping:")
for _, r in ret_orders.head(5).iterrows():
    print(f"Order: {r['Order_ID']}, Refund: {r['Refund_Amount']}, Line_Total: {r['Line_Total']}, Shipping: {r['Shipping_Cost']}")

print("\n=== DATE RANGES ===")
print("Order_Date range:", orders['Order_Date'].min(), "to", orders['Order_Date'].max())
print("Return_Date range:", returns['Return_Date'].min(), "to", returns['Return_Date'].max())
