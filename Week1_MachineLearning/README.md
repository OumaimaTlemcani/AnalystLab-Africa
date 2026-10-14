# ShopSmart Retail Analytics & AI Implementation
## Mission ML01 — Building Your First Machine Learning Models
**AnalystLab Africa | Week 1 | Batch F**

---

## 📋 Project Overview

This project delivers a complete Machine Learning solution for **ShopSmart Retail Ltd.**, a multi-location Nigerian retail chain. Using historical transaction data spanning 50,000 orders across 9 relational datasets, we build and deploy two predictive models:

| Task | Model | Target | Business Use |
|------|-------|--------|--------------|
| Regression | Linear Regression | `Order_Total` (NGN) | Revenue forecasting & cash-flow planning |
| Classification | Logistic Regression | `Return_Flag` (0/1) | Return-risk detection & proactive inventory staging |

---

## 📁 Project Structure

```
Week1_MachineLearning/
│
├── ML01_Foundations.ipynb       # Main deliverable: full analysis notebook
│
├── data/
│   ├── raw/                     # Original 9 CSV + Data Dictionary.xlsx
│   │   ├── Customers.csv
│   │   ├── Products.csv
│   │   ├── Orders.csv
│   │   ├── Stores.csv
│   │   ├── Returns.csv
│   │   ├── Order_Items.csv
│   │   ├── Inventory.csv
│   │   ├── Employees.csv
│   │   ├── Suppliers.csv
│   │   └── Data Dictionary.xlsx
│   ├── master_dataset.csv       # Merged, cleaned dataset (50,000 rows)
│   ├── train.csv                # Training split (80% → 40,000 rows)
│   └── test.csv                 # Test split (20% → 10,000 rows)
│
├── models/
│   ├── linear_regression_pipeline.pkl    # Full regression pipeline
│   ├── logistic_regression_pipeline.pkl  # Full classification pipeline
│   ├── linear_regression.pkl             # Regression model only
│   ├── logistic_regression.pkl           # Classification model only
│   ├── scaler.pkl                        # StandardScaler artifact
│   └── encoder.pkl                       # OneHotEncoder artifact
│
├── reports/
│   ├── ML_Report.pdf            # Formal business report (PDF)
│   └── figures/
│       ├── actual_vs_predicted_regression.png
│       ├── residual_plot_regression.png
│       ├── confusion_matrix.png
│       └── roc_pr_curve.png
│
├── scripts/
│   ├── predict.py               # Standalone inference script (Task G)
│   ├── prepare_data.py          # Data cleaning & feature engineering
│   ├── train_regression.py      # Linear Regression training script
│   └── train_classification.py  # Logistic Regression training script
│
├── requirements.txt             # Python dependencies
└── .gitignore
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### 1. Clone / Download the project
```bash
# Navigate to the project folder
cd Week1_MachineLearning
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### Option A: Jupyter Notebook (Recommended)
Open `ML01_Foundations.ipynb` in Jupyter Lab / Jupyter Notebook / VS Code.
All 25 cells are pre-executed with saved outputs. Re-run them top-to-bottom to reproduce all results.

```bash
jupyter notebook ML01_Foundations.ipynb
```

### Option B: Standalone Training Scripts
```bash
# Step 1: Prepare data
python scripts/prepare_data.py

# Step 2: Train regression model
python scripts/train_regression.py

# Step 3: Train classification model
python scripts/train_classification.py
```

### Option C: Inference Only (predict.py)
```bash
# Demo mode — runs 3 realistic ShopSmart scenarios
python scripts/predict.py --demo

# CLI mode — specify a single transaction
python scripts/predict.py \
  --quantity 2 \
  --unit_price 85000 \
  --discount 20 \
  --shipping_cost 3500 \
  --customer_age 42 \
  --customer_gender Male \
  --customer_segment Gold \
  --product_category Electronics \
  --product_cost_price 55000 \
  --product_catalog_price 90000 \
  --payment_method Card \
  --sales_channel Online \
  --store_region South \
  --order_status Completed \
  --order_month 8 \
  --order_day 15 \
  --order_dayofweek 2 \
  --order_quarter 3 \
  --is_weekend 0

# Interactive mode — guided terminal prompts
python scripts/predict.py --interactive
```

---

## 📊 Model Performance

### Regression — Predicting `Order_Total`

| Metric | Baseline (Mean) | Linear Regression |
|--------|-----------------|-------------------|
| MAE    | NGN 97,868      | **NGN 29,575**    |
| RMSE   | NGN 119,494     | **NGN 40,088**    |
| R²     | −0.0002         | **0.8874**        |

> **Interpretation:** The model explains **88.7%** of variance in order value, reducing prediction error by ~70% versus a naïve baseline. Average prediction error is ±NGN 29,575.

### Classification — Predicting `Return_Flag`

| Metric    | Value  | Notes |
|-----------|--------|-------|
| Accuracy  | 51.6%  | Lower than 95.1% majority-class dummy — model deliberately trades accuracy for recall |
| Precision | 4.65%  | 4.65% of flagged orders are true returns |
| Recall    | 45.7%  | Catches **45.7% of all actual returns** |
| F1-Score  | 0.0844 |  |
| ROC-AUC   | 0.4912 | Near-random; reflects uniform synthetic return labels in dataset |

> **Interpretation:** The classifier is optimised for **recall** (minimising missed returns) rather than precision, which is appropriate in retail operations where the cost of missing a return exceeds the cost of a false flag. The near-random ROC-AUC reflects that the synthetic dataset does not encode meaningful return predictors — a known data limitation.

---

## 🔑 Key Feature Importance

### Regression — Top Drivers of Order Value
1. **Unit_Price** (+NGN 85,880 per std unit) — dominant ticket driver
2. **Quantity** (+NGN 71,292 per std unit) — basket volume multiplier
3. **Shipping_Cost** (+NGN 1,334) — logistics pass-through

### Classification — Top Return Risk Factors
1. **Order_Month** (OR: 1.11) — late-year seasonal surge
2. **Product_Catalog_Price** (OR: 1.10) — premium items returned slightly more
3. **Store_Region_East** (OR: 1.09) — marginally elevated return risk in Eastern stores

---

## 💼 Business Questions (Part 7 Summary)

| # | Question | Key Finding |
|---|----------|-------------|
| 1 | Which variables predict customer spending? | Unit_Price & Quantity dominate; Gold segment adds ~NGN 468 lift |
| 2 | What drives product returns? | Seasonal month, premium pricing, Eastern region |
| 3 | Which category is most predictable? | Beauty (MAPE: 0.71); Home least predictable (0.83) |
| 4 | Revenue by customer group? | Silver: NGN 154,579 avg · Gold: NGN 154,093 avg · Bronze: NGN 154,084 avg |
| 5 | Top 5 revenue-generating stores? | STR015 Lagos North (NGN 317.7M), STR021 Lagos West (NGN 316.8M) |
| 6 | Business applications? | Revenue forecasting, return staging, loyalty targeting |
| 7 | Model limitations? | Linear assumption; synthetic uniform returns cap AUC near 0.50 |
| 8 | Additional data needed? | Customer return history, product fit reviews, logistics delay logs |

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | ≥2.0.0 | Data manipulation |
| numpy | ≥1.24.0 | Numerical computing |
| matplotlib | ≥3.7.0 | Plotting |
| seaborn | ≥0.12.0 | Statistical visualisation |
| scikit-learn | ≥1.3.0 | ML models & pipelines |
| joblib | ≥1.3.0 | Model serialisation |
| openpyxl | ≥3.1.0 | Excel data dictionary reading |
| reportlab | ≥4.0.0 | PDF report generation |
| python-pptx | ≥0.6.21 | PowerPoint report generation |
| ipykernel | ≥6.20.0 | Jupyter notebook support |

---

## 🗃️ Dataset Overview

| Dataset | Rows | Key Columns | Role |
|---------|------|-------------|------|
| Orders.csv | 50,000 | Order_ID, Customer_ID, Order_Date, Order_Total | Transaction backbone |
| Order_Items.csv | 50,000 | Order_ID, Product_ID, Quantity, Unit_Price | Line-item detail |
| Customers.csv | 5,000 | Customer_ID, Age, Gender, Segment | Customer demographics |
| Products.csv | 500 | Product_ID, Category, Cost_Price, Catalog_Price | Product metadata |
| Stores.csv | 30 | Store_ID, Name, Region | Location reference |
| Returns.csv | ~2,440 | Return_ID, Order_ID, Return_Date | Return event log |
| Inventory.csv | 500 | Product_ID, Stock_Level | Stock data |
| Employees.csv | 100 | Employee_ID, Store_ID | Staff data |
| Suppliers.csv | 50 | Supplier_ID, Product_ID | Supply chain |

---

## 👤 Author

**AnalystLab Africa — Week 1 ML Intern**
*Experience Lab Internship Programme | Batch F*
*Mission ML01: Building Your First Machine Learning Models*

---

## 📄 License

This project is submitted as part of the **AnalystLab Africa Internship Programme** and is intended for educational evaluation purposes only.
