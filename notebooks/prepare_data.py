import os
import sys
import json
import pandas as pd
from sklearn.model_selection import train_test_split

# Add backend directory to path so we can import app.utils.preprocess
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.utils.preprocess import preprocess_features

def main():
    print("Starting Phase 2: Machine Learning Preparation...")
    
    # 1. Paths setup
    raw_data_path = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\data_clean\student_data_clean.csv"
    output_dir = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\data_clean"
    model_dir = r"c:\Users\hp\Desktop\Projects\Student-Mental-health-analysis\backend\models"
    
    os.makedirs(model_dir, exist_ok=True)
    
    # 2. Load dataset
    print(f"Loading raw dataset from: {raw_data_path}")
    df = pd.read_csv(raw_data_path)
    
    # 3. Separate Features (X) and Target (y)
    X_raw = df.drop(columns=["Depression"])
    y = df["Depression"]
    
    # 4. Preprocess Features
    print("Preprocessing raw features...")
    # First preprocess without trained_columns to get the full feature set (especially one-hot dummies)
    X_processed = preprocess_features(X_raw)
    
    # Get the list of preprocessed column names
    feature_columns = X_processed.columns.tolist()
    print(f"Total features after preprocessing/encoding: {len(feature_columns)}")
    
    # Save the list of feature columns for prediction time (to prevent training-serving skew)
    feature_path = os.path.join(model_dir, "model_features.json")
    with open(feature_path, "w") as f:
        json.dump(feature_columns, f, indent=2)
    print(f"Saved feature column names to: {feature_path}")
    
    # 5. Train-Test Split (80% Train, 20% Test)
    # Using stratify=y to maintain the same class ratio (58.55% vs 41.45%) in both train and test splits
    print("Performing stratified train-test split (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, 
        y, 
        test_size=0.20, 
        random_state=42, 
        stratify=y
    )
    
    # 6. Save splits
    x_train_path = os.path.join(output_dir, "X_train.csv")
    x_test_path = os.path.join(output_dir, "X_test.csv")
    y_train_path = os.path.join(output_dir, "y_train.csv")
    y_test_path = os.path.join(output_dir, "y_test.csv")
    
    X_train.to_csv(x_train_path, index=False)
    X_test.to_csv(x_test_path, index=False)
    y_train.to_csv(y_train_path, index=False)
    y_test.to_csv(y_test_path, index=False)
    
    print(f"Data successfully split and saved to directory: {output_dir}")
    print(f" - X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    print(f" - X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")
    print("Phase 2 complete!")

if __name__ == "__main__":
    main()
