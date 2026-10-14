"""
ShopSmart Retail Analytics & AI Implementation
Mission ML01: Building Your First Machine Learning Models

Data Preparation Pipeline (Task B)
- Loads and inspects all raw datasets
- Resolves schema, date parsing, and type conversions
- Performs safe relational joins avoiding Cartesian explosion
- Computes Line_Total and Order_Total without leakage
- Derives binary Return_Flag safely avoiding duplicates
- Splits data into train.csv (80%) and test.csv (20%) with stratification
- Fits preprocessing components (OneHotEncoder, StandardScaler) ONLY on training data
- Runs end-to-end validation checks
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def prepare_data():
    raw_dir = r"c:\Users\HyperX\Desktop\analystLab\Week1_MachineLearning\data\raw"
    data_dir = r"c:\Users\HyperX\Desktop\analystLab\Week1_MachineLearning\data"
    
    print("=" * 60)
    print("STEP 1: LOADING RAW DATASETS")
    print("=" * 60)
    customers = pd.read_csv(os.path.join(raw_dir, "Customers.csv"))
    products = pd.read_csv(os.path.join(raw_dir, "Products.csv"))
    stores = pd.read_csv(os.path.join(raw_dir, "Stores.csv"))
    orders = pd.read_csv(os.path.join(raw_dir, "Orders.csv"))
    order_items = pd.read_csv(os.path.join(raw_dir, "Order_Items.csv"))
    returns = pd.read_csv(os.path.join(raw_dir, "Returns.csv"))
    
    print(f"Loaded Orders:       {orders.shape}")
    print(f"Loaded Order_Items:  {order_items.shape}")
    print(f"Loaded Customers:    {customers.shape}")
    print(f"Loaded Products:     {products.shape}")
    print(f"Loaded Stores:       {stores.shape}")
    print(f"Loaded Returns:      {returns.shape}")

    print("\n" + "=" * 60)
    print("STEP 2: CLEANING & TYPE STANDARDIZATION")
    print("=" * 60)
    
    # 1. Parse Dates
    orders['Order_Date'] = pd.to_datetime(orders['Order_Date'], format='%m/%d/%Y', errors='coerce')
    customers['Registration_Date'] = pd.to_datetime(customers['Registration_Date'], format='%m/%d/%Y', errors='coerce')
    stores['Opening_Date'] = pd.to_datetime(stores['Opening_Date'], format='%m/%d/%Y', errors='coerce')
    
    # Check date parsing integrity
    assert orders['Order_Date'].isnull().sum() == 0, "Error: Null dates found in Orders!"
    assert customers['Registration_Date'].isnull().sum() == 0, "Error: Null dates found in Customers!"
    assert stores['Opening_Date'].isnull().sum() == 0, "Error: Null dates found in Stores!"
    print("[OK] All date columns successfully parsed to datetime64.")

    # 2. Extract Temporal Features from Order_Date
    orders['Order_Year'] = orders['Order_Date'].dt.year
    orders['Order_Month'] = orders['Order_Date'].dt.month
    orders['Order_Day'] = orders['Order_Date'].dt.day
    orders['Order_DayOfWeek'] = orders['Order_Date'].dt.dayofweek # 0=Mon, 6=Sun
    orders['Order_Quarter'] = orders['Order_Date'].dt.quarter
    orders['Is_Weekend'] = orders['Order_DayOfWeek'].isin([5, 6]).astype(int)
    print("[OK] Temporal features created: Order_Month, Order_Day, Order_DayOfWeek, Order_Quarter, Is_Weekend.")

    # 3. Clean Order Items & Verify Line_Total Formula
    # Formula: Line_Total = Quantity * Unit_Price - Discount
    calculated_line_total = orders['Quantity'] * orders['Unit_Price'] - orders['Discount']
    item_line_total = order_items.set_index('Order_ID')['Line_Total']
    orders['Line_Total'] = orders['Order_ID'].map(item_line_total)
    
    assert (orders['Line_Total'] == calculated_line_total).all(), "Discrepancy in Line_Total calculation!"
    print("[OK] Line_Total verified: 100% matches (Quantity * Unit_Price) - Discount.")

    # 4. Define Target 1: Order_Total
    # Total payable value of the order invoice including delivery fee
    orders['Order_Total'] = orders['Line_Total'] + orders['Shipping_Cost']
    print(f"[OK] Order_Total defined as Line_Total + Shipping_Cost. Mean: NGN {orders['Order_Total'].mean():,.2f}")

    # 5. Define Target 2: Return_Flag (Safely avoiding 1-to-many return duplicate records)
    returned_order_ids = set(returns['Order_ID'].dropna().unique())
    orders['Return_Flag'] = orders['Order_ID'].isin(returned_order_ids).astype(int)
    return_count = orders['Return_Flag'].sum()
    return_rate = (return_count / len(orders)) * 100
    print(f"[OK] Return_Flag created via set membership: {return_count:,} positive cases ({return_rate:.2f}% return rate).")

    print("\n" + "=" * 60)
    print("STEP 3: RELATIONAL JOINS INTO MASTER DATASET")
    print("=" * 60)
    
    # Prepare dimension tables with unambiguous column names
    customers_clean = customers.rename(columns={
        'City': 'Customer_City',
        'State': 'Customer_State',
        'Gender': 'Customer_Gender',
        'Age': 'Customer_Age'
    })[['Customer_ID', 'Customer_Gender', 'Customer_Age', 'Customer_City', 'Customer_State', 'Customer_Segment', 'Registration_Date']]
    
    products_clean = products.rename(columns={
        'Category': 'Product_Category',
        'Sub_Category': 'Product_Sub_Category',
        'Brand': 'Product_Brand',
        'Cost_Price': 'Product_Cost_Price',
        'Selling_Price': 'Product_Catalog_Price'
    })[['Product_ID', 'Product_Name', 'Product_Category', 'Product_Brand', 'Product_Cost_Price', 'Product_Catalog_Price']]
    
    stores_clean = stores.rename(columns={
        'Store_Name': 'Store_Name',
        'Region': 'Store_Region',
        'State': 'Store_State',
        'City': 'Store_City',
        'Opening_Date': 'Store_Opening_Date'
    })[['Store_ID', 'Store_Name', 'Store_Region', 'Store_State', 'Store_City', 'Store_Opening_Date']]

    # Join dimensions onto Orders (Order Level Granularity: 50,000 rows)
    master_df = orders.merge(customers_clean, on='Customer_ID', how='inner')
    assert len(master_df) == 50000, f"Customer join altered row count to {len(master_df)}"
    
    master_df = master_df.merge(products_clean, on='Product_ID', how='inner')
    assert len(master_df) == 50000, f"Product join altered row count to {len(master_df)}"
    
    master_df = master_df.merge(stores_clean, on='Store_ID', how='inner')
    assert len(master_df) == 50000, f"Store join altered row count to {len(master_df)}"

    # Feature Engineering: Profit and Margin
    master_df['Gross_Profit'] = master_df['Line_Total'] - (master_df['Quantity'] * master_df['Product_Cost_Price'])
    master_df['Profit_Margin'] = (master_df['Gross_Profit'] / master_df['Line_Total']).round(4)
    
    # Verify no nulls across master dataset
    assert master_df.isnull().sum().sum() == 0, "Null values detected in master dataset!"
    assert master_df['Order_ID'].nunique() == 50000, "Duplicate Order_IDs detected in master dataset!"
    print(f"[OK] Master Dataset built successfully: {master_df.shape[0]:,} rows x {master_df.shape[1]} columns.")
    
    # Save master_dataset.csv
    master_path = os.path.join(data_dir, "master_dataset.csv")
    master_df.to_csv(master_path, index=False)
    print(f"[OK] Saved: {master_path} ({os.path.getsize(master_path):,} bytes)")

    print("\n" + "=" * 60)
    print("STEP 4: TRAIN / TEST SPLIT (80% / 20%)")
    print("=" * 60)
    
    train_df, test_df = train_test_split(
        master_df,
        test_size=0.20,
        random_state=42,
        stratify=master_df['Return_Flag']
    )
    
    print(f"Train set: {train_df.shape[0]:,} rows (Returns: {train_df['Return_Flag'].sum():,}, {train_df['Return_Flag'].mean()*100:.2f}%)")
    print(f"Test set:  {test_df.shape[0]:,} rows (Returns: {test_df['Return_Flag'].sum():,}, {test_df['Return_Flag'].mean()*100:.2f}%)")
    
    train_path = os.path.join(data_dir, "train.csv")
    test_path = os.path.join(data_dir, "test.csv")
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    print(f"[OK] Saved: {train_path}")
    print(f"[OK] Saved: {test_path}")

    print("\n" + "=" * 60)
    print("STEP 5: PREPROCESSING PIPELINE VALIDATION (NO LEAKAGE)")
    print("=" * 60)
    
    # Define modeling features (prediction-time features)
    numerical_features = [
        'Quantity', 'Unit_Price', 'Discount', 'Shipping_Cost',
        'Customer_Age', 'Product_Cost_Price', 'Product_Catalog_Price',
        'Order_Month', 'Order_Day', 'Order_DayOfWeek', 'Order_Quarter', 'Is_Weekend'
    ]
    
    categorical_features = [
        'Customer_Gender', 'Customer_Segment', 'Product_Category',
        'Payment_Method', 'Sales_Channel', 'Store_Region', 'Order_Status'
    ]
    
    print(f"Numerical features ({len(numerical_features)}): {numerical_features}")
    print(f"Categorical features ({len(categorical_features)}): {categorical_features}")

    # Fit Scaler strictly on X_train numerical
    scaler = StandardScaler()
    scaler.fit(train_df[numerical_features])
    X_train_num_scaled = scaler.transform(train_df[numerical_features])
    X_test_num_scaled = scaler.transform(test_df[numerical_features])
    
    # Fit OneHotEncoder strictly on X_train categorical
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoder.fit(train_df[categorical_features])
    X_train_cat_encoded = encoder.transform(train_df[categorical_features])
    X_test_cat_encoded = encoder.transform(test_df[categorical_features])
    
    # Combine feature matrices
    X_train_proc = np.hstack([X_train_num_scaled, X_train_cat_encoded])
    X_test_proc = np.hstack([X_test_num_scaled, X_test_cat_encoded])
    
    print(f"[OK] Preprocessing verified: X_train shape = {X_train_proc.shape}, X_test shape = {X_test_proc.shape}")
    print(f"[OK] Scaler fitted strictly on train: mean={scaler.mean_[:3].round(2)}")
    print(f"[OK] Encoder fitted strictly on train: {len(encoder.get_feature_names_out())} encoded dummy features")

    print("\n" + "=" * 60)
    print("STEP 6: VALIDATION INTEGRITY REPORT")
    print("=" * 60)
    print("1. Master Dataset Rows:       50,000 (Exact 1:1 match with Orders.csv)")
    print("2. Master Dataset Duplicates: 0")
    print("3. Master Dataset Nulls:      0")
    print("4. Train Set Rows:            40,000 (80.0%)")
    print("5. Test Set Rows:             10,000 (20.0%)")
    print(f"6. Train Target 1 (Mean):     NGN {train_df['Order_Total'].mean():,.2f}")
    print(f"7. Test Target 1 (Mean):      NGN {test_df['Order_Total'].mean():,.2f}")
    print(f"8. Train Target 2 (Rate):     {train_df['Return_Flag'].mean()*100:.2f}%")
    print(f"9. Test Target 2 (Rate):      {test_df['Return_Flag'].mean()*100:.2f}%")
    print("10. Target Leakage Exclusions: Excluded Return_Reason, Refund_Amount, Return_Date")
    print("11. ID Column Exclusions:      Excluded Order_ID, Customer_ID, Product_ID, Store_ID from feature matrix")
    print("12. Data Leakage Prevention:   Preprocessing fitted exclusively on training set.")
    print("=" * 60)
    print("ALL VALIDATION CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    prepare_data()
