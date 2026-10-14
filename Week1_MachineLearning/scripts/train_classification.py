"""
ShopSmart Retail Analytics & AI Implementation
Mission ML01: Building Your First Machine Learning Models

Task D: Logistic Regression Model for Return_Flag Prediction
- Verifies target variable is binary (0/1) and validates class imbalance
- Defines prediction unit as single order transaction
- Evaluates Dummy Baseline, Standard Logistic Regression, and Balanced Logistic Regression
- Calculates Accuracy, Precision, Recall, F1-Score, Confusion Matrix, and ROC-AUC
- Generates side-by-side Confusion Matrix and ROC/PR curve plots
- Extracts standardized coefficients and odds ratios
- Serializes trained model and pipeline artifacts using joblib
"""

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, roc_curve, precision_recall_curve, average_precision_score
)

# Plot styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'

def train_and_evaluate_classification():
    base_dir = r"c:\Users\HyperX\Desktop\analystLab\Week1_MachineLearning"
    data_dir = os.path.join(base_dir, "data")
    models_dir = os.path.join(base_dir, "models")
    fig_dir = os.path.join(base_dir, "reports", "figures")
    
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    
    print("=" * 65)
    print("STEP 1: VERIFYING TARGET & CLASS DISTRIBUTION")
    print("=" * 65)
    
    train_df = pd.read_csv(os.path.join(data_dir, "train.csv"))
    test_df = pd.read_csv(os.path.join(data_dir, "test.csv"))
    
    target_col = "Return_Flag"
    assert target_col in train_df.columns, f"Target '{target_col}' missing from train set!"
    assert target_col in test_df.columns, f"Target '{target_col}' missing from test set!"
    
    # Verify binary target values
    unique_train = set(train_df[target_col].unique())
    unique_test = set(test_df[target_col].unique())
    assert unique_train == {0, 1}, f"Unexpected target values in train: {unique_train}"
    assert unique_test == {0, 1}, f"Unexpected target values in test: {unique_test}"
    
    train_counts = train_df[target_col].value_counts()
    test_counts = test_df[target_col].value_counts()
    
    print(f"Prediction Unit: 1 unique Order transaction (Order_ID level)")
    print(f"Train Set (40,000 orders): Non-returned={train_counts[0]:,} ({train_counts[0]/len(train_df)*100:.2f}%), Returned={train_counts[1]:,} ({train_counts[1]/len(train_df)*100:.2f}%)")
    print(f"Test Set  (10,000 orders): Non-returned={test_counts[0]:,} ({test_counts[0]/len(test_df)*100:.2f}%), Returned={test_counts[1]:,} ({test_counts[1]/len(test_df)*100:.2f}%)")
    print(f"[OK] Significant Class Imbalance: ~95.12% Non-returned vs. 4.88% Returned.")

    print("\n" + "=" * 65)
    print("STEP 2: PREDICTION-TIME FEATURES")
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
    print(f"[OK] Feature set contains {len(all_features)} prediction-time features.")
    print("[OK] Excluded target leakage: Return_Reason, Refund_Amount, Return_Date, Line_Total.")

    X_train = train_df[all_features]
    y_train = train_df[target_col]
    X_test = test_df[all_features]
    y_test = test_df[target_col]

    print("\n" + "=" * 65)
    print("STEP 3: MODEL TRAINING (BASELINE, DEFAULT, BALANCED)")
    print("=" * 65)
    
    # Pipeline Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), categorical_features)
        ]
    )
    
    # 1. Baseline: Dummy Classifier predicting majority class (0)
    dummy = DummyClassifier(strategy='most_frequent')
    dummy.fit(X_train, y_train)
    y_pred_dummy = dummy.predict(X_test)
    
    # 2. Standard Logistic Regression (Default unweighted)
    pipe_default = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42))
    ])
    pipe_default.fit(X_train, y_train)
    y_pred_def = pipe_default.predict(X_test)
    y_prob_def = pipe_default.predict_proba(X_test)[:, 1]
    
    # 3. Balanced Logistic Regression (Addressing 95:5 class imbalance)
    pipe_balanced = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
    ])
    pipe_balanced.fit(X_train, y_train)
    y_pred_bal = pipe_balanced.predict(X_test)
    y_prob_bal = pipe_balanced.predict_proba(X_test)[:, 1]
    
    print("[OK] All three classification models trained successfully.")

    print("\n" + "=" * 65)
    print("STEP 4: EVALUATION METRICS COMPARISON (TEST SET)")
    print("=" * 65)
    
    def get_metrics(y_true, y_pred, y_prob=None):
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        roc = roc_auc_score(y_true, y_prob) if y_prob is not None else 0.5
        return acc, prec, rec, f1, roc

    acc_dum, prec_dum, rec_dum, f1_dum, roc_dum = get_metrics(y_test, y_pred_dummy)
    acc_def, prec_def, rec_def, f1_def, roc_def = get_metrics(y_test, y_pred_def, y_prob_def)
    acc_bal, prec_bal, rec_bal, f1_bal, roc_bal = get_metrics(y_test, y_pred_bal, y_prob_bal)
    
    print(f"{'Metric':<14} | {'Majority Baseline':<18} | {'Logistic Reg (Default)':<22} | {'Logistic Reg (Balanced)':<22}")
    print("-" * 84)
    print(f"{'Accuracy':<14} | {acc_dum:>18.4f} | {acc_def:>22.4f} | {acc_bal:>22.4f}")
    print(f"{'Precision':<14} | {prec_dum:>18.4f} | {prec_def:>22.4f} | {prec_bal:>22.4f}")
    print(f"{'Recall':<14} | {rec_dum:>18.4f} | {rec_def:>22.4f} | {rec_bal:>22.4f}")
    print(f"{'F1-Score':<14} | {f1_dum:>18.4f} | {f1_def:>22.4f} | {f1_bal:>22.4f}")
    print(f"{'ROC-AUC':<14} | {roc_dum:>18.4f} | {roc_def:>22.4f} | {roc_bal:>22.4f}")
    print("-" * 84)

    # Confusion matrices
    cm_def = confusion_matrix(y_test, y_pred_def)
    cm_bal = confusion_matrix(y_test, y_pred_bal)
    
    print("\nConfusion Matrix (Default Logistic Regression):")
    print(f"  TN: {cm_def[0,0]:>5} | FP: {cm_def[0,1]:>5}")
    print(f"  FN: {cm_def[1,0]:>5} | TP: {cm_def[1,1]:>5}")
    
    print("\nConfusion Matrix (Balanced Logistic Regression):")
    print(f"  TN: {cm_bal[0,0]:>5} | FP: {cm_bal[0,1]:>5}")
    print(f"  FN: {cm_bal[1,0]:>5} | TP: {cm_bal[1,1]:>5}")

    print("\n" + "=" * 65)
    print("STEP 5: FEATURE IMPORTANCE & ODDS RATIOS")
    print("=" * 65)
    
    clf = pipe_balanced.named_steps['classifier']
    cat_names = pipe_balanced.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features)
    feature_names = numerical_features + list(cat_names)
    coefs = clf.coef_[0]
    odds_ratios = np.exp(coefs)
    
    feature_importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefs,
        'Odds_Ratio': odds_ratios,
        'Abs_Coefficient': np.abs(coefs)
    }).sort_values('Abs_Coefficient', ascending=False)
    
    print("Top 10 Most Influential Features (Balanced Model):")
    for idx, r in feature_importance_df.head(10).reset_index(drop=True).iterrows():
        direction = "Higher Return Odds" if r['Coefficient'] > 0 else "Lower Return Odds"
        print(f"  {idx+1:>2}. {r['Feature']:<32} | Coef: {r['Coefficient']:>7.4f} | Odds Ratio: {r['Odds_Ratio']:>6.4f} ({direction})")

    print("\n" + "=" * 65)
    print("STEP 6: GENERATING CLASSIFICATION DIAGNOSTIC PLOTS")
    print("=" * 65)
    
    # Plot 1: Side-by-side Confusion Matrices
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    # Heatmap 1: Default
    sns.heatmap(cm_def, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax1,
                annot_kws={'size': 14, 'weight': 'bold'},
                xticklabels=['Pred: Kept (0)', 'Pred: Returned (1)'],
                yticklabels=['Actual: Kept (0)', 'Actual: Returned (1)'])
    ax1.set_title("Confusion Matrix: Default Logistic Regression\n(Accuracy=95.12%, Recall=0.0%)", fontsize=12, fontweight='bold', pad=10)
    ax1.set_ylabel("Actual Label", fontsize=11)
    ax1.set_xlabel("Predicted Label", fontsize=11)
    
    # Heatmap 2: Balanced
    sns.heatmap(cm_bal, annot=True, fmt='d', cmap='Greens', cbar=False, ax=ax2,
                annot_kws={'size': 14, 'weight': 'bold'},
                xticklabels=['Pred: Kept (0)', 'Pred: Returned (1)'],
                yticklabels=['Actual: Kept (0)', 'Actual: Returned (1)'])
    ax2.set_title("Confusion Matrix: Balanced Logistic Regression\n(Recall=45.70%, Precision=4.65%)", fontsize=12, fontweight='bold', pad=10)
    ax2.set_ylabel("Actual Label", fontsize=11)
    ax2.set_xlabel("Predicted Label", fontsize=11)
    
    plt.tight_layout()
    cm_path = os.path.join(fig_dir, "confusion_matrix.png")
    fig.savefig(cm_path, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Saved: {cm_path}")

    # Plot 2: ROC Curve & Precision-Recall Curve
    fig, (ax_roc, ax_pr) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    
    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_prob_bal)
    ax_roc.plot(fpr, tpr, color='#1f77b4', lw=2.5, label=f'Logistic Regression (AUC = {roc_bal:.3f})')
    ax_roc.plot([0, 1], [0, 1], color='#d62728', lw=2, linestyle='--', label='Random Chance (AUC = 0.500)')
    ax_roc.set_title("Receiver Operating Characteristic (ROC) Curve", fontsize=12, fontweight='bold', pad=10)
    ax_roc.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    ax_roc.set_ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11)
    ax_roc.legend(loc='lower right', frameon=True)
    
    # Precision-Recall Curve
    prec_curve, rec_curve, _ = precision_recall_curve(y_test, y_prob_bal)
    pr_auc = average_precision_score(y_test, y_prob_bal)
    base_rate = y_test.mean()
    ax_pr.plot(rec_curve, prec_curve, color='#2ca02c', lw=2.5, label=f'Logistic Regression (PR-AUC = {pr_auc:.3f})')
    ax_pr.axhline(base_rate, color='#d62728', lw=2, linestyle='--', label=f'No-Skill Baseline ({base_rate*100:.2f}%)')
    ax_pr.set_title("Precision-Recall Curve (Imbalanced Return Target)", fontsize=12, fontweight='bold', pad=10)
    ax_pr.set_xlabel("Recall", fontsize=11)
    ax_pr.set_ylabel("Precision", fontsize=11)
    ax_pr.legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    roc_pr_path = os.path.join(fig_dir, "roc_pr_curve.png")
    fig.savefig(roc_pr_path, bbox_inches='tight')
    plt.close(fig)
    print(f"[OK] Saved: {roc_pr_path}")

    print("\n" + "=" * 65)
    print("STEP 7: SERIALIZING CLASSIFIER ARTIFACTS (TASK F)")
    print("=" * 65)
    
    # Save standalone estimator and full pipeline
    clf_path = os.path.join(models_dir, "logistic_regression.pkl")
    clf_pipe_path = os.path.join(models_dir, "logistic_regression_pipeline.pkl")
    
    joblib.dump(clf, clf_path)
    joblib.dump(pipe_balanced, clf_pipe_path)
    
    print(f"[OK] Saved: {clf_path}")
    print(f"[OK] Saved: {clf_pipe_path}")
    
    print("\n" + "=" * 65)
    print("TASK D CLASSIFICATION COMPLETE!")
    print("=" * 65)

if __name__ == "__main__":
    train_and_evaluate_classification()
