"""
ShopSmart Retail Analytics & AI Implementation
Mission ML01: Building Your First Machine Learning Models

Task C: Linear Regression Model for Order_Total Prediction
- Verifies target variable is numeric and clean
- Verifies input features are strictly prediction-time available
- Trains LinearRegression on training set (40,000 orders)
- Compares against DummyRegressor (mean baseline)
- Evaluates on untouched test set (10,000 orders): MAE, RMSE, R²
- Generates publication-grade Actual vs. Predicted and Residual plots
- Analyzes feature coefficients
- Serializes trained model and preprocessing artifacts using joblib
"""

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

def train_and_evaluate_regression():
    base_dir = r"c:\Users\HyperX\Desktop\analystLab\Week1_MachineLearning"
    data_dir = os.path.join(base_dir, "data")
    models_dir = os.path.join(base_dir, "models")
    fig_dir = os.path.join(base_dir, "reports", "figures")
    
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    
    print("=" * 65)
    print("STEP 1: LOADING DATA & VERIFYING TARGET INTEGRITY")
    print("=" * 65)
    
    train_df = pd.read_csv(os.path.join(data_dir, "train.csv"))
    test_df = pd.read_csv(os.path.join(data_dir, "test.csv"))
    
    print(f"Loaded Train: {train_df.shape[0]:,} rows x {train_df.shape[1]} columns")
    print(f"Loaded Test:  {test_df.shape[0]:,} rows x {test_df.shape[1]} columns")
    
    target_col = "Order_Total"
    assert target_col in train_df.columns, f"Target '{target_col}' missing from train set!"
    assert target_col in test_df.columns, f"Target '{target_col}' missing from test set!"
    
    # Check numeric types and clean values
    assert pd.api.types.is_numeric_dtype(train_df[target_col]), "Target is not numeric!"
    assert train_df[target_col].isnull().sum() == 0, "Target has nulls in train!"
    assert test_df[target_col].isnull().sum() == 0, "Target has nulls in test!"
    assert not np.isinf(train_df[target_col]).any(), "Target has inf values in train!"
    assert not np.isinf(test_df[target_col]).any(), "Target has inf values in test!"
    
    print(f"[OK] Target '{target_col}' verified as numeric and clean.")
    print(f"     Train Target: Min=NGN {train_df[target_col].min():,.2f}, Max=NGN {train_df[target_col].max():,.2f}, Mean=NGN {train_df[target_col].mean():,.2f}")
    print(f"     Test Target:  Min=NGN {test_df[target_col].min():,.2f}, Max=NGN {test_df[target_col].max():,.2f}, Mean=NGN {test_df[target_col].mean():,.2f}")

    print("\n" + "=" * 65)
    print("STEP 2: DEFINING PREDICTION-TIME FEATURES")
    print("=" * 65)
    
    numerical_features = [
        'Quantity', 'Unit_Price', 'Discount', 'Shipping_Cost',
        'Customer_Age', 'Product_Cost_Price', 'Product_Catalog_Price',
        'Order_Month', 'Order_Day', 'Order_DayOfWeek', 'Order_Quarter', 'Is_Weekend'
    ]
    
    categorical_features = [
        'Customer_Gender', 'Customer_Segment', 'Product_Category',
        'Payment_Method', 'Sales_Channel', 'Store_Region', 'Order_Status'
    ]
    
    all_features = numerical_features + categorical_features
    print(f"[OK] Selected {len(all_features)} input features ({len(numerical_features)} numerical, {len(categorical_features)} categorical).")
    print("[OK] Verified exclusion of target leakage: Line_Total, Return_Flag, Return_Reason, Refund_Amount, Return_Date.")
    print("[OK] Verified exclusion of IDs/PII: Order_ID, Customer_ID, Product_ID, Store_ID, First_Name, Last_Name, Email, Phone.")

    X_train = train_df[all_features]
    y_train = train_df[target_col]
    X_test = test_df[all_features]
    y_test = test_df[target_col]

    print("\n" + "=" * 65)
    print("STEP 3: BUILDING PIPELINE & TRAINING LINEAR REGRESSION")
    print("=" * 65)
    
    # Preprocessor using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), categorical_features)
        ]
    )
    
    # Fit preprocessor on X_train only to extract standalone scaler and encoder for Task F
    scaler = StandardScaler().fit(train_df[numerical_features])
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore').fit(train_df[categorical_features])
    
    # Create complete Pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    
    # Baseline Model: DummyRegressor predicting mean
    baseline_model = DummyRegressor(strategy='mean')
    baseline_model.fit(X_train, y_train)
    y_pred_baseline = baseline_model.predict(X_test)
    
    # Train Linear Regression Pipeline
    pipeline.fit(X_train, y_train)
    y_pred_train = pipeline.predict(X_train)
    y_pred_test = pipeline.predict(X_test)
    print("[OK] Linear Regression model trained successfully on 40,000 orders.")

    print("\n" + "=" * 65)
    print("STEP 4: EVALUATION METRICS (TEST SET VS BASELINE)")
    print("=" * 65)
    
    # Baseline metrics
    base_mae = mean_absolute_error(y_test, y_pred_baseline)
    base_rmse = np.sqrt(mean_squared_error(y_test, y_pred_baseline))
    base_r2 = r2_score(y_test, y_pred_baseline)
    
    # Linear Regression Train metrics
    train_mae = mean_absolute_error(y_train, y_pred_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    train_r2 = r2_score(y_train, y_pred_train)
    
    # Linear Regression Test metrics
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    test_r2 = r2_score(y_test, y_pred_test)
    
    print(f"{'Metric':<10} | {'Baseline (Mean)':<18} | {'Linear Reg (Train)':<20} | {'Linear Reg (Test)':<18}")
    print("-" * 75)
    print(f"{'MAE':<10} | NGN {base_mae:>14,.2f} | NGN {train_mae:>16,.2f} | NGN {test_mae:>14,.2f}")
    print(f"{'RMSE':<10} | NGN {base_rmse:>14,.2f} | NGN {train_rmse:>16,.2f} | NGN {test_rmse:>14,.2f}")
    print(f"{'R² Score':<10} | {base_r2:>18.4f} | {train_r2:>20.4f} | {test_r2:>18.4f}")
    print("-" * 75)
    
    # Improvement over baseline
    mae_reduction = ((base_mae - test_mae) / base_mae) * 100
    rmse_reduction = ((base_rmse - test_rmse) / base_rmse) * 100
    print(f"Error Reduction vs Baseline: MAE reduced by {mae_reduction:.1f}%, RMSE reduced by {rmse_reduction:.1f}%.")

    print("\n" + "=" * 65)
    print("STEP 5: FEATURE IMPORTANCE (STANDARDIZED COEFFICIENTS)")
    print("=" * 65)
    
    reg_model = pipeline.named_steps['regressor']
    cat_names = pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
    feature_names = numerical_features + list(cat_names)
    coefficients = reg_model.coef_
    
    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefficients,
        'Abs_Coefficient': np.abs(coefficients)
    }).sort_values('Abs_Coefficient', ascending=False)
    
    print("Top 10 Most Influential Features:")
    for idx, r in coef_df.head(10).reset_index(drop=True).iterrows():
        print(f"  {idx+1:>2}. {r['Feature']:<32}: {r['Coefficient']:>14,.2f}")

    print("\n" + "=" * 65)
    print("STEP 6: GENERATING DIAGNOSTIC PLOTS")
    print("=" * 65)
    
    residuals = y_test - y_pred_test
    
    # Plot 1: Actual vs Predicted
    fig, ax = plt.subplots(figsize=(8, 7), dpi=300)
    # Scatter sample 2,000 points for clean visual rendering
    sample_indices = np.random.choice(len(y_test), size=min(2000, len(y_test)), replace=False)
    ax.scatter(y_test.iloc[sample_indices], y_pred_test[sample_indices], alpha=0.35, color='#1f77b4', edgecolor='none', s=25, label='Test Observations')
    
    # 45-degree reference line
    min_val = min(y_test.min(), y_pred_test.min())
    max_val = max(y_test.max(), y_pred_test.max())
    ax.plot([min_val, max_val], [min_val, max_val], color='#d62728', linestyle='--', linewidth=2, label='Perfect Fit Line (y = x)')
    
    ax.set_title("Actual vs. Predicted Order_Total (Linear Regression)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Actual Order_Total (NGN)", fontsize=11, labelpad=8)
    ax.set_ylabel("Predicted Order_Total (NGN)", fontsize=11, labelpad=8)
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x/1e3):,}k"))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x/1e3):,}k"))
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')
    
    # Add metric annotations
    stats_text = f"Test R²: {test_r2:.4f}\nMAE: NGN {test_mae:,.0f}\nRMSE: NGN {test_rmse:,.0f}"
    ax.text(0.95, 0.08, stats_text, transform=ax.transAxes, fontsize=10, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#ced4da', alpha=0.95))
    
    plt.tight_layout()
    actual_vs_pred_path = os.path.join(fig_dir, "actual_vs_predicted_regression.png")
    fig.savefig(actual_vs_pred_path, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Saved: {actual_vs_pred_path}")

    # Plot 2: Residual Plot (Residuals vs Predicted + Residual Distribution)
    fig, (ax_res, ax_hist) = plt.subplots(1, 2, figsize=(14, 6), dpi=300, gridspec_kw={'width_ratios': [3, 1]})
    
    ax_res.scatter(y_pred_test[sample_indices], residuals.iloc[sample_indices], alpha=0.35, color='#2ca02c', edgecolor='none', s=25)
    ax_res.axhline(0, color='#d62728', linestyle='--', linewidth=2)
    ax_res.set_title("Residual Plot (Errors vs. Predicted Values)", fontsize=13, fontweight='bold', pad=12)
    ax_res.set_xlabel("Predicted Order_Total (NGN)", fontsize=11, labelpad=8)
    ax_res.set_ylabel("Residuals (Actual - Predicted, NGN)", fontsize=11, labelpad=8)
    ax_res.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x/1e3):,}k"))
    ax_res.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x/1e3):,}k"))
    
    # Histogram of residuals
    sns.histplot(residuals, kde=True, ax=ax_hist, color='#2ca02c', bins=40, orientation='vertical')
    ax_hist.axhline(0, color='#d62728', linestyle='--', linewidth=2)
    ax_hist.set_title("Residual Distribution", fontsize=11, fontweight='bold', pad=12)
    ax_hist.set_xlabel("Count", fontsize=10)
    ax_hist.get_yaxis().set_ticklabels([])
    
    plt.tight_layout()
    residual_plot_path = os.path.join(fig_dir, "residual_plot_regression.png")
    fig.savefig(residual_plot_path, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Saved: {residual_plot_path}")

    print("\n" + "=" * 65)
    print("STEP 7: MODEL & PREPROCESSOR PERSISTENCE (TASK F REQUIREMENT)")
    print("=" * 65)
    
    # Save required individual artifacts as per official assignment:
    # linear_regression.pkl, scaler.pkl, encoder.pkl
    lr_path = os.path.join(models_dir, "linear_regression.pkl")
    scaler_path = os.path.join(models_dir, "scaler.pkl")
    encoder_path = os.path.join(models_dir, "encoder.pkl")
    pipeline_path = os.path.join(models_dir, "linear_regression_pipeline.pkl")
    
    joblib.dump(reg_model, lr_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(encoder, encoder_path)
    joblib.dump(pipeline, pipeline_path)
    
    print(f"[OK] Saved: {lr_path}")
    print(f"[OK] Saved: {scaler_path}")
    print(f"[OK] Saved: {encoder_path}")
    print(f"[OK] Saved: {pipeline_path}")
    
    print("\n" + "=" * 65)
    print("TASK C REGRESSION COMPLETE!")
    print("=" * 65)

if __name__ == "__main__":
    train_and_evaluate_regression()
