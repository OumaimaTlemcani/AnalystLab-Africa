import pandas as pd
import numpy as np
import os

raw_dir = r"c:\Users\HyperX\Desktop\analystLab\Week1_MachineLearning\data\raw"

files = [
    "Customers.csv",
    "Products.csv",
    "Stores.csv",
    "Orders.csv",
    "Order_Items.csv",
    "Returns.csv",
    "Employees.csv",
    "Suppliers.csv",
    "Inventory.csv"
]

dfs = {}
print("=== LOADING AND BASIC CHECKS ===")
for f in files:
    path = os.path.join(raw_dir, f)
    df = pd.read_csv(path)
    dfs[f] = df
    print(f"\n--- {f} ---")
    print(f"Rows: {len(df):,}, Cols: {len(df.columns)}")
    print("Duplicate rows:", df.duplicated().sum())
    
    # Missing values
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if len(null_cols) == 0:
        print("Missing values: None (0 across all columns)")
    else:
        print("Missing values by column:")
        print(null_cols)
        
    # Column details
    for col in df.columns:
        n_unique = df[col].nunique()
        dtype = df[col].dtype
        is_pk_candidate = (n_unique == len(df)) and (df[col].isnull().sum() == 0)
        pk_str = " [CANDIDATE PRIMARY KEY - 100% Unique]" if is_pk_candidate else ""
        sample_val = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else "N/A"
        print(f"  - {col} ({dtype}): {n_unique:,} unique values, sample='{sample_val}'{pk_str}")

print("\n=== FOREIGN KEY VERIFICATION ===")
# Check Orders foreign keys
print("Orders.Customer_ID in Customers.Customer_ID:", dfs["Orders.csv"]["Customer_ID"].isin(dfs["Customers.csv"]["Customer_ID"]).all())
print("Orders.Product_ID in Products.Product_ID:", dfs["Orders.csv"]["Product_ID"].isin(dfs["Products.csv"]["Product_ID"]).all())
print("Orders.Store_ID in Stores.Store_ID:", dfs["Orders.csv"]["Store_ID"].isin(dfs["Stores.csv"]["Store_ID"]).all())

# Check Order_Items foreign keys
print("Order_Items.Order_ID in Orders.Order_ID:", dfs["Order_Items.csv"]["Order_ID"].isin(dfs["Orders.csv"]["Order_ID"]).all())
print("Order_Items.Product_ID in Products.Product_ID:", dfs["Order_Items.csv"]["Product_ID"].isin(dfs["Products.csv"]["Product_ID"]).all())

# Check Returns foreign keys
print("Returns.Order_ID in Orders.Order_ID:", dfs["Returns.csv"]["Order_ID"].isin(dfs["Orders.csv"]["Order_ID"]).all())

# Check Employees foreign keys
print("Employees.Store_ID in Stores.Store_ID:", dfs["Employees.csv"]["Store_ID"].isin(dfs["Stores.csv"]["Store_ID"]).all())

# Check Inventory foreign keys
print("Inventory.Product_ID in Products.Product_ID:", dfs["Inventory.csv"]["Product_ID"].isin(dfs["Products.csv"]["Product_ID"]).all())
print("Inventory.Store_ID in Stores.Store_ID:", dfs["Inventory.csv"]["Store_ID"].isin(dfs["Stores.csv"]["Store_ID"]).all())

# Check Products and Suppliers
print("\n=== PRODUCTS VS SUPPLIERS ===")
print("Products brands sample:", dfs["Products.csv"]["Brand"].head(5).tolist())
print("Suppliers names sample:", dfs["Suppliers.csv"]["Supplier_Name"].head(5).tolist())
# Check if supplier links to brand or if Supplier_ID exists in products
print("Is Supplier_ID in Products?", "Supplier_ID" in dfs["Products.csv"].columns)
# Check supplier match with brand: e.g. "Zuniga PLC" vs "Zuniga PLC Supplies"
brand_supplier_match = dfs["Products.csv"]["Brand"].apply(lambda b: dfs["Suppliers.csv"]["Supplier_Name"].str.startswith(b).any())
print(f"Products with brand prefix matching Supplier_Name: {brand_supplier_match.sum()} / {len(dfs['Products.csv'])}")

print("\n=== DATA DICTIONARY CONTENTS ===")
dd_path = os.path.join(raw_dir, "Data Dictionary.xlsx")
dd = pd.read_csv(dd_path)
print(dd.to_string())
