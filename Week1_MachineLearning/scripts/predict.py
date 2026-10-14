#!/usr/bin/env python3
"""
ShopSmart Retail Analytics & AI Implementation
Mission ML01: Building Your First Machine Learning Models

Standalone Prediction Script (Task G)
- Loads serialized machine learning models and preprocessing pipelines
- Validates user input schema and values against training distributions
- Predicts continuous Order_Total (NGN) via Linear Regression
- Predicts Return Probability (%) and Return Flag via Logistic Regression
- Supports:
    1. CLI Arguments: pass parameters directly via terminal flags
    2. Demo Mode (--demo): evaluates representative test cases
    3. Interactive Mode (--interactive): guides user through terminal prompts
"""

import os
import sys
import argparse
import datetime
import joblib
import pandas as pd
import numpy as np

# Path configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

NUMERICAL_COLS = [
    'Quantity', 'Unit_Price', 'Discount', 'Shipping_Cost',
    'Customer_Age', 'Product_Cost_Price', 'Product_Catalog_Price',
    'Order_Month', 'Order_Day', 'Order_DayOfWeek', 'Order_Quarter', 'Is_Weekend'
]

CATEGORICAL_COLS = [
    'Customer_Gender', 'Customer_Segment', 'Product_Category',
    'Payment_Method', 'Sales_Channel', 'Store_Region', 'Order_Status'
]

ALL_FEATURE_COLS = NUMERICAL_COLS + CATEGORICAL_COLS

def load_artifacts():
    """
    Loads regression and classification pipelines.
    Falls back to individual components if pipeline is not found.
    """
    reg_pipe_path = os.path.join(MODELS_DIR, "linear_regression_pipeline.pkl")
    clf_pipe_path = os.path.join(MODELS_DIR, "logistic_regression_pipeline.pkl")
    
    if not os.path.exists(reg_pipe_path) or not os.path.exists(clf_pipe_path):
        # Check if individual components exist
        lr_path = os.path.join(MODELS_DIR, "linear_regression.pkl")
        clf_path = os.path.join(MODELS_DIR, "logistic_regression.pkl")
        scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
        encoder_path = os.path.join(MODELS_DIR, "encoder.pkl")
        
        missing = [p for p in [lr_path, clf_path, scaler_path, encoder_path] if not os.path.exists(p)]
        if missing:
            raise FileNotFoundError(
                f"Missing required model artifact(s): {missing}\n"
                "Please run 'python scripts/train_regression.py' and 'python scripts/train_classification.py' first."
            )
        
        print("[INFO] Loading individual model and preprocessor artifacts...")
        from sklearn.pipeline import Pipeline
        from sklearn.compose import ColumnTransformer
        
        scaler = joblib.load(scaler_path)
        encoder = joblib.load(encoder_path)
        reg_model = joblib.load(lr_path)
        clf_model = joblib.load(clf_path)
        
        preprocessor = ColumnTransformer([
            ('num', scaler, NUMERICAL_COLS),
            ('cat', encoder, CATEGORICAL_COLS)
        ])
        reg_pipe = Pipeline([('preprocessor', preprocessor), ('regressor', reg_model)])
        clf_pipe = Pipeline([('preprocessor', preprocessor), ('classifier', clf_model)])
    else:
        reg_pipe = joblib.load(reg_pipe_path)
        clf_pipe = joblib.load(clf_pipe_path)
        
    return reg_pipe, clf_pipe

def validate_and_prepare_input(data_dict):
    """
    Validates input fields, handles date parsing, applies sensible defaults,
    and returns a 1-row pandas DataFrame matching the training feature schema.
    """
    errors = []
    
    # Numerical validation
    try:
        quantity = int(data_dict.get('Quantity', 1))
        if quantity <= 0:
            errors.append("Quantity must be a positive integer greater than 0.")
    except (ValueError, TypeError):
        errors.append("Quantity must be a valid integer.")
        quantity = 1

    try:
        unit_price = float(data_dict.get('Unit_Price', 25000.0))
        if unit_price <= 0:
            errors.append("Unit_Price must be a positive number.")
    except (ValueError, TypeError):
        errors.append("Unit_Price must be a valid number.")
        unit_price = 25000.0

    try:
        discount = float(data_dict.get('Discount', 0.0))
        if discount < 0:
            errors.append("Discount cannot be negative.")
    except (ValueError, TypeError):
        errors.append("Discount must be a valid number.")
        discount = 0.0

    try:
        shipping_cost = float(data_dict.get('Shipping_Cost', 2500.0))
        if shipping_cost < 0:
            errors.append("Shipping_Cost cannot be negative.")
    except (ValueError, TypeError):
        errors.append("Shipping_Cost must be a valid number.")
        shipping_cost = 2500.0

    try:
        customer_age = int(data_dict.get('Customer_Age', 35))
        if not (10 <= customer_age <= 120):
            errors.append("Customer_Age must be between 10 and 120.")
    except (ValueError, TypeError):
        errors.append("Customer_Age must be a valid integer.")
        customer_age = 35

    product_cost_price = float(data_dict.get('Product_Cost_Price', unit_price * 0.65))
    product_catalog_price = float(data_dict.get('Product_Catalog_Price', unit_price))

    # Parse Date or use today's date
    date_val = data_dict.get('Order_Date', None)
    if date_val:
        try:
            order_dt = pd.to_datetime(date_val)
        except Exception:
            errors.append(f"Invalid date format: '{date_val}'. Use YYYY-MM-DD or M/D/YYYY.")
            order_dt = datetime.datetime.now()
    else:
        order_month = int(data_dict.get('Order_Month', datetime.datetime.now().month))
        order_day = int(data_dict.get('Order_Day', datetime.datetime.now().day))
        order_dayofweek = int(data_dict.get('Order_DayOfWeek', datetime.datetime.now().weekday()))
        order_quarter = int(data_dict.get('Order_Quarter', (order_month - 1) // 3 + 1))
        is_weekend = int(order_dayofweek in [5, 6])
        order_dt = None

    if order_dt is not None:
        order_month = order_dt.month
        order_day = order_dt.day
        order_dayofweek = order_dt.dayofweek
        order_quarter = order_dt.quarter
        is_weekend = int(order_dayofweek in [5, 6])

    # Categorical validation / defaults
    customer_gender = str(data_dict.get('Customer_Gender', 'Female')).capitalize()
    customer_segment = str(data_dict.get('Customer_Segment', 'Silver')).capitalize()
    product_category = str(data_dict.get('Product_Category', 'Electronics')).capitalize()
    payment_method = str(data_dict.get('Payment_Method', 'Card')).capitalize()
    sales_channel = str(data_dict.get('Sales_Channel', 'Online'))
    store_region = str(data_dict.get('Store_Region', 'South')).capitalize()
    order_status = str(data_dict.get('Order_Status', 'Completed')).capitalize()

    if errors:
        raise ValueError("Input Validation Error(s):\n  - " + "\n  - ".join(errors))

    # Build single-row DataFrame with the exact column order
    row_data = {
        'Quantity': [quantity],
        'Unit_Price': [unit_price],
        'Discount': [discount],
        'Shipping_Cost': [shipping_cost],
        'Customer_Age': [customer_age],
        'Product_Cost_Price': [product_cost_price],
        'Product_Catalog_Price': [product_catalog_price],
        'Order_Month': [order_month],
        'Order_Day': [order_day],
        'Order_DayOfWeek': [order_dayofweek],
        'Order_Quarter': [order_quarter],
        'Is_Weekend': [is_weekend],
        'Customer_Gender': [customer_gender],
        'Customer_Segment': [customer_segment],
        'Product_Category': [product_category],
        'Payment_Method': [payment_method],
        'Sales_Channel': [sales_channel],
        'Store_Region': [store_region],
        'Order_Status': [order_status]
    }
    
    return pd.DataFrame(row_data)

def predict(data_dict):
    """
    Executes inference using loaded pipelines and returns results dictionary.
    """
    reg_pipe, clf_pipe = load_artifacts()
    input_df = validate_and_prepare_input(data_dict)
    
    pred_order_total = float(reg_pipe.predict(input_df)[0])
    return_prob = float(clf_pipe.predict_proba(input_df)[0, 1])
    return_pred = int(clf_pipe.predict(input_df)[0])
    
    risk_level = "HIGH RISK" if return_prob >= 0.50 else "MODERATE / NORMAL RISK"
    
    return {
        "predicted_order_total": max(0.0, pred_order_total),
        "return_probability": return_prob,
        "predicted_return_flag": return_pred,
        "risk_level": risk_level,
        "input_features": input_df.to_dict(orient='records')[0]
    }

def print_result_card(res):
    """
    Formats the inference result into a clean terminal report card.
    """
    inputs = res['input_features']
    print("\n" + "=" * 65)
    print("           SHOPSMART AI INFERENCE ENGINE (ML01)")
    print("=" * 65)
    print("TRANSACTION DETAILS:")
    print(f"  * Quantity & Price : {inputs['Quantity']} unit(s) @ NGN {inputs['Unit_Price']:,.2f}")
    print(f"  * Discount & Ship  : NGN {inputs['Discount']:,.2f} disc | NGN {inputs['Shipping_Cost']:,.2f} shipping")
    print(f"  * Product Category : {inputs['Product_Category']}")
    print(f"  * Customer Profile : {inputs['Customer_Age']} yrs, {inputs['Customer_Gender']} ({inputs['Customer_Segment']} Tier)")
    print(f"  * Channel & Region : {inputs['Sales_Channel']} ({inputs['Payment_Method']}) in {inputs['Store_Region']} Region")
    print("-" * 65)
    print("MODEL PREDICTIONS:")
    print(f"  >> PREDICTED ORDER VALUE : NGN {res['predicted_order_total']:>14,.2f}")
    print(f"  >> RETURN PROBABILITY    : {res['return_probability']*100:>13.2f}%")
    print(f"  >> PREDICTED RETURN FLAG : {res['predicted_return_flag']:>14} ({res['risk_level']})")
    print("-" * 65)
    print("OPERATIONAL GUIDANCE:")
    if res['predicted_return_flag'] == 1:
        print("  [!] Flagged for return inspection. Ensure warranty documentation")
        print("      and return slip are automatically printed in package.")
    else:
        print("  [OK] Standard transaction. Expected to be retained by customer.")
    print("=" * 65 + "\n")

def run_demo():
    """
    Demonstrates prediction script on 3 diverse test examples.
    """
    print("=" * 65)
    print("RUNNING DEMO: 3 REALISTIC SHOPSMART TEST SCENARIOS")
    print("=" * 65)
    
    scenarios = [
        {
            "name": "Scenario 1: High-Value Online Electronics (Gold Customer)",
            "data": {
                'Quantity': 2,
                'Unit_Price': 85000.0,
                'Discount': 20.0,
                'Shipping_Cost': 3500.0,
                'Customer_Age': 42,
                'Customer_Gender': 'Male',
                'Customer_Segment': 'Gold',
                'Product_Category': 'Electronics',
                'Payment_Method': 'Card',
                'Sales_Channel': 'Online',
                'Store_Region': 'South',
                'Order_Status': 'Completed',
                'Order_Month': 8,
                'Order_Day': 15,
                'Order_DayOfWeek': 4,
                'Order_Quarter': 3,
                'Is_Weekend': 0
            }
        },
        {
            "name": "Scenario 2: Low-Value In-Store Groceries (Bronze Customer)",
            "data": {
                'Quantity': 4,
                'Unit_Price': 3500.0,
                'Discount': 5.0,
                'Shipping_Cost': 500.0,
                'Customer_Age': 26,
                'Customer_Gender': 'Female',
                'Customer_Segment': 'Bronze',
                'Product_Category': 'Groceries',
                'Payment_Method': 'Cash',
                'Sales_Channel': 'In-Store',
                'Store_Region': 'North',
                'Order_Status': 'Completed',
                'Order_Month': 3,
                'Order_Day': 10,
                'Order_DayOfWeek': 1,
                'Order_Quarter': 1,
                'Is_Weekend': 0
            }
        },
        {
            "name": "Scenario 3: Fashion Basket (Silver Customer, Eastern Store)",
            "data": {
                'Quantity': 3,
                'Unit_Price': 28000.0,
                'Discount': 10.0,
                'Shipping_Cost': 2000.0,
                'Customer_Age': 31,
                'Customer_Gender': 'Female',
                'Customer_Segment': 'Silver',
                'Product_Category': 'Fashion',
                'Payment_Method': 'Transfer',
                'Sales_Channel': 'Online',
                'Store_Region': 'East',
                'Order_Status': 'Pending',
                'Order_Month': 11,
                'Order_Day': 22,
                'Order_DayOfWeek': 5,
                'Order_Quarter': 4,
                'Is_Weekend': 1
            }
        }
    ]
    
    for sc in scenarios:
        print(f"\n---> {sc['name']}")
        res = predict(sc['data'])
        print_result_card(res)

def run_interactive():
    """
    Guides user interactively through terminal prompts.
    """
    print("\n" + "=" * 65)
    print("INTERACTIVE INFERENCE MODE — Enter transaction details")
    print("(Press Enter to accept suggested defaults)")
    print("=" * 65)
    
    def prompt_val(prompt_text, default):
        user_in = input(f"{prompt_text} [{default}]: ").strip()
        return user_in if user_in else default

    data = {
        'Quantity': int(prompt_val("Order Quantity (1-10)", "2")),
        'Unit_Price': float(prompt_val("Product Unit Price in NGN", "45000")),
        'Discount': float(prompt_val("Discount Amount (NGN)", "10")),
        'Shipping_Cost': float(prompt_val("Shipping Cost in NGN", "2500")),
        'Product_Category': prompt_val("Category (Beauty/Clothing/Electronics/Groceries/Home)", "Electronics"),
        'Customer_Age': int(prompt_val("Customer Age (18-70)", "34")),
        'Customer_Gender': prompt_val("Customer Gender (Male/Female)", "Female"),
        'Customer_Segment': prompt_val("Customer Segment (Bronze/Silver/Gold)", "Gold"),
        'Payment_Method': prompt_val("Payment Method (Card/Cash/Transfer)", "Card"),
        'Sales_Channel': prompt_val("Sales Channel (Online/In-Store)", "Online"),
        'Store_Region': prompt_val("Store Region (North/South/East/West)", "South"),
        'Order_Status': prompt_val("Order Status (Completed/Pending)", "Completed"),
        'Order_Date': prompt_val("Order Date (YYYY-MM-DD)", datetime.date.today().strftime("%Y-%m-%d"))
    }
    
    res = predict(data)
    print_result_card(res)

def main():
    parser = argparse.ArgumentParser(description="ShopSmart ML Inference Engine: Predict Order_Total and Return Probability")
    parser.add_argument("--demo", action="store_true", help="Run 3 diverse demo scenarios")
    parser.add_argument("--interactive", action="store_true", help="Run interactive terminal prompt")
    parser.add_argument("--quantity", type=int, default=None, help="Order item quantity")
    parser.add_argument("--unit_price", type=float, default=None, help="Product unit price (NGN)")
    parser.add_argument("--discount", type=float, default=None, help="Discount deducted (NGN)")
    parser.add_argument("--shipping_cost", type=float, default=None, help="Delivery shipping cost (NGN)")
    parser.add_argument("--category", type=str, default=None, help="Product Category")
    parser.add_argument("--age", type=int, default=None, help="Customer Age")
    parser.add_argument("--gender", type=str, default=None, help="Customer Gender")
    parser.add_argument("--segment", type=str, default=None, help="Customer Segment (Bronze/Silver/Gold)")
    parser.add_argument("--channel", type=str, default=None, help="Sales Channel (Online/In-Store)")
    parser.add_argument("--region", type=str, default=None, help="Store Region (North/South/East/West)")
    parser.add_argument("--payment", type=str, default=None, help="Payment Method (Card/Cash/Transfer)")

    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if args.interactive or len(sys.argv) == 1:
        # If no arguments provided in interactive environment or explicitly requested
        if sys.stdin.isatty():
            run_interactive()
        else:
            # Running headless or in automated test: execute demo
            print("[INFO] No CLI flags provided; running demonstration mode:")
            run_demo()
        return

    # Build input dict from CLI flags
    data = {}
    if args.quantity is not None: data['Quantity'] = args.quantity
    if args.unit_price is not None: data['Unit_Price'] = args.unit_price
    if args.discount is not None: data['Discount'] = args.discount
    if args.shipping_cost is not None: data['Shipping_Cost'] = args.shipping_cost
    if args.category is not None: data['Product_Category'] = args.category
    if args.age is not None: data['Customer_Age'] = args.age
    if args.gender is not None: data['Customer_Gender'] = args.gender
    if args.segment is not None: data['Customer_Segment'] = args.segment
    if args.channel is not None: data['Sales_Channel'] = args.channel
    if args.region is not None: data['Store_Region'] = args.region
    if args.payment is not None: data['Payment_Method'] = args.payment

    try:
        res = predict(data)
        print_result_card(res)
    except Exception as e:
        print(f"\n[ERROR] {e}\n", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
