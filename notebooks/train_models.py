import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from xgboost import XGBClassifier

def evaluate_model(model, X_test, y_test, name):
    """
    Evaluate a model on the test set and print metrics.
    """
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"\n=================== {name} Test Set Evaluation ===================")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)
    
    return {
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1 Score": f1,
        "Confusion Matrix": cm.tolist()
    }

def main():
    print("Starting Phase 4: Machine Learning Model Training & Tuning...")
    
    # 1. Paths setup
    data_dir = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\data_clean"
    model_dir = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\backend\models"
    os.makedirs(model_dir, exist_ok=True)
    
    # 2. Load splits
    X_train = pd.read_csv(os.path.join(data_dir, "X_train.csv"))
    X_test = pd.read_csv(os.path.join(data_dir, "X_test.csv"))
    y_train = pd.read_csv(os.path.join(data_dir, "y_train.csv")).values.ravel()
    y_test = pd.read_csv(os.path.join(data_dir, "y_test.csv")).values.ravel()
    
    # 3. Setup Stratified Cross-Validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    results = {}
    best_models = {}
    
    # ==========================================
    # Model 1: Logistic Regression (Pipeline + Scale)
    # ==========================================
    print("\n--- Training Logistic Regression ---")
    lr_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('lr', LogisticRegression(solver='liblinear', random_state=42))
    ])
    
    lr_param_grid = {
        'lr__C': [0.01, 0.1, 1.0, 10.0],
        'lr__penalty': ['l1', 'l2']
    }
    
    lr_grid = GridSearchCV(lr_pipeline, lr_param_grid, cv=cv, scoring='f1', n_jobs=-1)
    lr_grid.fit(X_train, y_train)
    
    print(f"Best Hyperparameters: {lr_grid.best_params_}")
    print(f"Best CV F1 Score    : {lr_grid.best_score_:.4f}")
    
    best_models["Logistic Regression"] = lr_grid.best_estimator_
    results["Logistic Regression"] = evaluate_model(lr_grid.best_estimator_, X_test, y_test, "Logistic Regression")

    # ==========================================
    # Model 2: Random Forest (No scaling needed)
    # ==========================================
    print("\n--- Training Random Forest ---")
    rf = RandomForestClassifier(random_state=42)
    
    # Fast, reasonable parameter grid
    rf_param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [5, 10, None]
    }
    
    rf_grid = GridSearchCV(rf, rf_param_grid, cv=cv, scoring='f1', n_jobs=-1)
    rf_grid.fit(X_train, y_train)
    
    print(f"Best Hyperparameters: {rf_grid.best_params_}")
    print(f"Best CV F1 Score    : {rf_grid.best_score_:.4f}")
    
    best_models["Random Forest"] = rf_grid.best_estimator_
    results["Random Forest"] = evaluate_model(rf_grid.best_estimator_, X_test, y_test, "Random Forest")

    # ==========================================
    # Model 3: XGBoost (No scaling needed)
    # ==========================================
    print("\n--- Training XGBoost ---")
    xgb = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
    
    xgb_param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 6, 9],
        'learning_rate': [0.05, 0.1, 0.2]
    }
    
    xgb_grid = GridSearchCV(xgb, xgb_param_grid, cv=cv, scoring='f1', n_jobs=-1)
    xgb_grid.fit(X_train, y_train)
    
    print(f"Best Hyperparameters: {xgb_grid.best_params_}")
    print(f"Best CV F1 Score    : {xgb_grid.best_score_:.4f}")
    
    best_models["XGBoost"] = xgb_grid.best_estimator_
    results["XGBoost"] = evaluate_model(xgb_grid.best_estimator_, X_test, y_test, "XGBoost")

    # ==========================================
    # Model Comparison & Champion Selection
    # ==========================================
    print("\n\n=================== Model Comparison Summary ===================")
    comparison_data = []
    for name, metrics in results.items():
        comparison_data.append({
            "Model": name,
            "Accuracy": metrics["Accuracy"],
            "Precision": metrics["Precision"],
            "Recall": metrics["Recall"],
            "F1 Score": metrics["F1 Score"]
        })
    comparison_df = pd.DataFrame(comparison_data)
    print(comparison_df.to_string(index=False))
    
    # Select the champion model (highest F1 score)
    champion_name = comparison_df.loc[comparison_df['F1 Score'].idxmax()]['Model']
    champion_model = best_models[champion_name]
    
    print(f"\nChampion Model: {champion_name} (F1 Score: {results[champion_name]['F1 Score']:.4f})")
    
    # Save best model using joblib
    model_save_path = os.path.join(model_dir, "best_model.joblib")
    joblib.dump(champion_model, model_save_path)
    print(f"Saved champion model to: {model_save_path}")
    
    print("\nPhase 4 complete!")

if __name__ == "__main__":
    main()
