import pandas as pd
import numpy as np

# Sleep Duration Ordinal Mapping
# Sleep quality is ordinal: 7-8 hours is healthiest (highest score), down to less than 5 hours / irregular sleep.
SLEEP_MAP = {
    "7-8 hours": 3,
    "More than 8 hours": 4,
    "5-6 hours": 2,
    "Less than 5 hours": 1,
    "Irregular Sleep": 0
}

# Dietary Habits Ordinal Mapping
# Healthy food is high, down to unhealthy and irregular diet.
DIET_MAP = {
    "Healthy": 3,
    "Moderate": 2,
    "Unhealthy": 1,
    "Irregular Diet": 0
}

# Binary Categorical Mappings
BINARY_MAPS = {
    "Gender": {"Male": 1, "Female": 0},
    "Family.History.of.Mental.Illness": {"Yes": 1, "No": 0},
    "Have.you.ever.had.suicidal.thoughts..": {"Yes": 1, "No": 0}
}

# Features that must be excluded from prediction
COLS_TO_DROP = ["id", "Job.Satisfaction"]

def preprocess_features(df: pd.DataFrame, trained_columns=None) -> pd.DataFrame:
    """
    Preprocess raw student features DataFrame for training or prediction.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input raw data containing student characteristics.
    trained_columns : list, optional
        The exact list of feature columns from the training set. If provided,
        one-hot encoded columns will be reindexed/aligned to match this list.
        
    Returns:
    --------
    pd.DataFrame
        Preprocessed DataFrame containing only numeric columns, aligned and ready for ML models.
    """
    # 1. Work on a copy to prevent side effects
    processed_df = df.copy()
    
    # 2. Drop columns that are not useful for prediction
    for col in COLS_TO_DROP:
        if col in processed_df.columns:
            processed_df = processed_df.drop(columns=[col])
            
    # 3. Apply binary mapping (1 for Yes/Male, 0 for No/Female)
    for col, mapping in BINARY_MAPS.items():
        if col in processed_df.columns:
            # Map values; fill unknown or missing values with the most common mapping (0)
            processed_df[col] = processed_df[col].map(mapping).fillna(0).astype(int)
            
    # 4. Apply ordinal mappings
    if "Sleep.Duration" in processed_df.columns:
        processed_df["Sleep.Duration"] = processed_df["Sleep.Duration"].map(SLEEP_MAP).fillna(2).astype(int)
        
    if "Dietary.Habits" in processed_df.columns:
        processed_df["Dietary.Habits"] = processed_df["Dietary.Habits"].map(DIET_MAP).fillna(2).astype(int)
        
    # 5. One-hot encode the 'Degree' column
    # If 'Degree' is present, we get dummies.
    if "Degree" in processed_df.columns:
        # Get dummies for Degree
        degree_dummies = pd.get_dummies(processed_df["Degree"], prefix="Degree", dtype=int)
        # Drop original Degree and concatenate dummies
        processed_df = processed_df.drop(columns=["Degree"])
        processed_df = pd.concat([processed_df, degree_dummies], axis=1)
        
    # 6. Align features with trained columns (important for test split and inference!)
    if trained_columns is not None:
        # Reindex to ensure we have exactly the columns of trained_columns (in the correct order)
        # Missing dummy columns will be filled with 0, and any extra dummy columns will be dropped.
        processed_df = processed_df.reindex(columns=trained_columns, fill_value=0)
        
    # Ensure everything is numeric
    for col in processed_df.columns:
        if processed_df[col].dtype == object:
            # Fallback label encoding if any categorical slipped through
            processed_df[col] = pd.factorize(processed_df[col])[0]
            
    return processed_df
